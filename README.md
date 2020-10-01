## player-tech-assignment

You need to create a production-ready tool that will automate the update of a thousand music players by using an API. You don't have to create the API.

Your tool will be used by different people using different operating systems. The most common ones will be Windows, MacOS and Linux.

The input is a .csv file containing, at the very minimum, MAC addresses of players to update, always in the first column.

## Usage
Install dependencies:
```
$ pip install -r requirements_dev.txt
```

Run music player simulated server:
```
$ python -m player_tech_assignment.cli run-simulation-server
# server is accessible on localhost:5000
```

Update music players CLI command:
```
$ python -m player_tech_assignment.cli update-software --usernarme <username> --password <password> --input <csv_file_input>
```
Note: Use password: ``password`` when using the update-software function with the simulated server

## Tests
To run unit tests, the music player update software simulated server needs to be run beforehand.
```
$ pytest -v
```

## Design choices
* Python was chosen because it is a cross-platform language able to be ran on Windows, MacOS and Linux. It is also a scripting language ideal for this simple use case of simply calling an HTTP API and contains standardized librairies for HTTP requests and .csv file parsing. Additionally, it is very fast for prototype and implementation, contains excellent tools for unit tests and can be integrated effortlessly in CI builds (e.g. JenkinsFile).
* The architecture consists of the CLI, client, server and .csv file parser in different files and objects. The goal is to have an object-oriented design to be easily reusable in other python modules and for readability.
* ``cli.py`` is user-friendly CLI tool to run commands to start the simulated server and tp update the music players
* ``client.py`` is the Music Player client. It validates the .csv input file content and the MAC addresses. The update function requires the .csv file input and a valid username and password to refresh the authenfication token and make sure it doens't get expired. It is able to make two requests:
    *  GET /login request to get authentification token ID
    *  PUT /profiles/clientId:{macaddress} request to update the software version
* ``csv_reader.py`` is the Music Player .csv file reader input containing the MAC addresses to be updated. It validates the content of the .csv file and is able to return the list of addresses to update.
* ``server.py`` is the Music Player update simulation server used for internal testing. For the software update API, it verifies the authentifation token and returns corresponding error codes if the token or MAC adderess is invalid.

## Built With

* [Python 3.8.4](https://www.python.org/downloads/release/python-384/) - Programming language
* [Click](https://github.com/pallets/click) - CLI library
* [flask](https://github.com/pallets/flask) - Web framework
* [pyJWT](https://github.com/jpadilla/pyjwt) - JSON Web Token library
* [pytest](https://github.com/pytest-dev/pytest) - Test framework

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Credits

* This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.