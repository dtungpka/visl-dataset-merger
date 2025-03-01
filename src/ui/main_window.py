from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QMessageBox, QVBoxLayout, 
                            QWidget, QPushButton, QListWidget, QLabel, QProgressBar,
                            QHBoxLayout, QListWidgetItem, QCheckBox, QSplitter, QMenuBar, QAction)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from controllers.folder_scanner import FolderScanner
from controllers.map_processor import MapProcessor
from controllers.data_merger import DataMerger
from ui.conflict_dialog import ConflictDialog
from ui.progress_dialog import ProgressDialog
from ui.about_dialog import AboutDialog
from utils.logger import get_logger
import os
from utils.constants import APP_VERSION
class WorkerThread(QThread):
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, data_merger):
        super().__init__()
        self.data_merger = data_merger
        
    def run(self):
        try:
            success = self.data_merger.merge(progress_callback=self.update_progress)
            self.finished.emit(success, "" if success else "Merge failed")
        except Exception as e:
            self.finished.emit(False, str(e))
            
    def update_progress(self, value):
        self.progress_updated.emit(value)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Dataset Merger v{APP_VERSION}")
        self.setGeometry(100, 100, 800, 600)
        
        self.logger = get_logger()
        self.folder_scanner = FolderScanner()
        self.map_processor = MapProcessor()
        self.data_merger = DataMerger()
        
        self.program_folders = []
        self.folder_maps = {}
        self.conflicts = {}
        self.master_map = {}
        
        self.initUI()
        
    def initUI(self):
        # Add menu bar
        self.create_menu_bar()
        
        main_layout = QVBoxLayout()
        
        # Splitter for two panels
        splitter = QSplitter(Qt.Vertical)
        
        # Top panel - folder selection
        top_panel = QWidget()
        top_layout = QVBoxLayout(top_panel)
        
        folder_header = QLabel("<b>Program Folders</b>")
        top_layout.addWidget(folder_header)
        
        self.folder_list = QListWidget()
        top_layout.addWidget(self.folder_list)
        
        folder_buttons = QHBoxLayout()
        self.find_button = QPushButton("Find Program Folders")
        self.find_button.clicked.connect(self.find_program_folders)
        folder_buttons.addWidget(self.find_button)
        
        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.clicked.connect(self.remove_selected_folder)
        folder_buttons.addWidget(self.remove_button)
        
        top_layout.addLayout(folder_buttons)
        
        # Bottom panel - conflicts/maps
        bottom_panel = QWidget()
        bottom_layout = QVBoxLayout(bottom_panel)
        
        maps_header = QLabel("<b>Maps and Conflicts</b>")
        bottom_layout.addWidget(maps_header)
        
        self.maps_list = QListWidget()
        bottom_layout.addWidget(self.maps_list)
        
        map_buttons = QHBoxLayout()
        self.process_maps_button = QPushButton("Process Maps")
        self.process_maps_button.clicked.connect(self.process_maps)
        map_buttons.addWidget(self.process_maps_button)
        
        self.resolve_conflicts_button = QPushButton("Resolve Conflicts")
        self.resolve_conflicts_button.clicked.connect(self.show_conflicts_dialog)
        self.resolve_conflicts_button.setEnabled(False)
        map_buttons.addWidget(self.resolve_conflicts_button)
        
        bottom_layout.addLayout(map_buttons)
        
        # Add panels to splitter
        splitter.addWidget(top_panel)
        splitter.addWidget(bottom_panel)
        main_layout.addWidget(splitter)
        
        # Bottom controls
        bottom_controls = QHBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        bottom_controls.addWidget(self.progress_bar)
        
        self.merge_button = QPushButton("Start Merge")
        self.merge_button.clicked.connect(self.start_merge)
        self.merge_button.setEnabled(False)
        bottom_controls.addWidget(self.merge_button)
        
        main_layout.addLayout(bottom_controls)
        
        # Set main widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        
    def create_menu_bar(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        
        # File menu
        file_menu = menu_bar.addMenu("File")
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
    
    def show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.exec_()
        
    def find_program_folders(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Root Directory")
        if not folder_path:
            return
            
        self.logger.log_info(f"Scanning for program folders in: {folder_path}")
        
        # Show dialog that scan is in progress
        QMessageBox.information(self, "Scanning", "Scanning for program folders, please wait...")
        
        # Scan for program folders
        found_folders = self.folder_scanner.scan(folder_path)
        
        # Update UI
        self.program_folders = found_folders
        self.update_folder_list()
        
        if not found_folders:
            QMessageBox.warning(self, "No Folders Found", "No valid program folders were found in the selected directory.")
    
    def update_folder_list(self):
        self.folder_list.clear()
        for folder in self.program_folders:
            item = QListWidgetItem(folder)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked)
            self.folder_list.addItem(item)
    
    def remove_selected_folder(self):
        selected_items = self.folder_list.selectedItems()
        if not selected_items:
            return
            
        for item in selected_items:
            folder = item.text()
            self.program_folders.remove(folder)
            self.logger.log_info(f"Removed folder: {folder}")
            
        self.update_folder_list()
    
    def process_maps(self):
        if not self.program_folders:
            QMessageBox.warning(self, "No Folders", "Please select program folders first.")
            return
            
        # Get checked folders only
        checked_folders = []
        for i in range(self.folder_list.count()):
            item = self.folder_list.item(i)
            if item.checkState() == Qt.Checked:
                checked_folders.append(item.text())
        
        if not checked_folders:
            QMessageBox.warning(self, "No Folders Selected", "Please select at least one program folder.")
            return
        
        # Process maps
        result = self.map_processor.process_maps(checked_folders)
        self.folder_maps = result["maps"]
        self.conflicts = result["conflicts"]
        
        # Update maps list
        self.maps_list.clear()
        
        # Add header for maps
        self.maps_list.addItem("--- Maps ---")
        
        # Display maps
        for folder, maps in self.folder_maps.items():
            folder_name = os.path.basename(folder)
            self.maps_list.addItem(f"Folder: {folder_name}")
            for entry_id, label in maps.items():
                self.maps_list.addItem(f"  {entry_id} => {label}")
        
        # Add header for conflicts
        if self.conflicts:
            self.maps_list.addItem("--- Conflicts ---")
            for conflict_key, conflict_items in self.conflicts.items():
                self.maps_list.addItem(f"Conflict: {conflict_key}")
                for item in conflict_items:
                    if "id" in item:
                        folder_name = os.path.basename(item["folder"])
                        self.maps_list.addItem(f"  {folder_name}: ID {item['id']} conflicts with {item['conflicting_id']}")
                    elif "label" in item:
                        folder_name = os.path.basename(item["folder"])
                        self.maps_list.addItem(f"  {folder_name}: Label {item['label']} conflicts with {item['conflicting_label']}")
            
            self.resolve_conflicts_button.setEnabled(True)
        else:
            self.maps_list.addItem("No conflicts found")
            self.master_map = self._create_master_map()
            self.merge_button.setEnabled(True)
    
    def show_conflicts_dialog(self):
        if not self.conflicts:
            return
            
        # Convert conflicts to simple list for dialog
        conflict_list = []
        for conflict_key, items in self.conflicts.items():
            conflict_list.append(f"Conflict: {conflict_key}")
            for item in items:
                if "id" in item:
                    folder_name = os.path.basename(item["folder"])
                    conflict_list.append(f"  {folder_name}: ID {item['id']} conflicts with {item['conflicting_id']}")
                elif "label" in item:
                    folder_name = os.path.basename(item["folder"])
                    conflict_list.append(f"  {folder_name}: Label {item['label']} conflicts with {item['conflicting_label']}")
        
        dialog = ConflictDialog(conflict_list, self)
        result = dialog.exec_()
        
        if result == QDialog.Accepted:
            action = dialog.get_selected_action()
            selected_items = dialog.conflict_list.selectedItems()
            
            if not selected_items:
                return
                
            # Get selected conflict
            selected_text = selected_items[0].text()
            
            # Handle conflict resolution based on action
            if action == "keep":
                QMessageBox.information(self, "Action", f"Keep as main: {selected_text}")
                # TODO: Implement actual conflict resolution
            elif action == "new_entry":
                QMessageBox.information(self, "Action", f"Set as new entry: {selected_text}")
                # TODO: Implement actual conflict resolution
            elif action == "delete":
                QMessageBox.information(self, "Action", f"Delete entry: {selected_text}")
                # TODO: Implement actual conflict resolution
            
            # For now, pretend conflicts are resolved
            self.conflicts = {}
            self.master_map = self._create_master_map()
            self.merge_button.setEnabled(True)
    
    def _create_master_map(self):
        """Create a master map from the folder maps (simplistic approach for now)"""
        master_map = {}
        
        # Combine all maps (this is simplistic, conflicts should be properly resolved)
        for folder, maps in self.folder_maps.items():
            for entry_id, label in maps.items():
                # Simple strategy: just use the first encountered entry for each label
                reversed_map = {v: k for k, v in master_map.items()}
                if label not in reversed_map:
                    master_map[entry_id] = label
        
        return master_map
    
    def start_merge(self):
        if not self.master_map:
            QMessageBox.warning(self, "No Maps", "Please process maps first.")
            return
        
        # Select output folder
        output_folder = QFileDialog.getExistingDirectory(self, "Select Master Output Folder")
        if not output_folder:
            return
        
        # Setup data merger
        checked_folders = []
        for i in range(self.folder_list.count()):
            item = self.folder_list.item(i)
            if item.checkState() == Qt.Checked:
                checked_folders.append(item.text())
        
        self.data_merger.setup(checked_folders, output_folder, self.master_map)
        
        # Create progress dialog
        progress_dialog = ProgressDialog(self)
        progress_dialog.show()
        
        # Create worker thread
        self.worker = WorkerThread(self.data_merger)
        self.worker.progress_updated.connect(progress_dialog.update_progress)
        self.worker.finished.connect(self.merge_completed)
        self.worker.finished.connect(progress_dialog.close_dialog)
        self.worker.start()
    
    def merge_completed(self, success, error_message):
        if success:
            QMessageBox.information(self, "Success", "Data merging completed successfully!")
        else:
            QMessageBox.critical(self, "Error", f"An error occurred: {error_message}")