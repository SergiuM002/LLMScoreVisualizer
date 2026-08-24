import unittest
from unittest.mock import MagicMock, patch, mock_open
from controllers.views.csv_import_menu_controller import CSVImportMenuController

class TestCSVImportMenuController(unittest.TestCase):
    
    def setUp(self):
        main_ctrl = MagicMock()
        self.controller = CSVImportMenuController(main_ctrl)
        self.controller.view = MagicMock()
        
    def test_add_csv_new_file_success(self):
        self.controller._valid_columns = MagicMock(return_value=(True, ""))
        self.controller._msic_in_range = MagicMock(return_value=True)
        self.controller._valid_nucleotides = MagicMock(return_value=True)
        
        self.assertTrue(self.controller.add_csv("mock_valid.csv"))
        self.assertIn("mock_valid.csv", self.controller.csv_files)
        self.controller.view.pack_csv_button.assert_called_once()
        self.controller.view.show_already_imported_error.assert_not_called()
        
    def test_add_csv_new_file_failure_already_imported(self):
        self.controller._valid_columns = MagicMock(return_value=(True, ""))
        self.controller._msic_in_range = MagicMock(return_value=True)
        self.controller._valid_nucleotides = MagicMock(return_value=True)
                
        self.controller.csv_files = ["mock_duplicate.csv"]
        
        self.assertFalse(self.controller.add_csv("mock_duplicate.csv"))
        self.assertIn("mock_duplicate.csv", self.controller.csv_files)
        self.controller.view.pack_csv_button.assert_not_called()
        self.controller.view.show_already_imported_error.assert_called_once()
        
    def test_add_csv_new_file_failure_invalid_file_extension(self):
        self.controller._valid_columns = MagicMock(return_value=(True, ""))
        self.controller._msic_in_range = MagicMock(return_value=True)
        self.controller._valid_nucleotides = MagicMock(return_value=True)
        
        self.assertFalse(self.controller.add_csv("mock_duplicate.cdv"))
        self.controller.view.pack_csv_button.assert_not_called()
        self.controller.view.show_invalid_file_extension_error.assert_called_once()    
        
    @patch("builtins.open", new_callable=mock_open, read_data="ref,MSIC\nt,0.99\nc,-0.99")
    def test_msic_in_range_success(self, mock_file):
        self.assertTrue(self.controller._msic_in_range("mock_valid.csv"))

    @patch("builtins.open", new_callable=mock_open, read_data="ref,MSIC\nt,0.99\nc,-1.01")
    def test_msic_in_range_failure(self, mock_file):
        self.assertFalse(self.controller._msic_in_range("mock_valid.csv"))
        
    @patch("builtins.open", new_callable=mock_open, read_data="ref,MSIC\na,0.92\nc,-0.79\ng,0.2\nt,-0.5")
    def test_valid_nucleotides_success(self, mock_file):
        self.assertTrue(self.controller._valid_nucleotides("mock_valid.csv"))

    @patch("builtins.open", new_callable=mock_open, read_data="ref,MSIC\nt,0.99\np,-0.01")
    def test_valid_nucleotides_success(self, mock_file):
        self.assertFalse(self.controller._valid_nucleotides("mock_valid.csv"))
        
    @patch("builtins.open", new_callable=mock_open, read_data="ref,MSIC\nt,0.99\np,-0.7")
    def test_valid_columns_success(self, mock_file):
        self.assertTrue(self.controller._valid_columns("mock_valid.csv"))
        
    @patch("builtins.open", new_callable=mock_open, read_data="ref,MDIC\nt,0.99\np,-0.31")
    def test_valid_columns_failure_no_msic(self, mock_file):
        self.assertEqual(self.controller._valid_columns("mock_valid.csv"), (False, "MSIC"))
        
    @patch("builtins.open", new_callable=mock_open, read_data="resf,MSIC\nt,0.99\np,-0.31")
    def test_valid_columns_failure_no_ref(self, mock_file):
        self.assertEqual(self.controller._valid_columns("mock_valid.csv"), (False, "ref"))
        
if __name__ == "__main__":
    unittest.main()