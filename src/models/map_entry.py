class MapEntry:
    def __init__(self, entry_id: str, label: str):
        self.entry_id = entry_id
        self.label = label.lower().replace(" ", "_")  # Normalize to lowercase camel case

    def __repr__(self):
        return f"MapEntry(entry_id='{self.entry_id}', label='{self.label}')"

    def to_dict(self):
        return {
            "id": self.entry_id,
            "label": self.label
        }