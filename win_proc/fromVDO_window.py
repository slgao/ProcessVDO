from dialog_window import DialogWindow
import py_gui.from_vdo as frvdo


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
