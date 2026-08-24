import unittest
import tempfile
from pathlib import Path
import pandas as pd
from unittest.mock import MagicMock
from controllers.views.msic_profile_controller import MSICProfileController

CSV = """ref,MSIC
A,0.45
T,-0.82
G,0.15
C,-0.34
A,0.78
T,-0.12
G,0.91
C,-0.65
A,0.22
T,-0.49
G,0.08
C,-0.73"""

GBK_WITH_BOTH = """LOCUS       TEST_REC1                 12 bp    DNA     linear   SYN 01-JAN-2024
FEATURES             Location/Qualifiers
     gene            1..12
                     /gene="testGene"
ORIGIN
        1 atgcatgcat gc
"""

GBK_NO_FEATURES = """LOCUS       TEST_REC2                 12 bp    DNA     linear   SYN 01-JAN-2024
ORIGIN
        1 atgcatgcat gc
"""

GBK_NO_SEQUENCE = """LOCUS       TEST_REC3                 12 bp    DNA     linear   SYN 01-JAN-2024
FEATURES             Location/Qualifiers
     gene            1..12
                     /gene="testGene"
ORIGIN
//"""

GBK_INVALID = """LOCUS       TEST_REC3                 12 bp    DNA     linear   SYN 01-JAN-2024
FEATURES             Location/Qualifiers
     gene            1..12
                     /gene="testGene"
//"""

GBK_NON_MATCHING = """LOCUS       TEST_REC1                 12 bp    DNA     linear   SYN 01-JAN-2024
FEATURES             Location/Qualifiers
     gene            1..12
                     /gene="testGene"
ORIGIN
        1 atgcgtgcat gc
"""

class TestCSVImportMenuController(unittest.TestCase):
    
    def setUp(self):
            main_ctrl = MagicMock()
            self.controller = MSICProfileController(main_ctrl)
            self.controller.view = MagicMock()
            self.controller.main_ctrl = MagicMock()
            self.controller.main_ctrl.height_quo = 1
            
            self.temp_dir = tempfile.TemporaryDirectory()
            self.csv_path = Path(self.temp_dir.name) / "test_data.csv"
            self.csv_path.write_text(CSV)
            self.df = pd.read_csv(self.csv_path)
            self.addCleanup(self.temp_dir.cleanup)
            
    def _create_gbk(self, content):
        path = Path(self.temp_dir.name) / "test.gb"
        path.write_text(content)
        return path
            
    def test_get_plot_success(self):
        self.controller.get_plot(df=self.df, csv_path=str(self.csv_path), genbank_file=str(self._create_gbk(GBK_WITH_BOTH)))
        self.controller.view.show_no_sequence_error.assert_not_called()
        self.controller.view.show_no_features_error.assert_not_called()
        self.controller.view.show_invalid_genbank_error.assert_not_called()
        self.controller.view.show_non_matching_error.assert_not_called()
        
    def test_get_plot_failure_no_features(self):
        self.controller.get_plot(df=self.df, csv_path=str(self.csv_path), genbank_file=str(self._create_gbk(GBK_NO_FEATURES)))
        self.controller.view.show_no_sequence_error.assert_not_called()
        self.controller.view.show_no_features_error.assert_called_once()
        self.controller.view.show_invalid_genbank_error.assert_not_called()
        self.controller.view.show_non_matching_error.assert_not_called()
        
    def test_get_plot_failure_no_sequence(self):
        self.controller.get_plot(df=self.df, csv_path=str(self.csv_path), genbank_file=str(self._create_gbk(GBK_NO_SEQUENCE)))
        self.controller.view.show_no_sequence_error.assert_called_once()
        self.controller.view.show_no_features_error.assert_not_called()
        self.controller.view.show_invalid_genbank_error.assert_not_called()
        self.controller.view.show_non_matching_error.assert_not_called()
        
    def test_get_plot_failure_invalid_gbk(self):
        self.controller.get_plot(df=self.df, csv_path=str(self.csv_path), genbank_file=str(self._create_gbk(GBK_INVALID)))
        self.controller.view.show_no_sequence_error.assert_not_called()
        self.controller.view.show_no_features_error.assert_not_called()
        self.controller.view.show_invalid_genbank_error.assert_called_once()
        self.controller.view.show_non_matching_error.assert_not_called()
        
    def test_get_plot_failure_non_matching(self):
        self.controller.get_plot(df=self.df, csv_path=str(self.csv_path), genbank_file=str(self._create_gbk(GBK_NON_MATCHING)))
        self.controller.view.show_no_sequence_error.assert_not_called()
        self.controller.view.show_no_features_error.assert_not_called()
        self.controller.view.show_invalid_genbank_error.assert_not_called()
        self.controller.view.show_non_matching_error.assert_called_once()