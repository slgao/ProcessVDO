from dialog_window import DialogWindow
import py_gui.output_hdf5 as outh5


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
