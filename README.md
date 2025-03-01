# Dataset Merger

## Overview
The Dataset Merger is a Python application built with PyQt5 that facilitates the merging of datasets collected from various machines. The application allows users to select multiple program folders, process their associated `maps.txt` files, and consolidate the output data into a master dataset. This tool is particularly useful for managing data collected in different environments where labeling conventions may vary.

## Features
- **Folder Selection**: Users can choose multiple program folders containing the necessary `maps.txt` file and output data.
- **Map Processing**: The application normalizes map entries to a consistent format and removes entries without corresponding data.
- **Conflict Resolution**: Users are prompted to resolve any conflicting map entries through a user-friendly dialog.
- **Data Merging**: The application merges data from selected program folders into a master output folder, renaming subfolders as necessary to avoid duplicates.
- **Progress Tracking**: A progress bar provides real-time feedback during the merging process.
- **Logging**: All changes and actions are logged for debugging and rollback purposes.

## Installation
To install the Dataset Merger, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd dataset-merger
pip install -r requirements.txt
```

## Usage
1. Run the application:
   ```bash
   python src/main.py
   ```
2. Use the interface to select the program folders you wish to merge.
3. Review and modify the detected program folders as needed.
4. Process the `maps.txt` files to normalize entries and resolve conflicts.
5. Start the merging process and monitor progress through the progress dialog.
6. Upon completion, a master `maps.txt` file and output folder will be created in the specified destination.

## Contributing
Contributions to the Dataset Merger are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.