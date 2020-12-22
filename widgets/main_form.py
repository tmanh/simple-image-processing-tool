from PyQt5.QtWidgets import QAction, QMenu

from widgets.base_form import BaseViewer
from widgets.threshold import ThresholdDialog


class ImageViewer(BaseViewer):
    def __init__(self):
        super(ImageViewer, self).__init__()

    def create_toolbar(self):
        super(ImageViewer, self).create_toolbar()

    def create_additional_menus(self):
        threshold_action = QAction("&Threshold...", self, triggered=self.threshold)
        
        self.image_menu = QMenu("&Image", self)
        self.image_menu.setDisabled(True)
        self.image_menu.addAction(threshold_action)

        self.menuBar().addMenu(self.image_menu)

    def threshold(self):
        dlg = ThresholdDialog(self.current_image, self)
        print(dlg.get_results())

    def open(self):
        super().open()

        if self.current_image is not None:
            self.image_menu.setEnabled(True)
