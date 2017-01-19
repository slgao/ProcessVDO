# coding: utf-8
# import local modules
import sys
import os
import glob
import re
import time
import shutil
import matplotlib.pyplot as plt
from PyQt4 import QtGui, QtCore

# import third party modules
import py_gui.main_window as mw
import py_gui.export_pano_img as expimg
import py_gui.export_pano_gps as expgps
import py_gui.about_dialog as aboutd
from win_proc.dialog_window import DialogWindow
from win_proc.res_analyse_window import ResAnalyseWindow
from win_proc.out_hdf5_window import OutHdf5Window

if sys.version_info.major < 3:
    import Tkinter as tk
else:
    import tkinter as tk
import gui
from cli import get_args
import vdo
import vdo.VideoRead.VideoRead as VR
#import pstats
###################
import ipdb
__author__ = 'gao.shulin'


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
    ipdb.set_trace()
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
