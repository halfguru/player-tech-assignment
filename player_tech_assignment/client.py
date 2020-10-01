"""
Music player client to the update server

Functionalities:
    1) GET /login request to get authentification token ID
    2) PUT /profiles/clientId:{macaddress} request to update the software version
"""
import os
import re
import requests

from .csv_reader import MusicPlayerCsvReader

__all__ = ['MusicPlayerClient', 'MusicPlayerClientError']


class MusicPlayerClientError(Exception):
    """
    Music Player Client Error
    """
    pass


class MusicPlayerClient():
    def __init__(self, base_url: str, username: str, password: str):
        """
        Music player client to make requests to the update server

        Args:
            base_url (str): client base URL
            username (str): login username
            password (str): login password
        """
        self._base_url = base_url
        self._username = username
        self._password = password

        # Validate base url home page is accessible
        try:
            requests.get(self._base_url)
        except requests.exceptions.ConnectionError:
            raise MusicPlayerClientError("Music player server is not accessible")

    @staticmethod
    def _validate_mac_address(mac_address: str) -> bool:
        """
        Validate MAC address format

        Args:
            mac_address (str): music player MAC address

        Returns:
            bool: True if MAC address is valid
        """
        if not isinstance(mac_address, str):
            raise MusicPlayerClientError("mac_address is of type {0} instead of {1}".format(type(mac_address), str))

        return re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac_address.lower())

    def _login(self):
        """ 
        Login to Music Player Server
        POST /login request

        Returns:
            Response: /login POST request response
        """
        url = '{0}/login'.format(self._base_url)
        json_data = {
            "username": self._username,
            "password": self._password
        }
        res = requests.post(url, data=json_data)
        return res

    def _update_player(self, mac_address, token):
        """
        Update the software version of a device with MAC address
        PUT /profiles/clientId:{macaddress} request

        Args:
            mac_address (str): music player MAC address
            token (str): authentification token

        Returns:
            Response: /profiles/clientId:{macaddress} PUT request response
        """
        url = '{0}/profiles/clientId:{1}?token={2}'.format(self._base_url, mac_address, token)
        json_data = {
            "profile": {
                "applications": [
                    {
                        "applicationId": "music_app",
                        "version": "v1.4.10"
                    },
                    {
                        "applicationId": "diagnostic_app",
                        "version": "v1.2.6"
                    },
                    {
                        "applicationId": "settings_app",
                        "version": "v1.1.5"
                    }
                ]
            }
        }
        res = requests.put(url, json=json_data)
        return res

    def get_authentification_token_id(self) -> str:
        """
        Get authentification ID

        Raises:
            MusicPlayerClientError: [description]

        Returns:
            str: token id
        """
        res = self._login()
        if res.status_code == 200:
            return res.json()["token"]
        else:
            raise MusicPlayerClientError("Could not get token because of invalid credentials")

    def update_players(self, csv_file: str):
        """
        Update music players from .csv configuration

        Args:
           csv_file (str): music player update file

        Raises:
            MusicPlayerClientError: Update player request not successful
        """
        reader = MusicPlayerCsvReader(csv_file)
        mac_address_list = reader.get_mac_address_list()

        for mac_address in mac_address_list:
            if not self._validate_mac_address(mac_address):
                raise MusicPlayerClientError("MAC address {0} format is not valid".format(mac_address))

            token = self.get_authentification_token_id()

            res = self._update_player(mac_address, token)
            if res.status_code != 200:
                raise MusicPlayerClientError("Error: {0}".format(res.text))
