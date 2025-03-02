import os
import unittest
import tempfile
import shutil
from src.controllers.folder_scanner import FolderScanner

class TestFolderScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = FolderScanner()
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        
    def test_scan(self):
        """Test the scan method finds properly structured program folders"""
        # Create proper folder structure for testing
        program_folder = os.path.join(self.test_dir, 'program1')
        os.makedirs(program_folder, exist_ok=True)
        
        # Create maps.txt
        maps_file = os.path.join(program_folder, 'maps.txt')
        with open(maps_file, 'w') as f:
            f.write("A1 => nha_lau\nA2 => nha_may_ngoi\n")
        
        # Create output folder with proper folder format
        output_folder = os.path.join(program_folder, 'output')
        os.makedirs(output_folder, exist_ok=True)
        os.makedirs(os.path.join(output_folder, 'A1P1'), exist_ok=True)
        os.makedirs(os.path.join(output_folder, 'A2P1'), exist_ok=True)
        
        # Test scanning works properly
        found_folders = self.scanner.scan(self.test_dir)
        self.assertEqual(len(found_folders), 1)
        self.assertEqual(found_folders[0], program_folder)

    def test_invalid_folder(self):
        """Test that scan correctly ignores invalid folders"""
        # Create folder without required structure
        invalid_folder = os.path.join(self.test_dir, 'invalid')
        os.makedirs(invalid_folder, exist_ok=True)
        
        # Test scanning returns empty list
        found_folders = self.scanner.scan(self.test_dir)
        self.assertEqual(found_folders, [])
        
    def test_no_output_data(self):
        """Test that folders with maps.txt but no output data are ignored"""
        # Create folder with maps.txt but no output data
        program_folder = os.path.join(self.test_dir, 'program2')
        os.makedirs(program_folder, exist_ok=True)
        
        # Create maps.txt
        maps_file = os.path.join(program_folder, 'maps.txt')
        with open(maps_file, 'w') as f:
            f.write("A1 => nha_lau\n")
        
        # Create empty output folder without proper content
        output_folder = os.path.join(program_folder, 'output')
        os.makedirs(output_folder, exist_ok=True)
        
        # Test scanning ignores folder with no valid output data
        found_folders = self.scanner.scan(self.test_dir)
        self.assertEqual(found_folders, [])

    def test_remove_empty_folders(self):
        """Test the remove_empty_folders method"""
        # Add some folders to the scanner
        program_folder1 = os.path.join(self.test_dir, 'program1')
        program_folder2 = os.path.join(self.test_dir, 'program2')
        
        os.makedirs(program_folder1, exist_ok=True)
        os.makedirs(program_folder2, exist_ok=True)
        
        # Create output with data in program1
        output_folder1 = os.path.join(program_folder1, 'output')
        os.makedirs(output_folder1, exist_ok=True)
        os.makedirs(os.path.join(output_folder1, 'A1P1'), exist_ok=True)
        
        # Create empty output in program2
        output_folder2 = os.path.join(program_folder2, 'output')
        os.makedirs(output_folder2, exist_ok=True)
        
        # Manually set program folders (since scan would filter them)
        self.scanner.program_folders = [program_folder1, program_folder2]
        
        # Test remove_empty_folders filters out empty folders
        valid_folders = self.scanner.remove_empty_folders()
        self.assertEqual(len(valid_folders), 1)
        self.assertEqual(valid_folders[0], program_folder1)

    def tearDown(self):
        # Clean up temporary directory
        shutil.rmtree(self.test_dir)

if __name__ == '__main__':
    unittest.main()