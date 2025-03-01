from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QPushButton

class ProgressDialog(QDialog):
    def __init__(self, parent=None):
        super(ProgressDialog, self).__init__(parent)
        self.setWindowTitle("Merging Data")
        self.setFixedSize(300, 150)

        self.layout = QVBoxLayout()
        self.label = QLabel("Merging data, please wait...")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.progress_bar)

        self.setLayout(self.layout)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def set_message(self, message):
        self.label.setText(message)

    def close_dialog(self):
        self.accept()