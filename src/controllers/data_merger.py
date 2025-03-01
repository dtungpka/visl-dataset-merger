import os
import shutil
from utils.logger import get_logger
from utils.file_operations import copy_file, copy_folder

class DataMerger:
    def __init__(self):
        self.logger = get_logger()
        self.program_folders = []
        self.master_output_folder = None
        self.master_map = {}
        self.change_log = []
        
    def setup(self, program_folders, master_output_folder, master_map):
        """Set up the data merger with folders to process and output location"""
        self.program_folders = program_folders
        self.master_output_folder = master_output_folder
        self.master_map = master_map
        
        # Create master output folder if it doesn't exist
        os.makedirs(self.master_output_folder, exist_ok=True)
        os.makedirs(os.path.join(self.master_output_folder, 'output'), exist_ok=True)
        
        # Write master map file
        self._write_master_map()
        
        return True
        
    def merge(self, progress_callback=None):
        """Merge data from program folders to master folder"""
        if not self.program_folders or not self.master_output_folder:
            self.logger.log_error("Merge not properly set up. Missing folders or map.")
            return False
        
        total_actions = len(self.program_folders)
        completed_actions = 0
        
        try:
            # Process each program folder
            for folder in self.program_folders:
                self.logger.log_info(f"Processing folder: {folder}")
                
                # Get output folder
                output_folder = os.path.join(folder, 'output')
                if not os.path.exists(output_folder):
                    self.logger.log_warning(f"Output folder not found in {folder}")
                    continue
                
                # Get map file
                map_file = os.path.join(folder, 'config', 'maps.txt')
                if not os.path.exists(map_file):
                    map_file = os.path.join(folder, 'maps.txt')
                    if not os.path.exists(map_file):
                        self.logger.log_warning(f"Map file not found in {folder}")
                        continue
                
                # Load this folder's map
                folder_map = self._load_folder_map(map_file)
                
                # Process output subfolders
                for item in os.listdir(output_folder):
                    item_path = os.path.join(output_folder, item)
                    if os.path.isdir(item_path):
                        self._process_subfolder(item, item_path, folder_map)
                
                # Update progress
                completed_actions += 1
                if progress_callback:
                    progress_value = int((completed_actions / total_actions) * 100)
                    progress_callback(progress_value)
            
            self.logger.log_completion()
            return True
            
        except Exception as e:
            self.logger.log_error(f"Error during merge: {e}")
            return False
    
    def _load_folder_map(self, map_file):
        """Load a map file for a specific folder"""
        folder_map = {}
        try:
            with open(map_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    parts = line.split('=>')
                    if len(parts) == 2:
                        entry_id = parts[0].strip()
                        label = parts[1].strip()
                        folder_map[entry_id] = label
        except Exception as e:
            self.logger.log_error(f"Error loading map file {map_file}: {e}")
            
        return folder_map
    
    def _process_subfolder(self, subfolder_name, subfolder_path, folder_map):
        """Process an output subfolder"""
        # Example: A1P1
        try:
            # Extract action ID (e.g., 'A1')
            action_id = None
            for i in range(1, 100):  # Support up to A99
                if subfolder_name.startswith(f"A{i}P"):
                    action_id = f"A{i}"
                    break
            
            if not action_id or action_id not in folder_map:
                self.logger.log_warning(f"Could not find matching map entry for {subfolder_name}")
                return
            
            # Get the normalized label from master map
            original_label = folder_map[action_id]
            master_label = None
            master_id = None
            
            # Find corresponding entry in master map
            for mid, mlabel in self.master_map.items():
                if mlabel.lower() == original_label.lower():
                    master_label = mlabel
                    master_id = mid
                    break
            
            if not master_label:
                self.logger.log_warning(f"No matching label in master map for {original_label}")
                return
                
            # Create new output folder path using master label
            person_id = subfolder_name[len(action_id):]  # Extract person part (e.g., 'P1')
            new_subfolder_name = f"{master_id}{person_id}"
            new_subfolder_path = os.path.join(self.master_output_folder, 'output', new_subfolder_name)
            
            # Check if destination already exists
            if os.path.exists(new_subfolder_path):
                # Handle duplicate by appending a number to person ID
                base_person_id = person_id.rstrip('0123456789')
                person_num = int(person_id[len(base_person_id):] or 1)
                
                while os.path.exists(new_subfolder_path):
                    person_num += 1
                    new_subfolder_name = f"{master_id}{base_person_id}{person_num}"
                    new_subfolder_path = os.path.join(self.master_output_folder, 'output', new_subfolder_name)
                
                self.logger.log_info(f"Renamed subfolder {subfolder_name} to {new_subfolder_name} to avoid conflict")
            
            # Copy data to master output
            copy_folder(subfolder_path, new_subfolder_path)
            self.change_log.append(f"Copied {subfolder_path} to {new_subfolder_path}")
            
        except Exception as e:
            self.logger.log_error(f"Error processing subfolder {subfolder_name}: {e}")
    
    def _write_master_map(self):
        """Write the master map to a file in the master output folder"""
        try:
            map_file_path = os.path.join(self.master_output_folder, 'maps.txt')
            with open(map_file_path, 'w', encoding='utf-8') as f:
                for entry_id, label in self.master_map.items():
                    f.write(f"{entry_id} => {label}\n")
            
            self.logger.log_info(f"Wrote master map to {map_file_path}")
        except Exception as e:
            self.logger.log_error(f"Error writing master map: {e}")