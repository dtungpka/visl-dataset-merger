import os
import unittest
from src.controllers.folder_scanner import FolderScanner

class TestFolderScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = FolderScanner()

    def test_find_program_folders(self):
        # Assuming we have a test directory structure set up
        test_directory = 'test_data'
        os.makedirs(os.path.join(test_directory, 'A1P1'), exist_ok=True)
        os.makedirs(os.path.join(test_directory, 'A2P1'), exist_ok=True)
        os.makedirs(os.path.join(test_directory, 'A1P2'), exist_ok=True)
        with open(os.path.join(test_directory, 'maps.txt'), 'w') as f:
            f.write("A1 => nha_lau\nA2 => nha_may_ngoi\n")

        found_folders = self.scanner.find_program_folders(test_directory)
        expected_folders = [
            os.path.join(test_directory, 'A1P1'),
            os.path.join(test_directory, 'A2P1'),
            os.path.join(test_directory, 'A1P2')
        ]

        self.assertEqual(sorted(found_folders), sorted(expected_folders))

    def test_invalid_folder(self):
        invalid_directory = 'invalid_data'
        found_folders = self.scanner.find_program_folders(invalid_directory)
        self.assertEqual(found_folders, [])

    def tearDown(self):
        # Clean up test directories
        test_directory = 'test_data'
        if os.path.exists(test_directory):
            for folder in os.listdir(test_directory):
                folder_path = os.path.join(test_directory, folder)
                if os.path.isdir(folder_path):
                    os.rmdir(folder_path)
            os.rmdir(test_directory)

if __name__ == '__main__':
    unittest.main()