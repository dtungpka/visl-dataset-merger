import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from ui.main_window import MainWindow
from utils.logger import setup_logger

def main():
    # Set up logging
    setup_logger()

    # Create the Qt application
    app = QApplication(sys.argv)
    
    # Set application icon
    icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                           "resources", "logo.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # Create and show the main window
    main_window = MainWindow()
    main_window.show()

    # Start the event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()