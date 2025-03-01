import unittest
from src.controllers.map_processor import MapProcessor

class TestMapProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = MapProcessor()

    def test_normalize_text(self):
        self.assertEqual(self.processor.normalize_text("Nhà Lầu"), "nhaLau")
        self.assertEqual(self.processor.normalize_text("NHA MAI NGOI"), "nhaMaiNgoi")
        self.assertEqual(self.processor.normalize_text("nha_rong"), "nhaRong")

    def test_remove_empty_entries(self):
        maps = {
            "A1": "nha_lau",
            "A2": "nha_may_ngoi",
            "A3": "",
            "A4": "nha_san"
        }
        output_folders = ["A1P1", "A2P1"]
        processed_maps = self.processor.remove_empty_entries(maps, output_folders)
        expected_maps = {
            "A1": "nha_lau",
            "A2": "nha_may_ngoi"
        }
        self.assertEqual(processed_maps, expected_maps)

    def test_conflict_resolution(self):
        maps = {
            "A1": "nha_lau",
            "A2": "nha_lau"
        }
        resolved_maps = self.processor.resolve_conflicts(maps)
        self.assertIn("A1", resolved_maps)
        self.assertIn("A2_new", resolved_maps)

    def test_process_maps(self):
        maps = {
            "A1": "nha_lau",
            "A2": "nha_may_ngoi"
        }
        output_folders = ["A1P1", "A2P1"]
        processed_maps = self.processor.process_maps(maps, output_folders)
        self.assertEqual(len(processed_maps), 2)

if __name__ == '__main__':
    unittest.main()