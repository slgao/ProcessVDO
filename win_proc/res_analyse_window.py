import py_gui.resolution_analyse as ra
from win_proc.fh5_window import FH5Window
from win_proc.fromVDO_window import FromVDOWindow
from PyQt4 import QtGui


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
