from PyQt5 import QtCore

from PyQt5.QtGui import QImage, QPixmap, QPalette, QIcon
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QAction, \
    QFileDialog

from PIL import Image
from PIL.ImageQt import ImageQt


class BaseViewer(QMainWindow):
    zoom_request = QtCore.pyqtSignal(int, QtCore.QPoint)

    def connect_and_emit_trigger(self):
        # Connect the trigger signal to a slot.
        self.zoom_request.connect(self.wheel_event)

        # Emit the signal.
        self.zoom_request.emit()

    def __init__(self):
        super().__init__()

        self.original_image = None
        self.current_image = None
        self.previous_processed_images = []

        self.toolbar = self.addToolBar('Toolbar')
        self.create_toolbar()

        self.create_actions()
        self.create_menus()

        self.scale_factor = 0.0

        self.image_label = QLabel()
        self.image_label.setBackgroundRole(QPalette.Base)
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.image_label.setScaledContents(True)

        self.scroll_area = QScrollArea()
        self.scroll_area.setBackgroundRole(QPalette.Dark)
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setVisible(False)

        self.setCentralWidget(self.scroll_area)   

        self.setWindowTitle("Image Viewer")
        self.resize(800, 600)

    def create_toolbar(self):
        open_action = QAction(QIcon('./icons/open-512.png'), 'Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open)

        self.toolbar.addAction(open_action)

    ##############
    # Image
    ##############

    def update_image(self):
        image = QImage(ImageQt(self.current_image))

        self.image_label.setPixmap(QPixmap.fromImage(image))
        self.scale_factor = 1.0

        self.scroll_area.setVisible(True)
        self.fit_to_window_action.setEnabled(True)
        self.update_size_actions()

        if not self.fit_to_window_action.isChecked():
            self.image_label.adjustSize()

    ##############
    # Actions
    ##############

    def create_actions(self):
        self.open_action = QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.open)
        self.exit_action = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.zoom_in_action = QAction("Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.zoom_in)
        self.zoom_out_action = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.zoom_out)
        self.original_action = QAction("&Original Size", self, shortcut="Ctrl+B", enabled=False, triggered=self.original)
        self.fit_to_window_action = QAction("&Fit to Window", self, enabled=False, checkable=True, shortcut="Ctrl+F", triggered=self.fit_to_window)
        self.about_action = QAction("&About", self, triggered=self.about)

    def open(self):
        options = QFileDialog.Options()

        filename, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if filename:
            self.original_image = Image.open(filename)
            self.current_image = self.original_image.copy()

            self.update_image()

    def about(self):
        QMessageBox.about(self, "About Image Viewer",
                          "<p>A simple processing tool, where you can try several image processing techniques on your image. </p>")

    ##############
    # Image size
    ##############

    def zoom_in(self):
        self.scale_image(1.25)

    def zoom_out(self):
        self.scale_image(0.8)

    def original(self):
        self.image_label.adjustSize()
        self.scale_factor = 1.0

    def fit_to_window(self):
        fit_to_window_flag = self.fit_to_window_action.isChecked()
        self.scroll_area.setWidgetResizable(fit_to_window_flag)
        if not fit_to_window_flag:
            self.original()

        self.update_size_actions()

    def update_size_actions(self):
        self.zoom_in_action.setEnabled(not self.fit_to_window_action.isChecked())
        self.zoom_out_action.setEnabled(not self.fit_to_window_action.isChecked())
        self.original_action.setEnabled(not self.fit_to_window_action.isChecked())

    def scale_image(self, factor):
        self.scale_factor *= factor
        self.image_label.resize(self.scale_factor * self.image_label.pixmap().size())

        self.adjust_scroll_bar(self.scroll_area.horizontalScrollBar(), factor)
        self.adjust_scroll_bar(self.scroll_area.verticalScrollBar(), factor)

        self.zoom_in_action.setEnabled(self.scale_factor < 3.0)
        self.zoom_out_action.setEnabled(self.scale_factor > 0.333)

    def adjust_scroll_bar(self, scroll_bar, factor):
        scroll_bar.setValue(int(factor * scroll_bar.value() + ((factor - 1) * scroll_bar.pageStep() / 2)))

    ##############
    # Menus
    ##############

    def create_menus(self):
        self.file_menu = QMenu("&File", self)
        self.file_menu.addAction(self.open_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)

        self.view_menu = QMenu("&View", self)
        self.view_menu.addAction(self.zoom_in_action)
        self.view_menu.addAction(self.zoom_out_action)
        self.view_menu.addAction(self.original_action)
        self.view_menu.addSeparator()
        self.view_menu.addAction(self.fit_to_window_action)

        self.help_menu = QMenu("&Help", self)
        self.help_menu.addAction(self.about_action)

        self.menuBar().addMenu(self.file_menu)
        self.menuBar().addMenu(self.view_menu)

        self.create_additional_menus()

        self.menuBar().addMenu(self.help_menu)
        
    def create_additional_menus(self):
        pass

    ##############
    # Event
    ##############

    def wheel_event(self, ev):
        mods = ev.modifiers()
        delta = ev.angleDelta()
            
        if QtCore.Qt.ControlModifier == int(mods):
            # with Ctrl/Command key
            # zoom
            self.zoomRequest.emit(delta.y(), ev.pos())
        else:
            # scroll
            self.scrollRequest.emit(delta.x(), QtCore.Qt.Horizontal)
            self.scrollRequest.emit(delta.y(), QtCore.Qt.Vertical)
        
        ev.accept()
