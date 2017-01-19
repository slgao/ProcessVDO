import os
import glob
import re
import shutil
from PyQt4 import QtCore
import vdo
import py_gui.from_hdf5 as frhd5

from dialog_window import DialogWindow
__author__ = 'gao.shulin'


class Options(object):
    attributes = ['debug', 'use_cams',
                  'AbExtCounter', 'save', 'Jumping', 'FrameInfo'
                  ]

    def __init__(self, **kwargs):
        for attr in self.__class__.attributes:
            setattr(self, attr, kwargs.get(attr))


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
