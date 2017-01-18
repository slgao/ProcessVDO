__author__ = 'gao.shulin'
# coding: utf-8
import sys
import os
import glob
import re
import time
import shutil
import matplotlib.pyplot as plt
# import third party modules
if sys.version_info.major < 3:
    import Tkinter as tk
else:
    import tkinter as tk
from PyQt4 import QtGui, QtCore
import py_gui.main_window as mw
import py_gui.resolution_analyse as ra
import py_gui.from_vdo as frvdo
import py_gui.from_hdf5 as frhd5
import py_gui.output_hdf5 as outh5
import py_gui.export_pano_img as expimg
import py_gui.export_pano_gps as expgps
import py_gui.about_dialog as aboutd

# import local modules
import gui
from cli import get_args
import vdo
import vdo.VideoRead.VideoRead as VR
#import pstats
###################
import ipdb


class Options(object):
    attributes = ['debug', 'use_cams',
                  'AbExtCounter', 'save', 'Jumping', 'FrameInfo'
                  ]

    def __init__(self, **kwargs):
        for attr in self.__class__.attributes:
            setattr(self, attr, kwargs.get(attr))


class CamInfo:

    def __init__(self, ImType, Folder, CamID, divider, ExtCounterRange):
        self.ImType = ImType
        self.Folder = Folder
        self.CamID = CamID
        self.divider = divider
        self.ExtCounterRange = ExtCounterRange


def jpeg():
    im_type = 'JPEG'
    return im_type


def c_linear():
    im_type = 'CLinear'
    return im_type


def bw_linear():
    im_type = 'BWLinear'
    return im_type

# Determine whether image is color linear or BW linear or JPEG
img_type = {
    513: jpeg,
    514: c_linear,
    515: bw_linear
}


class DialogWindow(QtGui.QDialog):
    # set common features used by QDialog

    def __init__(self, parent=None):
        super(DialogWindow, self).__init__(parent)

    def set_path(self, lineEdit_path):
        file_name = str(QtGui.QFileDialog.getExistingDirectory(
            self, "Select Directory"))
        if file_name is not '':
            lineEdit_path.setText(file_name)

    def show_warning(self, message):
        QtGui.QMessageBox.critical(
            self, "Warning", message, QtGui.QMessageBox.Ok)

    def show_info(self, message):
        QtGui.QMessageBox.information(self, "Information!", message)


class ResAnalyseWindow(QtGui.QDialog):

    def __init__(self, parent=None):
        super(ResAnalyseWindow, self).__init__(parent)
        self.ui = ra.Ui_Dialog()
        self.ui.setupUi(self)
        self.set_connections()

    def set_connections(self):
        self.ui.from_vdo_btn.clicked.connect(self.from_vdo_btn_clicked)
        self.ui.from_hdf5_btn.clicked.connect(self.from_hdf5_btn_clicked)

    def from_vdo_btn_clicked(self):
        from_vdo_window = FromVDOWindow()
        # make the background window freeze
        from_vdo_window.setModal(True)
        from_vdo_window.show()
        from_vdo_window.exec_()

    def from_hdf5_btn_clicked(self):
        from_hdf5_window = FH5Window()
        # make the background window freeze
        from_hdf5_window.setModal(True)
        from_hdf5_window.show()
        from_hdf5_window.exec_()


class OutHdf5Window(DialogWindow):

    def __init__(self, parent=None):
        super(OutHdf5Window, self).__init__(parent)
        self.ui = outh5.Ui_Dialog()
        self.ui.setupUi(self)
        self.set_connections()

    def set_connections(self):
        # vdo path and save path need to be set
        self.ui.vdo_browse_btn.clicked.connect(
            lambda: self.set_path(self.ui.vdo_path))
        self.ui.save_browse_btn.clicked.connect(
            lambda: self.set_path(self.ui.save_path))
        # TODO: add more button set_connections


class ExpPanoImgWindow(DialogWindow):

    def __init__(self, parent=None):
        super(ExpPanoImgWindow, self).__init__(parent)
        self.ui = expimg.Ui_Dialog()
        self.ui.setupUi(self)
        self.set_connections()

    def set_connections(self):
        self.ui.vdo_browse_btn.clicked.connect(
            lambda: self.set_path(self.ui.vdo_path))
        self.ui.img_save_browse_btn.clicked.connect(
            lambda: self.set_path(self.ui.img_save_path))
        # TODO: add more button set_connections


class ExpPanoGPSWindow(DialogWindow):

    def __init__(self, parent=None):
        super(ExpPanoGPSWindow, self).__init__(parent)
        self.ui = expgps.Ui_Dialog()
        self.ui.setupUi(self)
        self.set_connections()

    def set_connections(self):
        self.ui.vdo_browse_btn.clicked.connect(
            lambda: self.set_path(self.ui.vdo_path))
        self.ui.img_save_browse_btn.clicked.connect(
            lambda: self.set_path(self.ui.img_save_path))
        self.ui.poi_browse_btn.clicked.connect(
            lambda: self.set_path(self.ui.poi_path))
        self.ui.gps_save_browse_btn.clicked.connect(
            lambda: self.set_path(self.ui.gps_path))
        # TODO: add more button set_connections


class WThreadFH5Window(QtCore.QThread):

    attributes = ['h5_path', 'lb_path']

    def __init__(self, parent=None, **kwargs):
        super(WThreadFH5Window, self).__init__(parent)
        for attr in self.__class__.attributes:
            setattr(self, attr, kwargs.get(attr))

    def run(self):

        # get run name from the h5 folder
        # ipdb.set_trace()
        # check whether hdf5 path is valid
        if not os.path.exists(self.h5_path):
            self.emit(QtCore.SIGNAL("show_warning"), "HDF5 path is not valid!")
            return
        else:
            # check whether h5 files exist
            h5s = glob.glob("{}/*.h5".format(self.h5_path))
            if not h5s:
                self.emit(QtCore.SIGNAL("show_warning"),
                          "No HDF5 files are found!")
                return
            # here below not refactored
            try:
                fn_evnt = r'{}/*.evnt.txt'.format(self.h5_path)
                fn_evnt = glob.glob(fn_evnt)
            except ValueError:
                self.emit(QtCore.SIGNAL("show_warning"),
                          "event or s3db file(s) ... are not found!")
                return
            evnt = re.split('/|\\\\', fn_evnt[0])[-1]
            run = re.split(r'\.(?!\d)', evnt)[0]

        # check whether the LB data of the processed run exists
        fn_lbd = os.path.join((self.lb_path), "{}.lbd".format(run))
        fn_lbe = os.path.join((self.lb_path), "{}.lbe".format(run))

        if not os.path.exists(self.lb_path):
            self.emit(QtCore.SIGNAL("show_warning"),
                      "LockBox data path is not valid!")
            return
        # ipdb.set_trace()
        if not (os.path.exists(fn_lbd) and os.path.exists(fn_lbe)):
            self.emit(QtCore.SIGNAL("show_warning"),
                      "No LockBox data found in the folder!")
            return
        # else start processing

        # copy LB data to h5 folder
        shutil.copy(fn_lbe, self.h5_path)
        shutil.copy(fn_lbd, self.h5_path)

        # resolution analyse
        options = Options()  # fake options
        if options.debug and not options.use_cams:
            options.use_cams = ['60']
        # TODO: handle this also in get_args?
        if options.use_cams is None:
            # use all
            if options.debug:
                options.use_cams = ['60']
            else:
                options.use_cams = vdo.check.VdoRun.default_cams

        if options.save is not None and not len(options.save):
            # empty list -> use_cams
            options.save = options.use_cams

        # TODO: switch automatic between py2exe app and python script app
        # Use this only for py2exe application --Shulin
        elif options.save is None:
            options.save = options.use_cams

        speed_max = 40
        select_range = {'subrange_selected': False}

        # select_range={'subrange_selected' : True, 'offset_dist' : 500,
        # 'select_dist' : 50*1000} #15092918

        # this will introduce QPixmap error
        vdo.check.analyseVdo(folder=self.h5_path, run=None, options=options,
                             speed_max=speed_max, select_range=select_range)

        # update the prgressbar
        # import time
        # time.sleep(10)
        self.emit(QtCore.SIGNAL("show_info"), "Done!")

        return

    def terminate(self):
        # TODO: need to use it right
        self.terminate()
        self.emit(QtCore.SIGNAL("reset_dialog_window"))


class FH5Window(DialogWindow):

    def __init__(self, parent=None):
        super(FH5Window, self).__init__(parent)
        self.ui = frhd5.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.cancel_btn.setEnabled(False)
        self.ui.stop_btn.setEnabled(False)
        self.set_connections()

    def set_connections(self):
        self.ui.h5_browse_btn.clicked.connect(
            lambda: self.set_path(self.ui.h5_path))
        self.ui.lockbox_browse_btn.clicked.connect(
            lambda: self.set_path(self.ui.lockbox_path))
        # TODO: add more button set_connections
        self.ui.out_graph_btn.clicked.connect(self.out_graph_btn_clicked)

    def reset_dialog_window(self):
        self.ui.out_graph_btn.setEnabled(True)
        self.ui.cancel_btn.setEnabled(False)
        self.ui.stop_btn.setEnabled(False)
        self.ui.progressBar.setValue(0)

    def show_info(self, message):
        super(FH5Window, self).show_info(message)
        self.reset_dialog_window()

    def show_warning(self, message):
        super(FH5Window, self).show_warning(message)
        self.reset_dialog_window()

    def out_graph_btn_clicked(self):
        # self.ui.progressBar.setMaximum()
        h5_path = str(self.ui.h5_path.text())
        lb_path = str(self.ui.lockbox_path.text())
        # create thread to do the processing
        self.get_thread = WThreadFH5Window(h5_path=h5_path, lb_path=lb_path)
        # connect signals
        self.connect(self.get_thread, QtCore.SIGNAL(
            "show_info"), self.show_info)
        self.connect(self.get_thread, QtCore.SIGNAL(
            "show_warning"), self.show_warning)
        self.connect(self.get_thread, QtCore.SIGNAL(
            "reset_dialog_window"), self.reset_dialog_window)
        # initialize progressBar
        self.get_thread.start()
        self.ui.out_graph_btn.setEnabled(False)
        self.ui.cancel_btn.setEnabled(False)
        self.ui.stop_btn.setEnabled(True)
        self.ui.stop_btn.clicked.connect(self.get_thread.terminate)


class FromVDOWindow(DialogWindow):

    def __init__(self, parent=None):
        super(FromVDOWindow, self).__init__(parent)
        self.ui = frvdo.Ui_Dialog()
        self.ui.setupUi(self)
        self.set_connections()

    def set_connections(self):
        self.ui.lockbox_browse_btn.clicked.connect(
            lambda: self.set_path(self.ui.lockbox_path))
        self.ui.vdo_browse_btn.clicked.connect(
            lambda: self.set_path(self.ui.vdo_path))
        self.ui.save_browse_btn.clicked.connect(
            lambda: self.set_path(self.ui.save_path))
        # TODO: add more button set_connections


class AboutDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.ui = aboutd.Ui_Dialog()
        self.ui.setupUi(self)
    # def connections(self):


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = mw.Ui_MainWindow()
        self.ui.setupUi(self)
        # set connections for the buttons
        self.set_connections()

    def set_connections(self):
        self.ui.res_btn.clicked.connect(self.res_btn_clicked)
        self.ui.hdf5_btn.clicked.connect(self.hdf5_btn_clicked)
        self.ui.pano_img_btn.clicked.connect(self.pano_img_btn_clicked)
        self.ui.pano_gps_btn.clicked.connect(self.pano_gps_btn_clicked)
        self.ui.actionAbout.triggered.connect(self.actionAbout_triggered)

    def res_btn_clicked(self):
        res_analyse_window = ResAnalyseWindow()
        # make the background window freeze
        res_analyse_window.setModal(True)
        res_analyse_window.show()
        res_analyse_window.exec_()

    def hdf5_btn_clicked(self):
        out_hdf5_window = OutHdf5Window()
        # make the background window freeze
        out_hdf5_window.setModal(True)
        out_hdf5_window.show()
        out_hdf5_window.exec_()

    def pano_img_btn_clicked(self):
        exp_pano_img_window = ExpPanoImgWindow()
        # make the background window freeze
        exp_pano_img_window.setModal(True)
        exp_pano_img_window.show()
        exp_pano_img_window.exec_()

    def pano_gps_btn_clicked(self):
        exp_pano_gps_window = ExpPanoGPSWindow()
        # make the background window freeze
        exp_pano_gps_window.setModal(True)
        exp_pano_gps_window.show()
        exp_pano_gps_window.exec_()

    def actionAbout_triggered(self):
        about_window = AboutDialog()
        # make the background window freeze
        about_window.setModal(True)
        about_window.show()
        about_window.exec_()

if __name__ == "__main__":
    use_tkinter_gui, use_pyqt_gui = False, True
    if use_tkinter_gui:
        root = tk.Tk()
        file_dialog = gui.TkFileDialog(root)
        file_dialog.pack()
        #the_lable = Label(root, text = "vdo_check")
        # the_lable.pack()
        root.mainloop()
        sys.exit()
    elif use_pyqt_gui:
        app = QtGui.QApplication(sys.argv)
        myapp = MainWindow()
        myapp.show()
        sys.exit(app.exec_())

    else:
        options = get_args()
        # TODO: set in options/cli or some parameter file!!
        select_range = {'subrange_selected': False}
        # select_range={'subrange_selected' : True, 'offset_dist' : 710/8*1000, 'select_dist' : 70/8*1000} #15092918
        #select_range = {'subrange_selected' : True, 'offset_dist' : 80E3/8, 'select_dist' : 20E3/8}
        #select_range = {'subrange_selected' : True, 'offset_dist' : (99E3)/8, 'select_dist' : (225-99)*1E3/8}
        #select_range = {'subrange_selected' : True, 'offset_dist' : (34E3)/8, 'select_dist' : (56-35)*1E3/8}
        #select_range = {'subrange_selected' : True, 'offset_dist' : (69E3)/8, 'select_dist' : (81-69)*1E3/8}
        speed_max = 40

        if options.debug and not options.use_cams:
            options.use_cams = ['60']
        # TODO: handle this also in get_args?
        if options.use_cams is None:
            # use all
            if options.debug:
                options.use_cams = ['60']
            else:
                options.use_cams = vdo.check.VdoRun.default_cams

        if options.save is not None and not len(options.save):
            # empty list -> use_cams
            options.save = options.use_cams

        # TODO: switch automatic between py2exe app and python script app
        # Use this only for py2exe application --Shulin
        elif options.save is None:
            options.save = options.use_cams

        if options.debug:
            Exc = None
        else:
            Exc = Exception

        range_exist = None  # Whether a range exists in the camera images
        ext_counter_range = []

        factor = 8.0  # primary Int Counter is 1/8
        if options.arg[0][-3:] == "vdo":
            folder = os.path.dirname(os.path.abspath(options.arg[0]))
        else:
            folder = os.path.abspath(options.arg[0])

        run = re.split('/|\\\\', folder)[-1]

        try:
            fn_evnt = r'{}/*.evnt.txt'.format(folder)
            fn_s3db = r'{}/*.s3db'.format(folder)
            fn_lbd = r'{}.lbd'.format(run)
            fn_lbe = r'{}.lbe'.format(run)
            # fn_yaml = r'{}.yaml'.format('columns') # TODO: config.yaml in
            # libs/vdo or local to exe should be enough! Generate solution for
            # py2exe version.
            fn_evnt = glob.glob(fn_evnt)
            fn_s3db = glob.glob(fn_s3db)
            files_copy = [fn_evnt[0], fn_s3db[0], fn_lbd, fn_lbe]
            # print fn_evnt, fn_s3db
        except ValueError:
            print("File(s) ... are missing!")

        if options.img_export:  # Export camera images
            if len(options.img_export) == 3:  # cam_id, 1st_ext_cnt, 2nd_ext_cnt
                range_exist = True
            else:
                range_exist = False
                ext_counter_range = [options.img_export[0]]
                if (options.img_export[0] not in ('c50', 'c51')):
                    print("External counter range should be given to the linear camera")
                    sys.exit()
        else:
            try:
                if options.eval_multi:
                    #cProfile.run('_ = vdo.check.analyseVdo_multiDir(args = options)', 'restats')
                    #p = pstats.Stats('restats')
                    # p.sort_stats('cumulative').print_stats(10)
                    _ = vdo.check.analyseVdo_multiDir(
                        args=options, speed_max=speed_max)
                    sys.exit()
                else:
                    # if args.write_csv:
                    if options.write_csv:  # TODO - and eventually check if vdo files are in folder
                        VR.WriteCSV(options.arg[0])
                        # pass

                    # Check whether lbd lbe files exist
                    if glob.glob('{}/{}.lbd'.format(folder, run)) and glob.glob('{}/{}.lbe'.format(folder, run)):
                        print("There exist lbd, lbe files!")
                    # Copy evnt.txt, s3db, lbe, lbd and yaml files to folder
                    else:
                        try:
                            for f in files_copy:
                                shutil.copy(f, run)
                        except IOError:
                            print("No external lbd lbe files copied!")
                            sys.exit()

                    '''Analyse the csv files from vdo files and output graphs'''
                    #time1 = time.time()
                    # TODO: set speed and select_range in options
                    vdoData, cam_results, figs = vdo.check.analyseVdo(
                        folder=folder, run=None, options=options, speed_max=speed_max, select_range=select_range)
                    #time2 = time.time()
                    #print ("took {} seconds".format(time2-time1))
                sys.exit()
            except Exc as e:
                plt.close('all')
                raise e

        # get external counter

        ext_counter_range = [options.img_export[0]]
        cam_id = ext_counter_range[0]

        if range_exist:
            ext_cnt_range = [int(s)
                             for s in options.img_export[1:] if s.isdigit()]
            ext_counter_range += ext_cnt_range

            vdoData = vdo.check.VdoData()
            vdoData.load(folder, None)  # run changed to folder
            processed = vdo.check.process_extData(None,
                                                  vdoData.trackNetCfg,
                                                  vdoData.evnt,
                                                  factor)

            dividers = processed['s3db']
            divider = vdo.check.get_divider(dividers, cam_id)

            # DMA event txt
            dmaSync, cntExt_interpf, cntInt_interpf = processed['evnt']
            print(dmaSync)

            try:
                InternalRange = cntInt_interpf(
                    [ext_counter_range[1], ext_counter_range[2]])
            except ValueError:
                print('No External Counter Exist!!')
                sys.exit()

            save_range = "{}({}, {})".format(ext_counter_range[
                0], InternalRange[0], InternalRange[1])
        else:
            save_range = "{}".format(ext_counter_range[0])
        print(save_range)

        #filename = args.arg[0]
        directory = options.arg[0]
        data_out_option = 1  # Output video data, '0' = No Decompression, '1' = RGB, '2' = YUV
        save_pano_img = 0  # Export panorama camera images
        uncertainty = 0.8
        Data = VR.VdoRead(directory, save_range,
                          data_out_option, save_pano_img, uncertainty)

        if cam_id == "c50" or cam_id == "c51":  # Panorama camera images are exported in VideoRead module
            # pano_ante_dist contains the distance (mm) between antenna and two
            # pano cameras
            pano_ante_dist = [3793.5, 30000]
            poi_file = "{}_poi.csv".format(run)
            seg_file = "{}_seg.csv".format(run)
            _ = vdo.check.save_GPS_coord(
                run, poi_file, seg_file, cam_id, folder, factor, pano_ante_dist)
            sys.exit()
        else:
            if not Data[0]:
                print("No image data acquired!")
                sys.exit()
            else:
                ImType = img_type[Data[1][0].get('image_type')]()
                CamInfo = CamInfo(ImType, run, cam_id,
                                  divider, ext_counter_range)
                start = time.time()
                # Output images taken by cameras
                VR.CamIm(Data, CamInfo, len_frame=2000)
                end = time.time()
                timing = end - start
                if len(ext_counter_range) == 3:
                    print('It takes {} seconds to save images for camera {}_ExtCnt[{}, {}]!!'.format(
                        timing, cam_id, ext_counter_range[1], ext_counter_range[2]))
                # else:
                # print 'It takes {} seconds to save images for camera
                # {}!!'.format(timing, cam_id)
