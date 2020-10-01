"""
Music Player .csv file reader
"""
import csv
from pathlib import Path
from typing import List

__all__ = ['MusicPlayerCsvReader', 'MusicPlayerCsvReaderError']


CSV_FILE_SUFFIX = ".csv"
CSV_FILE_MAC_ADDRESS_COLUMN_NAME = "mac_addresses"
CSV_FILE_ID1_COLUMN_NAME = "id1"
CSV_FILE_ID2_COLUMN_NAME = "id2"
CSV_FILE_ID3_COLUMN_NAME = "id3"


class MusicPlayerCsvReaderError(Exception):
    """
    Music Player Csv Reader Error
    """
    pass


class MusicPlayerCsvReader:
    def __init__(self, csv_file):
        """
        Music Player .csv file reader

        Args:
            csv_file (str): music player update file

        Raises:
            MusicPlayerCsvReaderError: csv file not found or wrong extension
        """
        self._csv_file_dict = {}
        self._csv_file_dict["mac_addresses"] = []
        self._csv_file_dict["id1"] = []
        self._csv_file_dict["id2"] = []
        self._csv_file_dict["id3"] = []
        self._csv_file = Path(csv_file)
        if not self._csv_file.is_file():
            raise MusicPlayerCsvReaderError("{0} file not found".format(csv_file))
        if self._csv_file.suffix != CSV_FILE_SUFFIX:
            raise MusicPlayerCsvReaderError("{0} file doesn't contain a {1} extension".format(csv_file, CSV_FILE_SUFFIX))
        self.read()

    def read(self):
        """
        Read CSV file and extract data

        Raises:
            MusicPlayerCsvReaderError: invalid csv file content 
        """
        with open(self._csv_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            line_count = 0
            for rows in reader:
                # Verify column name
                if line_count == 0:
                    if CSV_FILE_MAC_ADDRESS_COLUMN_NAME not in rows[0]:
                        raise MusicPlayerCsvReaderError("{0} file wrong mac address column name".format(self._csv_file))
                    elif CSV_FILE_ID1_COLUMN_NAME not in rows[1]:
                        raise MusicPlayerCsvReaderError("{0} file wrong id1 column name".format(self._csv_file))
                    elif CSV_FILE_ID2_COLUMN_NAME not in rows[2]:
                        raise MusicPlayerCsvReaderError("{0} file wrong id2 column name".format(self._csv_file))
                    elif CSV_FILE_ID3_COLUMN_NAME not in rows[3]:
                        raise MusicPlayerCsvReaderError("{0} file wrong id3 column name".format(self._csv_file))

                if line_count != 0:
                    if not rows[0] or not rows[1] or not rows[2] or not rows[3]:
                        raise MusicPlayerCsvReaderError("{0} has empty elements".format(self._csv_file))
                    self._csv_file_dict["mac_addresses"].append(rows[0].replace(",", ""))
                    self._csv_file_dict["id1"].append(rows[1])
                    self._csv_file_dict["id2"].append(rows[2])
                    self._csv_file_dict["id3"].append(rows[3])
                line_count += 1

    def get_mac_address_list(self) -> List:
        return self._csv_file_dict["mac_addresses"]
