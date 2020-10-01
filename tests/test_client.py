"""
Tests for the Music Player Client
"""
import random
import requests
import unittest

from player_tech_assignment.client import MusicPlayerClient, MusicPlayerClientError
from player_tech_assignment.cli import DEFAULT_BASE_URL


class TestClient(unittest.TestCase):
    """
    Test Music Player Client
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the Music Player Client
        """
        cls.client = MusicPlayerClient(DEFAULT_BASE_URL)

    def test_invalid_client(self):
        """
        Test invalid Music Player Client base URL
        """
        with self.assertRaises(MusicPlayerClientError):
            MusicPlayerClient("http://127.0.0.1:5001")

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
        self.assertRaises(TypeError, self.client.login)
        self.assertRaises(TypeError, self.client.login, username="potato")
        self.assertRaises(TypeError, self.client.login, password="pepe")
        self.assertRaises(MusicPlayerClientError, self.client.login, "username", "random")

        # Valid username and password combination
        token = self.client.login(username="username", password="password")
        self.assertIsInstance(token, str)
        self.assertTrue(token)

    def test_update(self):
        random_valid_mac_address = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                                                random.randint(0, 255),
                                                                random.randint(0, 255))
        # Invalid function parameters
        self.assertRaises(TypeError, self.client.update_player, "charabia")
        self.assertRaises(TypeError, self.client.update_player, random_valid_mac_address)
        self.assertRaises(MusicPlayerClientError, self.client.update_player, "asdf", "token")

        # Invalid token
        self.assertTrue(self.client.update_player(random_valid_mac_address, "aleatory").status_code == 404)

        # MAC address not in local MAC addresses list
        token = self.client.login(username="username", password="password")
        self.assertTrue(self.client.update_player("8F:1E:C8:64:8C:03", token).status_code == 401)

        # MAC address and token valid
        self.assertTrue(self.client.update_player("8F:1E:C8:64:8C:02", token).status_code == 200)

        # ------------------------- Scripts ---------------------------------#
if __name__ == '__main__':
    unittest.main()
