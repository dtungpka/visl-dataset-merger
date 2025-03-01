def to_lower_camel_case(text):
    if not text:
        return ""
    
    words = text.split()
    return words[0].lower() + ''.join(word.capitalize() for word in words[1:])

def normalize_map_entry(entry):
    entry_id, label = entry.split('=>')
    normalized_label = to_lower_camel_case(label.strip())
    return entry_id.strip(), normalized_label

def remove_empty_entries(map_entries, output_folders):
    return {entry_id: label for entry_id, label in map_entries.items() if any(entry_id in folder for folder in output_folders)}