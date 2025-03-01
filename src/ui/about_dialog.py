from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import os
from utils.constants import APP_VERSION

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Dataset Merger")
        self.setFixedSize(500, 250)
        
        # Main layout
        main_layout = QHBoxLayout()
        
        # Left side - Logo
        logo_layout = QVBoxLayout()
        logo_label = QLabel()
        
        # Get the path to the logo file
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                "resources", "logo.png")
        
        # If logo exists, load it, otherwise show a text placeholder
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        else:
            logo_label.setText("Dataset\nMerger")
            logo_label.setFont(QFont("Arial", 24, QFont.Bold))
            logo_label.setAlignment(Qt.AlignCenter)
        
        logo_layout.addWidget(logo_label)
        logo_layout.setAlignment(Qt.AlignCenter)
        main_layout.addLayout(logo_layout)
        
        # Right side - Info
        info_layout = QVBoxLayout()
        
        # App name
        app_name_label = QLabel("Dataset Merger")
        app_name_label.setFont(QFont("Arial", 16, QFont.Bold))
        info_layout.addWidget(app_name_label)
        
        # Version
        version_label = QLabel(f"Version {APP_VERSION}")
        info_layout.addWidget(version_label)
        
        # Description
        desc_label = QLabel(
            "A Qt5 application for merging datasets from multiple program folders."
        )
        desc_label.setWordWrap(True)
        info_layout.addWidget(desc_label)
        
        # Spacer
        info_layout.addStretch()
        
        # Contact info
        contact_label = QLabel("Created by: dtungpka")
        info_layout.addWidget(contact_label)
        
        github_label = QLabel("<a href='https://github.com/dtungpka'>github.com/dtungpka</a>")
        github_label.setOpenExternalLinks(True)
        info_layout.addWidget(github_label)
        
        # Credit
        credit_label = QLabel("With the help of Claude 3.7 Sonnet")
        info_layout.addWidget(credit_label)
        
        # Close button
        button_layout = QHBoxLayout()
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        info_layout.addLayout(button_layout)
        
        main_layout.addLayout(info_layout)
        self.setLayout(main_layout)