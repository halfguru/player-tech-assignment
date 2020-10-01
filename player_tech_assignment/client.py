"""
Music player client to the update server
"""

import os
import re
import requests

__all__ = ['MusicPlayerClient', 'MusicPlayerClientError']


class MusicPlayerClientError(Exception):
    """
    Music Player Client Error
    """
    pass


class MusicPlayerClient():
    def __init__(self, base_url: str):
        """
        Music player client

        Args:
            base_url (str): client base URL
        """
        self._base_url = base_url
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

    def update_player(self, mac_address: str, token: str) -> str:
        """
        Request to update a music player with MAC address

        Args:
            mac_address (str): music player MAC address
            token (str): authentification token id

        Returns:
            str: request

        Raises:
            MusicPlayerClientError: MAC address is not valid
        """
        if not self._validate_mac_address(mac_address):
            raise MusicPlayerClientError("MAC address format is not valid")

        if not token:
            raise MusicPlayerClientError("Token is not defined")

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

    def login(self, username: str, password: str) -> str:
        """ 
        Login and get authentification token ID

        Args:
            username (str): login username
            password (str): login password

        Returns:
            str: token id
        """
        url = '{0}/login'.format(self._base_url)
        json_data = {
            "username": username,
            "password": password
        }
        res = requests.post(url, data=json_data)
        if res.status_code == 200:
            return res.json()["token"]
        else:
            raise MusicPlayerClientError("Could not get token because of invalid credentials")
