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
        self.folder_maps = {}  # Store folder maps as instance variable
        
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
            
            self.folder_maps[folder] = self._load_map_file(map_file_path, output_subfolders)
            
        # Identify and collect conflicts
        self._identify_conflicts(self.folder_maps)
        
        return {
            "maps": self.folder_maps,
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
        """
        Resolve a conflict with the specified action
        
        Args:
            conflict_type: 'label' or 'id' indicating the type of conflict
            conflict_key: The conflicting key (label or ID)
            resolution_action: 'keep_main', 'new_entry', or 'delete'
            resolution_data: Additional data for resolution (e.g. which entry to keep)
        
        Returns:
            bool: True if conflict resolved successfully
        """
        self.logger.log_info(f"Resolving conflict for {conflict_type} '{conflict_key}' with action {resolution_action}")
        
        if conflict_key not in self.conflicts:
            self.logger.log_error(f"Conflict {conflict_key} not found")
            return False
            
        conflict_entries = self.conflicts[conflict_key]
        
        # Resolution actions
        if resolution_action == "keep_main":
            # Keep one entry as main, remove others from conflicts
            main_entry = resolution_data.get('main_entry')
            if not main_entry or not isinstance(main_entry, dict):
                self.logger.log_error("Invalid main entry data for keep_main action")
                return False
                
            # Record which entry we're keeping
            self.logger.log_info(f"Keeping entry from folder {main_entry.get('folder')} as main")
            
            # Remove this conflict from the list
            del self.conflicts[conflict_key]
            
        elif resolution_action == "new_entry":
            # Create a new entry for the conflicting item
            new_id = resolution_data.get('new_id')
            if not new_id:
                self.logger.log_error("No new ID provided for new_entry action")
                return False
                
            # Update the entry with new ID
            folder = resolution_data.get('folder')
            if not folder:
                self.logger.log_error("No folder specified for new_entry action")
                return False
                
            # Update the folder maps (needs to be passed in separately or stored in the class)
            if hasattr(self, 'folder_maps') and folder in self.folder_maps:
                if conflict_type == 'label':
                    # Find the entry with this label and update its ID
                    for entry in conflict_entries:
                        if entry.get('folder') == folder:
                            old_id = entry.get('id')
                            if old_id in self.folder_maps[folder]:
                                label = self.folder_maps[folder][old_id]
                                del self.folder_maps[folder][old_id]
                                self.folder_maps[folder][new_id] = label
                                self.logger.log_info(f"Updated ID from {old_id} to {new_id} for label {label}")
                elif conflict_type == 'id':
                    # This is an ID conflict, so it's the same ID with different labels
                    # Create new ID for this folder's mapping
                    old_label = resolution_data.get('label')
                    if old_label and conflict_key in self.folder_maps[folder]:
                        self.folder_maps[folder][new_id] = old_label
                        del self.folder_maps[folder][conflict_key]
                        self.logger.log_info(f"Created new ID {new_id} for label {old_label}")
            
            # Remove this conflict from the list
            del self.conflicts[conflict_key]
            
        elif resolution_action == "delete":
            # Delete the conflicting entry
            folder = resolution_data.get('folder')
            if not folder:
                self.logger.log_error("No folder specified for delete action")
                return False
                
            # Find and remove entry from folder maps
            if hasattr(self, 'folder_maps') and folder in self.folder_maps:
                if conflict_type == 'label':
                    for entry in conflict_entries:
                        if entry.get('folder') == folder:
                            entry_id = entry.get('id')
                            if entry_id in self.folder_maps[folder]:
                                del self.folder_maps[folder][entry_id]
                                self.logger.log_info(f"Deleted entry {entry_id} => {conflict_key} from folder {folder}")
                elif conflict_type == 'id':
                    if conflict_key in self.folder_maps[folder]:
                        del self.folder_maps[folder][conflict_key]
                        self.logger.log_info(f"Deleted entry {conflict_key} from folder {folder}")
            
            # If all conflicts for this key are resolved, remove the conflict
            remaining_conflicts = [entry for entry in conflict_entries 
                                  if entry.get('folder') != folder]
            
            if not remaining_conflicts:
                del self.conflicts[conflict_key]
            else:
                self.conflicts[conflict_key] = remaining_conflicts
        
        else:
            self.logger.log_error(f"Unknown resolution action: {resolution_action}")
            return False
            
        self.logger.log_conflict_resolution(f"{conflict_type} '{conflict_key}': {resolution_action}")
        return True
    
    def generate_master_map(self, resolved_conflicts=None):
        """Generate a master map from all folder maps, applying conflict resolutions"""
        master_map = {}
        resolved_conflicts = resolved_conflicts or []
        
        # Track which entries have been added to master map
        processed_entries = set()
        
        # Apply conflict resolutions first
        for resolution in resolved_conflicts:
            if resolution['action'] == 'keep_main':
                master_map[resolution['id']] = resolution['label']
                processed_entries.add(resolution['id'])
                processed_entries.add(resolution['label'])
            elif resolution['action'] == 'new_entry':
                master_map[resolution['new_id']] = resolution['label']
                processed_entries.add(resolution['new_id'])
                processed_entries.add(resolution['label'])
        
        # Add non-conflicting entries from folder maps
        for folder, maps in self.folder_maps.items():
            for entry_id, label in maps.items():
                # Skip entries that were part of resolved conflicts
                if entry_id in processed_entries or label in processed_entries:
                    continue
                    
                # Handle any remaining conflicts with a simple strategy
                if entry_id in master_map and master_map[entry_id] != label:
                    # ID exists with different label - skip
                    self.logger.log_warning(f"Skipping conflicting entry: {entry_id} => {label}")
                    continue
                    
                # Check if this label exists with different ID
                reverse_map = {v: k for k, v in master_map.items()}
                if label in reverse_map and reverse_map[label] != entry_id:
                    # Label exists with different ID - skip
                    self.logger.log_warning(f"Skipping duplicate label: {entry_id} => {label}")
                    continue
                    
                # No conflicts, add to master map
                master_map[entry_id] = label
        
        self.master_map = master_map
        return master_map

    def has_unresolved_conflicts(self):
        """Check if there are any unresolved conflicts"""
        return len(self.conflicts) > 0

    def get_conflict_count(self):
        """Get the number of unresolved conflicts"""
        return len(self.conflicts)

    def get_conflicts(self):
        """Get all current conflicts"""
        return self.conflicts