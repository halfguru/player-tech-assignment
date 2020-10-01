"""
Tests for the Music Player .csv file reader
"""
from pathlib import Path
import unittest

from player_tech_assignment.csv_reader import MusicPlayerCsvReader, MusicPlayerCsvReaderError

WORKING_DIR = Path.cwd()
TEST_DATA_DIR = WORKING_DIR / "tests" / "test_data"
TEST_CSV_FILE = TEST_DATA_DIR / "test_local_data.csv"


class TestCsv(unittest.TestCase):
    """
    Test Music Player .csv reader
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the Music Player Client
        """
        cls.reader = MusicPlayerCsvReader(TEST_CSV_FILE)

    def test_reader(self):
        """
        Test Music Player Reader .csv file
        """
        # .csv file wrong data or format
        with self.assertRaisesRegex(MusicPlayerCsvReaderError, "file not found"):
            MusicPlayerCsvReader(TEST_DATA_DIR / "mate")
        with self.assertRaisesRegex(MusicPlayerCsvReaderError, "file doesn't contain a .csv extension"):
            MusicPlayerCsvReader(TEST_DATA_DIR / "test_invalid_extension.txt")
        with self.assertRaisesRegex(MusicPlayerCsvReaderError, "file wrong mac address column name"):
            MusicPlayerCsvReader(TEST_DATA_DIR / "test_invalid_input.csv")

        # valid .csv file
        MusicPlayerCsvReader(TEST_DATA_DIR / "test_local_data.csv")

        # ------------------------- Scripts ---------------------------------#
if __name__ == '__main__':
    unittest.main()
