"""
Music player update simulation server
"""

import datetime
from functools import wraps
from flask import Flask, render_template, make_response, jsonify, request, session
import jwt
from pathlib import Path
import os
import sys

from ..csv_reader import MusicPlayerCsvReader

__all__ = ['MusicPlayerUpdateServer', 'SECRET_KEY']

SECRET_KEY = 'playerTechAssignment'
WORKING_DIR = Path.cwd()
VALID_CLIENT_CSV_FILE = WORKING_DIR / "tests" / "test_data" / "test_local_data.csv"


class MusicPlayerUpdateServer:
    """
    Music player software update simulated server
    """

    def __init__(self):
        self._app = Flask(__name__)
        self._app.config['SECRET_KEY'] = SECRET_KEY
        self._app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
        self._app.add_url_rule('/', view_func=self.home)

        # Connects a URL rule
        self._app.add_url_rule('/get', endpoint="view", methods=['GET'], view_func=self.view)
        self._app.add_url_rule('/profiles/clientId:<string:macaddress>', endpoint="hook", methods=['PUT'], view_func=self.update)
        self._app.add_url_rule('/login', endpoint="login", methods=['POST'], view_func=self.login)

    def check_for_token(func):
        """
        Verify authentification token

        Args:
            func: Function prototype

        Returns:
            func: Function prototype
        """
        @wraps(func)
        def wrapped(*args, **kwargs):
            token = request.args.get('token')
            if not token:
                return jsonify({'message': 'Missing token'}), 403
            try:
                jwt.decode(token, SECRET_KEY)
            except jwt.exceptions.ExpiredSignatureError:
                return jsonify({'message': 'Token expired'}), 403
            except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.DecodeError):
                return jsonify({'message': 'profile of client {0} does not exist'.format(token)}), 404
            return func(*args, **kwargs)
        return wrapped

    @property
    def app(self):
        """
        Returns:
            (Flask object): Get the server object
        """
        return self._app

    @staticmethod
    def home():  # pragma: no cover
        """
        Home page display
        """
        print("Home page")
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return render_template('home.html')

    @staticmethod
    @check_for_token
    def view():
        """
        HTTP GET response test
        """
        print("HTTP GET")
        return "You got me!"

    def login(self):
        """
        Login
        """
        if request.form['username'] and request.form['password'] == 'password':
            session['logged_in'] = True
            token = jwt.encode({'user': request.form['username'],
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
                               self._app.config['SECRET_KEY'])
            return jsonify({'token': token.decode('UTF-8')})
        else:
            return make_response('Could not verify!', 403, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    @staticmethod
    @check_for_token
    def update(macaddress):
        """
        Update the software version
        """
        print("Update the software version")

        try:
            request_data = request.get_json()

            csv_reader = MusicPlayerCsvReader(VALID_CLIENT_CSV_FILE)
            mac_address_list = csv_reader.get_mac_address_list()

            # Invalid client ID
            if macaddress not in mac_address_list:
                return jsonify({"message": "invalid clientId or token supplied"}), 401

            res = make_response(jsonify(request_data), 200)
            return res

        except BaseException:
            res = jsonify({"message": "An internal server error occurred"}), 500
            return res
