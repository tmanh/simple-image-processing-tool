from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QImage, QPalette, QPixmap
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QGroupBox, QLabel, QRadioButton, QSizePolicy, QSpinBox, QVBoxLayout


# TODO: add preview

class ThresholdDialog(QDialog):
    def __init__(self, image, *args, **kwargs):
        super(ThresholdDialog, self).__init__(*args, **kwargs)

        self.original_image = image
        self.current_image = image.copy()

        self.setWindowTitle("Threshold image")

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.controls_group = QGroupBox('Threshold values');

        self.hsv_mode = QRadioButton('HSV')
        self.rgb_mode = QRadioButton('RGB')

        self.label_channel_1 = QLabel('')
        self.label_channel_2 = QLabel('')
        self.label_channel_3 = QLabel('')

        self.spin_box_channel_1 = QSpinBox()
        self.spin_box_channel_1.setAccelerated(True)
        self.spin_box_channel_1.setSingleStep(1)

        self.spin_box_channel_2 = QSpinBox()
        self.spin_box_channel_2.setAccelerated(True)
        self.spin_box_channel_2.setSingleStep(1)

        self.spin_box_channel_3 = QSpinBox()
        self.spin_box_channel_3.setAccelerated(True)
        self.spin_box_channel_3.setSingleStep(1)

        controls_layout = QGridLayout()
        controls_layout.addWidget(self.rgb_mode, 0, 0);
        controls_layout.addWidget(self.hsv_mode, 0, 1);
        controls_layout.addWidget(self.label_channel_1, 1, 0);
        controls_layout.addWidget(self.label_channel_2, 2, 0);
        controls_layout.addWidget(self.label_channel_3, 3, 0);
        controls_layout.addWidget(self.spin_box_channel_1, 1, 1);
        controls_layout.addWidget(self.spin_box_channel_2, 2, 1);
        controls_layout.addWidget(self.spin_box_channel_3, 3, 1);

        self.controls_group.setLayout(controls_layout);

        self.rgb_mode.toggled.connect(self.rgb_settings)
        self.hsv_mode.toggled.connect(self.hsv_settings)
        self.rgb_settings(True)

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.image_label = QLabel()
        self.image_label.setBackgroundRole(QPalette.Base)
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.image_label.setScaledContents(False)

        image = QImage(ImageQt(self.current_image))
        self.image_label.setPixmap(QPixmap.fromImage(image))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.controls_group)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def get_results(self):
        if self.exec_() == QDialog.Accepted:
            return 0, 1
        else:
            return None

    def rgb_settings(self, checked):
        self.rgb_mode.setChecked(checked)
        self.hsv_mode.setChecked(False)

        self.label_channel_1.setText('Red: ')
        self.label_channel_2.setText('Green: ')
        self.label_channel_3.setText('Blue: ')
        
        self.spin_box_channel_1.setRange(0, 255)
        self.spin_box_channel_2.setRange(0, 255)
        self.spin_box_channel_3.setRange(0, 255)

    def hsv_settings(self, checked):
        self.rgb_mode.setChecked(False)
        self.hsv_mode.setChecked(checked)

        self.label_channel_1.setText('Hue: ')
        self.label_channel_2.setText('Saturation: ')
        self.label_channel_3.setText('Value: ')
        
        self.spin_box_channel_1.setRange(0, 179)
        self.spin_box_channel_2.setRange(0, 255)
        self.spin_box_channel_3.setRange(0, 255)

    def preview(self):
        pass
