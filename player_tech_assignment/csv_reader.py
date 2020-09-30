"""
Music Player .csv file reader
"""
import csv
from pathlib import Path

CSV_FILE_SUFFIX = ".csv"
CSV_FILE_MAC_ADDRESS_COLUMN_NAME = "mac_addresses"
CSV_FILE_ID1_COLUMN_NAME = "id1"
CSV_FILE_ID2_COLUMN_NAME = "id2"
CSV_FILE_ID3_COLUMN_NAME = "id3"

class MusicPlayerCsvReaderException(Exception):
    """
    Music Player Csv Reader Exception
    """
    pass

class MusicPlayerCsvReader:
    def __init__(self, csv_file):
        """
        Music Player .csv file reader

        Args:
            csv_file (str): music player update file
        """
        self._csv_file_dict = {}
        self._csv_file_dict["mac_addresses"] = []
        self._csv_file_dict["id1"] = []
        self._csv_file_dict["id2"] = []
        self._csv_file_dict["id3"] = []
        self._csv_file = Path(csv_file)
        if not self._csv_file.is_file():
            raise MusicPlayerCsvReaderException("{0} file not found".format(csv_file))
        if self._csv_file.suffix != CSV_FILE_SUFFIX:
            raise MusicPlayerCsvReaderException("{0} file doesn't contain a {1} extension".format(csv_file, CSV_FILE_SUFFIX))
        self.read()

    def read(self):
        with open(self._csv_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            line_count = 0
            for rows in reader:
                # Verify column name
                if line_count == 0:
                    if CSV_FILE_MAC_ADDRESS_COLUMN_NAME not in rows[0]:
                        raise MusicPlayerCsvReaderException("{0} file wrong mac address column name")
                    elif CSV_FILE_ID1_COLUMN_NAME not in rows[1]:
                        raise MusicPlayerCsvReaderException("{0} file wrong id1 column name")
                    elif CSV_FILE_ID2_COLUMN_NAME not in rows[2]:
                        raise MusicPlayerCsvReaderException("{0} file wrong id2 column name")
                    elif CSV_FILE_ID3_COLUMN_NAME not in rows[3]:
                        raise MusicPlayerCsvReaderException("{0} file wrong id3 column name")

                if line_count != 0:
                    if not rows[0] or not rows[1] or not rows[2] or not rows[3]:
                         raise MusicPlayerCsvReaderException("{0} has empty elements")
                    self._csv_file_dict["mac_addresses"].append(rows[0])
                    self._csv_file_dict["id1"].append(rows[1])
                    self._csv_file_dict["id2"].append(rows[2])
                    self._csv_file_dict["id3"].append(rows[3])
                line_count += 1


    def get_mac_address(self):
        return self._csv_file_dict["mac_addresses"]

