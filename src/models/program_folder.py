class ProgramFolder:
    def __init__(self, path):
        self.path = path
        self.maps = {}
        self.output_data = []

    def load_maps(self, maps_file):
        try:
            with open(maps_file, 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip():
                        entry_id, label = line.strip().split('=>')
                        self.maps[entry_id.strip()] = label.strip().lower()
        except Exception as e:
            print(f"Error loading maps from {maps_file}: {e}")

    def collect_output_data(self):
        import os
        if os.path.exists(self.path):
            for subfolder in os.listdir(self.path):
                if os.path.isdir(os.path.join(self.path, subfolder)):
                    self.output_data.append(subfolder)

    def normalize_maps(self):
        normalized_maps = {}
        for entry_id, label in self.maps.items():
            normalized_label = self.to_lower_camel_case(label)
            normalized_maps[entry_id] = normalized_label
        self.maps = normalized_maps

    @staticmethod
    def to_lower_camel_case(text):
        words = text.split('_')
        return ''.join(word.capitalize() if i > 0 else word.lower() for i, word in enumerate(words))

    def get_maps(self):
        return self.maps

    def get_output_data(self):
        return self.output_data

    def __repr__(self):
        return f"ProgramFolder(path={self.path}, maps={self.maps}, output_data={self.output_data})"