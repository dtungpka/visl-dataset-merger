import os
from utils.logger import get_logger
from utils.text_normalizer import to_lower_camel_case, normalize_map_entry, remove_empty_entries

class MapProcessor:
    def __init__(self):
        self.logger = get_logger()
        self.master_map = {}
        self.conflicts = {}
    
    def process_maps(self, program_folders):
        """Process maps.txt from all program folders"""
        self.logger.log_info("Starting map processing")
        folder_maps = {}
        
        # First, load and normalize all maps
        for folder in program_folders:
            map_file_path = os.path.join(folder, 'config', 'maps.txt')
            
            if not os.path.exists(map_file_path):
                map_file_path = os.path.join(folder, 'maps.txt')
                if not os.path.exists(map_file_path):
                    self.logger.log_warning(f"No maps.txt found in {folder}")
                    continue
            
            output_folder = os.path.join(folder, 'output')
            output_subfolders = os.listdir(output_folder) if os.path.exists(output_folder) else []
            
            folder_maps[folder] = self._load_map_file(map_file_path, output_subfolders)
            
        # Identify and collect conflicts
        self._identify_conflicts(folder_maps)
        
        return {
            "maps": folder_maps,
            "conflicts": self.conflicts
        }
    
    def _load_map_file(self, map_file_path, output_subfolders):
        """Load and normalize map entries from a file"""
        map_entries = {}
        
        try:
            with open(map_file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        entry_id, label = normalize_map_entry(line)
                        
                        # Check if this entry has associated output data
                        has_data = any(subfolder.startswith(entry_id) for subfolder in output_subfolders)
                        
                        if has_data:
                            map_entries[entry_id] = label
                            self.logger.log_debug(f"Loaded map entry: {entry_id} => {label}")
                    except Exception as e:
                        self.logger.log_warning(f"Could not parse map entry: {line}. Error: {e}")
            
            return map_entries
        except Exception as e:
            self.logger.log_error(f"Error loading map file {map_file_path}: {e}")
            return {}
    
    def _identify_conflicts(self, folder_maps):
        """Identify conflicts between map entries from different folders"""
        # Track labels and their associated IDs across all folders
        label_id_map = {}
        id_label_map = {}
        
        for folder, maps in folder_maps.items():
            for entry_id, label in maps.items():
                # Check if this label already exists with a different ID
                if label in label_id_map and label_id_map[label] != entry_id:
                    conflict_id = label_id_map[label]
                    if label not in self.conflicts:
                        self.conflicts[label] = []
                    
                    conflict_entry = {
                        "folder": folder,
                        "id": entry_id,
                        "conflicting_id": conflict_id
                    }
                    self.conflicts[label].append(conflict_entry)
                    self.logger.log_warning(f"Conflict detected: {entry_id} and {conflict_id} both map to {label}")
                
                # Check if this ID already exists with a different label
                if entry_id in id_label_map and id_label_map[entry_id] != label:
                    conflict_label = id_label_map[entry_id]
                    if entry_id not in self.conflicts:
                        self.conflicts[entry_id] = []
                    
                    conflict_entry = {
                        "folder": folder,
                        "label": label,
                        "conflicting_label": conflict_label
                    }
                    self.conflicts[entry_id].append(conflict_entry)
                    self.logger.log_warning(f"Conflict detected: {entry_id} maps to both {label} and {conflict_label}")
                
                # Update tracking maps
                label_id_map[label] = entry_id
                id_label_map[entry_id] = label
        
        return self.conflicts
    
    def resolve_conflict(self, conflict_type, conflict_key, resolution_action, resolution_data):
        """Resolve a conflict with the specified action"""
        self.logger.log_info(f"Resolving conflict for {conflict_type} '{conflict_key}' with action {resolution_action}")
        
        # Resolution actions: keep_main, new_entry, delete
        if resolution_action == "keep_main":
            # Keep one entry as main, update others
            pass
        elif resolution_action == "new_entry":
            # Create a new entry for the conflicting item
            pass
        elif resolution_action == "delete":
            # Delete the conflicting entry
            pass
            
        self.logger.log_conflict_resolution(f"{conflict_type} '{conflict_key}': {resolution_action}")
        
        return True
    
    def generate_master_map(self, folder_maps, resolved_conflicts):
        """Generate a master map from all folder maps, applying conflict resolutions"""
        master_map = {}
        
        # Apply conflict resolutions
        for folder, maps in folder_maps.items():
            for entry_id, label in maps.items():
                # Check if this entry was part of a resolved conflict
                # If not, add it to master map
                if entry_id not in resolved_conflicts and label not in resolved_conflicts:
                    master_map[entry_id] = label
        
        # Add conflict resolutions to master map
        for resolution in resolved_conflicts:
            if resolution['action'] == 'keep_main':
                master_map[resolution['id']] = resolution['label']
            elif resolution['action'] == 'new_entry':
                master_map[resolution['new_id']] = resolution['label']
        
        return master_map