from dialog_window import DialogWindow
import py_gui.output_hdf5 as outh5
from PyQt4 import QtCore
import vdo.VideoRead.VideoRead as VR
import pandas as pd
import os
import glob
import re
import shutil
import os


class WThreadOutHdf5Window(QtCore.QThread):

    attributes = ["vdo_path", "save_path", "cam_list"]

    def __init__(self, parent=None, **kwargs):
        super(WThreadOutHdf5Window, self).__init__(parent)
        for attr in self.__class__.attributes:
            setattr(self, attr, kwargs.get(attr))

    def run(self):
        # check if all paths are valid
        if not os.path.exists(self.vdo_path):
            self.emit(QtCore.SIGNAL("show_warning"),
                      "vdo path is not valid!")
            return
        if not os.path.exists(self.save_path):
            self.emit(QtCore.SIGNAL("show_warning"), "save path is not valid!")
            return
        if not self.cam_list:
            self.emit(QtCore.SIGNAL("show_warning"), "No camera selected!")
            return
        res = self.vdo2h5(self.vdo_path)
        if res == 1:
            return
        self.emit(QtCore.SIGNAL("show_info"), "Done!")

    def vdo2h5(self, vdo_path):

        # check whether vdo exist
        vdos = glob.glob("{}/*.vdo".format(vdo_path))
        if not vdos:
            self.emit(QtCore.SIGNAL("show_warning"), "No VDO files found!")
            return 1
        # select the vdo files need to be processed
        arg_list = self.get_vdo_arg_list()
        if not arg_list:
            self.emit(QtCore.SIGNAL("show_warning"), "No vdo files selected!")
            return 1
        else:
            # check whether the selected vdo files exist in the vdo folder
            for i, val in enumerate(self.cam_list):
                vdos = glob.glob("{}/*{}.vdo".format(self.vdo_path, val))
                if not vdos:
                    self.emit(QtCore.SIGNAL("show_warning"),
                              "No vdo files for camera {}!".format(val))
                    return 1
            for i, val in enumerate(arg_list):
                VR.WriteCSV(val)
                self.emit(QtCore.SIGNAL("update_progressBar"))
            try:
                fn_evnt = r'{}/*.evnt.txt'.format(vdo_path)
                fn_s3db = r'{}/*.s3db'.format(vdo_path)
                fn_evnt = glob.glob(fn_evnt)
                fn_s3db = glob.glob(fn_s3db)
                files_copy = [fn_evnt[0], fn_s3db[0]]
                # print fn_evnt, fn_s3db
            except ValueError:
                print("event or s3db file(s) ... are missing!")
            evnt = re.split('/|\\\\', fn_evnt[0])[-1]
            run = re.split(r'\.(?!\d)', evnt)[0]

            try:
                for f in files_copy:
                    shutil.copy(f, run)
            except IOError:
                print("No external lbd lbe files copied!")

            current_folder_path, current_folder_name = os.path.split(
                os.getcwd())
            current_h5_dir = "{}/{}/{}".format(
                current_folder_path, current_folder_name, run)
            if os.path.exists(current_h5_dir):
                self.csv2h5(run)  # convert csv to h5
                if current_h5_dir != self.save_path:
                    des_folder = "{}/".format(self.save_path)
                    if not os.path.exists(des_folder):
                        os.makedirs(des_folder)
                    if not os.path.exists("{}/{}".format(des_folder, run)):
                        # move folder to target directory
                        shutil.move(current_h5_dir, des_folder)
                    else:
                        # h5 path and moving path are not the same
                        if os.path.abspath(current_h5_dir) != os.path.abspath("{}/{}".format(des_folder, run)):
                            # overwrite
                            try:
                                shutil.rmtree(os.path.abspath(
                                    "{}/{}".format(des_folder, run)))
                            except IOError:
                                print("Overwritten error occured!")
                            shutil.move(os.path.abspath(
                                current_h5_dir), os.path.abspath(des_folder))
                            print(
                                "Destination path already exists!\n Files are overwritten!")
                        else:
                            print(
                                "self - overwritten is not allowed!\n Files are saved in default(program) folder!")
            else:
                self.emit(QtCore.SIGNAL("show_warning"),
                          "Generated hdf5 folder does not exists!")
                return 1

        return run

    def get_vdo_arg_list(self):
        # get arg list for VR.WriteCSV function
        arg_list = []
        for i, val in enumerate(self.cam_list):
            arg_list.append(r"{}/*{}.vdo".format(self.vdo_path, val))
        return arg_list

    def csv2h5(self, dir):
        fn_csv = r"{}/*.csv".format(dir)
        fn_csv = glob.glob(fn_csv)
        for fn in fn_csv:
            recp = pd.read_csv(fn,
                               names=['Odometer', 'FrameNum'],
                               skiprows=2, delimiter=',')
            if recp.empty:
                continue
            fn_hdf = fn[:-3] + 'h5'
            h5_var = 'vdo'
            shuffle = True
            fletcher32 = True
            complib_h5py = 'gzip'
            complevel = 9
            import h5py
            reca = recp.to_records(index=False)
            with h5py.File(fn_hdf, 'w') as hfile:
                hfile.require_dataset(h5_var,
                                      shape=reca.shape,
                                      dtype=reca.dtype,
                                      data=reca,
                                      shuffle=shuffle,
                                      fletcher32=fletcher32,
                                      compression=complib_h5py,
                                      compression_opts=complevel,
                                      )
            os.remove(fn)


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
        self.ui.save_path.setText(os.getcwd())
        self.ui.out_h5_btn.clicked.connect(self.out_h5_btn_clicked)

    def reset_dialog_window(self):
        self.ui.out_h5_btn.setEnabled(True)
        self.ui.cancel_btn.setEnabled(False)
        self.ui.stop_btn.setEnabled(False)
        self.ui.progressBar.setValue(0)

    def show_info(self, message):
        super(OutHdf5Window, self).show_info(message)
        self.reset_dialog_window()

    def show_warning(self, message):
        super(OutHdf5Window, self).show_warning(message)
        self.reset_dialog_window()

    def get_selected_cams_list(self):
        # get selected camera IDs
        cam_list = []
        cam_ids = ["c50", "c51", "60", "61", "62",
                   "64", "65", "70", "71", "72", "74", "75"]
        for i, val in enumerate(cam_ids):
            cb_name = "checkBox_{}".format(val)
            if (getattr(self.ui, cb_name).isChecked()):
                cam_list.append(val)
        return cam_list

    def out_h5_btn_clicked(self):

        vdo_path = str(self.ui.vdo_path.text())
        save_path = str(self.ui.save_path.text())
        # get selected camera list
        cam_list = self.get_selected_cams_list()
        # create thread to do the processing
        self.get_thread = WThreadOutHdf5Window(
            vdo_path=vdo_path, save_path=save_path, cam_list=cam_list)
        # connect signals
        self.connect(self.get_thread, QtCore.SIGNAL(
            "show_info"), self.show_info)
        self.connect(self.get_thread, QtCore.SIGNAL(
            "show_warning"), self.show_warning)
        self.connect(self.get_thread, QtCore.SIGNAL(
            "reset_dialog_window"), self.reset_dialog_window)
        self.get_thread.start()
        self.ui.out_h5_btn.setEnabled(False)
        self.ui.cancel_btn.setEnabled(False)
        self.ui.stop_btn.setEnabled(True)
        self.ui.stop_btn.clicked.connect(self.get_thread.terminate)
