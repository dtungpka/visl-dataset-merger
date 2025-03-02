import os
import shutil
from utils.logger import get_logger

class FolderScanner:
    def __init__(self):
        self.program_folders = []
        self.logger = get_logger()

    def scan(self, root_directory):
        """Scan a directory to find program folders with maps.txt and output folder"""
        self.logger.log_directory_scan(root_directory)
        self.program_folders = []
        
        try:
            for root, dirs, files in os.walk(root_directory):
                # Check if this is a program folder
                if 'output' in dirs and os.path.exists(os.path.join(root,'config', 'maps.txt')):
                    maps_path = os.path.join(root, 'config', 'maps.txt')
                    output_path = os.path.join(root, 'output')
                    
                    # Verify output folder has content in AnPm format
                    if os.path.exists(output_path) and os.listdir(output_path):
                        for item in os.listdir(output_path):
                            # Check if folder name follows AnPm pattern
                            if os.path.isdir(os.path.join(output_path, item)) and any(item.startswith(f"A{i}P") for i in range(1, 100)):
                                self.program_folders.append(root)
                                self.logger.log_info(f"Found program folder: {root}")
                                break
            
            return self.program_folders
        except Exception as e:
            self.logger.log_error(f"Error scanning directories: {e}")
            return []

    def get_program_folders(self):
        return self.program_folders

    def remove_empty_folders(self):
        """Remove program folders that don't have data"""
        valid_folders = []
        for folder in self.program_folders:
            output_path = os.path.join(folder, 'output')
            if os.path.exists(output_path) and any(os.listdir(output_path)):
                valid_folders.append(folder)
            else:
                self.logger.log_info(f"Removing empty folder: {folder}")
                
        self.program_folders = valid_folders
        return self.program_folders