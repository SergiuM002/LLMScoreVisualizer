import unittest
from unittest.mock import MagicMock
from controllers.views.genbank_selection_controller import GenbankSelectionController

class TestCSVImportMenuController(unittest.TestCase):
    
    def setUp(self):
        main_ctrl = MagicMock()
        self.controller = GenbankSelectionController(main_ctrl)
        self.controller.view = MagicMock()
        
    def test_add_genbank_new_file_success(self):
        c = 0
        
        for file_extension in [".gb", ".gbk", ".gbff"]:
            c += 1
            self.assertTrue(self.controller.add_genbank(f"mock_valid{file_extension}"))
            self.assertIn(f"mock_valid{file_extension}", self.controller.genbank_files)
            self.assertEqual(self.controller.view.pack_genbank_button.call_count, c)
            
    def test_add_genbank_new_file_failure_already_imported(self):
        self.controller.genbank_files = ["mock_duplicate.gb"]
        
        self.assertFalse(self.controller.add_genbank(f"mock_duplicate.gb"))    
        self.controller.view.show_already_imported_error.assert_called_once()
        
    def test_add_genbank_new_file_failure_invalid_file_extension(self):
        self.assertFalse(self.controller.add_genbank(f"mock_invalid.gbw"))    
        self.controller.view.show_invalid_file_extension_error.assert_called_once()
        
if __name__ == "__main__":
    unittest.main() 