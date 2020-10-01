"""
Tests for the Music Player Client
"""
import jwt
from pathlib import Path
import random
import requests
import unittest

from player_tech_assignment.server.server import SECRET_KEY
from player_tech_assignment.csv_reader import MusicPlayerCsvReaderError
from player_tech_assignment.client import MusicPlayerClient, MusicPlayerClientError
from player_tech_assignment.cli import DEFAULT_BASE_URL

WORKING_DIR = Path.cwd()
TEST_DATA_DIR = WORKING_DIR / "tests" / "test_data"
TEST_CSV_FILE = TEST_DATA_DIR / "test_local_data.csv"


class TestClient(unittest.TestCase):
    """
    Test Music Player Client
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the Music Player Client
        """
        cls.client = MusicPlayerClient(DEFAULT_BASE_URL, "simon", "password")

    def test_invalid_client(self):
        """
        Test invalid Music Player Client base URL
        """
        with self.assertRaises(MusicPlayerClientError):
            MusicPlayerClient("http://127.0.0.1:5001", "simon", "password")

    def test_validate_mac_address(self):
        """
        Test Music Player Client MAC address validation
        """
        valid_mac_address = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                                         random.randint(0, 255),
                                                         random.randint(0, 255))
        # Invalid MAC addresses
        self.assertFalse(self.client._validate_mac_address("potato"))
        self.assertRaises(MusicPlayerClientError, self.client._validate_mac_address, random.randint(0, 1000))
        self.assertRaises(MusicPlayerClientError, self.client._validate_mac_address, False)

        # Valid MAC address
        self.assertTrue(self.client._validate_mac_address(valid_mac_address))

    def test_login(self):
        """
        Test Music Player Client login
        """
        # Invalid username and password combination
        invalid_client = MusicPlayerClient(DEFAULT_BASE_URL, "simon", "password123")
        self.assertRaises(MusicPlayerClientError, invalid_client.get_authentification_token_id)

        # Valid username and password combination
        token = self.client.get_authentification_token_id()
        self.assertIsInstance(token, str)
        jwt.decode(token, SECRET_KEY)

    def test_software_update_request(self):
        """
        Test Music Player Client software update request
        """
        random_valid_mac_address = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                                                random.randint(0, 255),
                                                                random.randint(0, 255))
        # Invalid token
        self.assertTrue(self.client._update_player(random_valid_mac_address, "aleatory").status_code == 404)

        # MAC address not in local MAC addresses list
        token = self.client.get_authentification_token_id()
        self.assertTrue(self.client._update_player("8F:1E:C8:64:8C:03", token).status_code == 401)

        # MAC address and token valid
        self.assertTrue(self.client._update_player("8F:1E:C8:64:8C:02", token).status_code == 200)

    def test_software_update(self):
        """
        Test Music Player Client software update
        """
        # Invalid csv file input
        self.assertRaises(MusicPlayerCsvReaderError, self.client.update_players, "charabia")
        self.assertRaises(MusicPlayerCsvReaderError, self.client.update_players, TEST_DATA_DIR / "test_invalid_extension.txt")

        # Valid csv file input
        self.client.update_players(TEST_CSV_FILE)


        # ------------------------- Scripts ---------------------------------#
if __name__ == '__main__':
    unittest.main()
