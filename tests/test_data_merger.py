import unittest
import os
import shutil
import tempfile
from src.controllers.data_merger import DataMerger

class TestDataMerger(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        
        # Create test folder structure
        self.program_folders = [
            os.path.join(self.test_dir, 'folder1'),
            os.path.join(self.test_dir, 'folder2'),
            os.path.join(self.test_dir, 'folder3')
        ]
        
        self.master_folder = os.path.join(self.test_dir, 'master_folder')
        os.makedirs(self.master_folder, exist_ok=True)
        
        # Create basic structure in each program folder
        for folder in self.program_folders:
            os.makedirs(os.path.join(folder, 'output'), exist_ok=True)
            os.makedirs(os.path.join(folder, 'config'), exist_ok=True)
            
            # Create maps.txt file
            with open(os.path.join(folder, 'config', 'maps.txt'), 'w') as f:
                if 'folder1' in folder:
                    f.write('A1 => nha_lau\n')
                elif 'folder2' in folder:
                    f.write('A2 => nha_may_ngoi\n')
                elif 'folder3' in folder:
                    f.write('A1 => nha_lau\n')
                    
            # Create sample output folders
            if 'folder1' in folder:
                os.makedirs(os.path.join(folder, 'output', 'A1P1'), exist_ok=True)
            elif 'folder2' in folder:
                os.makedirs(os.path.join(folder, 'output', 'A2P1'), exist_ok=True)
            elif 'folder3' in folder:
                os.makedirs(os.path.join(folder, 'output', 'A1P2'), exist_ok=True)
        
        # Initialize DataMerger
        self.data_merger = DataMerger()
        
        # Create a sample master map
        self.master_map = {
            'A1': 'nha_lau',
            'A2': 'nha_may_ngoi'
        }

    def tearDown(self):
        # Clean up temporary directory
        shutil.rmtree(self.test_dir)

    def test_setup(self):
        """Test if setup correctly initializes the merger"""
        result = self.data_merger.setup(self.program_folders, self.master_folder, self.master_map)
        self.assertTrue(result)
        self.assertEqual(self.data_merger.program_folders, self.program_folders)
        self.assertEqual(self.data_merger.master_output_folder, self.master_folder)
        self.assertEqual(self.data_merger.master_map, self.master_map)
        
        # Check if master maps.txt was created
        self.assertTrue(os.path.exists(os.path.join(self.master_folder, 'maps.txt')))

    def test_merge(self):
        """Test basic merge functionality"""
        self.data_merger.setup(self.program_folders, self.master_folder, self.master_map)
        
        # Create a simple progress callback for testing
        def progress_callback(value):
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 100)
            
        result = self.data_merger.merge(progress_callback)
        self.assertTrue(result)
        
        # Check if change log has entries
        self.assertGreater(len(self.data_merger.change_log), 0)
        
        # Check if output folders were created in master folder
        master_output_dir = os.path.join(self.master_folder, 'output')
        self.assertTrue(os.path.exists(master_output_dir))
        # There should be at least one subfolder
        self.assertGreater(len(os.listdir(master_output_dir)), 0)

if __name__ == '__main__':
    unittest.main()