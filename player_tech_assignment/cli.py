"""
Console script for player_tech_assignment.
"""
import click
import os

from .csv_reader import MusicPlayerCsvReader
from .server.server import MusicPlayerUpdateServer
from .client import MusicPlayerClient, MusicPlayerClientError

DEFAULT_BASE_URL = "http://127.0.0.1:5000"
DEFAULT_CSV_FILE = "test_data/input.csv"


@click.group()
def cli_pta():
    """
    Player Tech Assignment CLI
    """
    pass


@cli_pta.command()
@click.option("--input", "-c", type=str, default=DEFAULT_CSV_FILE, help="Specify input csv file", required=False)
def read_csv(input):
    """
    Read music player csv file
    """
    csv_reader = MusicPlayerCsvReader(input)
    mac_addresses = csv_reader.get_mac_address_list()
    click.echo(mac_addresses)


@cli_pta.command()
@click.option("--ipaddr", "-ip", type=str, default="0.0.0.0", help="Specify server ip address", required=False)
@click.option("--port", "-p", type=int, default=5000, help="Specify server port", required=False)
def run_server(ipaddr, port):
    """
    Run music player update server
    """
    server = MusicPlayerUpdateServer().app
    server.run(host=ipaddr, debug=True, port=port)


@cli_pta.command()
@click.option("--username", "-u", type=str, help="Specify authentification username", required=True)
@click.option("--password", "-p", type=str, help="Specify authentification password", required=True)
def login(username, password):
    """
    Login
    """
    try:
        client = MusicPlayerClient(DEFAULT_BASE_URL)
        token = client.login(username, password)
        os.environ["token"] = token
        print(token)
    except MusicPlayerClientError as err:
        click.echo("{0}".format(err))


@cli_pta.command()
@click.option("--macaddr", "-m", type=str, default="1B:7E:10:62:06:31", help="Specify music player MAC address", required=False)
@click.option("--token", "-t", type=str, default=os.environ.get("token"), help="Specify authentification token ID", required=False)
def update_software(macaddr, token):
    """
    Update software
    """
    try:
        client = MusicPlayerClient(DEFAULT_BASE_URL)
        res = client.update_player(macaddr, token)
        print(res)
    except MusicPlayerClientError as err:
        click.echo("{0}".format(err))


if __name__ == '__main__':
    cli_pta()
