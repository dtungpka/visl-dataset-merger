import unittest
from src.controllers.data_merger import DataMerger
from src.models.program_folder import ProgramFolder
from src.models.map_entry import MapEntry

class TestDataMerger(unittest.TestCase):

    def setUp(self):
        self.program_folders = [
            ProgramFolder(path='folder1', maps=[MapEntry(id='A1', label='nha_lau')], output_data=['A1P1']),
            ProgramFolder(path='folder2', maps=[MapEntry(id='A2', label='nha_may_ngoi')], output_data=['A2P1']),
            ProgramFolder(path='folder3', maps=[MapEntry(id='A1', label='nha_lau')], output_data=['A1P2']),
        ]
        self.master_folder = 'master_folder'
        self.data_merger = DataMerger(self.program_folders, self.master_folder)

    def test_merge_data_no_conflicts(self):
        self.data_merger.merge_data()
        self.assertEqual(len(self.data_merger.master_maps), 2)
        self.assertIn('nha_lau', self.data_merger.master_maps)
        self.assertIn('nha_may_ngoi', self.data_merger.master_maps)

    def test_merge_data_with_conflicts(self):
        self.program_folders[0].maps.append(MapEntry(id='A1', label='nha_lau'))
        self.data_merger.merge_data()
        self.assertEqual(len(self.data_merger.master_maps), 2)
        self.assertIn('nha_lau', self.data_merger.master_maps)
        self.assertEqual(self.data_merger.master_maps['nha_lau'], 'A1')

    def test_rename_subfolders(self):
        self.data_merger.rename_subfolders()
        self.assertEqual(self.data_merger.renamed_subfolders, ['folder1/A1P1', 'folder2/A2P1', 'folder3/A1P2'])

    def test_log_changes(self):
        self.data_merger.log_changes('Test log entry')
        self.assertIn('Test log entry', self.data_merger.change_log)

if __name__ == '__main__':
    unittest.main()