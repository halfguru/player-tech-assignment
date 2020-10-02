"""
Console script for player_tech_assignment.
"""
import click
import os

from .csv_reader import MusicPlayerCsvReader, MusicPlayerCsvReaderError
from .server.server import MusicPlayerUpdateServer
from .client import MusicPlayerClient, MusicPlayerClientError

DEFAULT_BASE_URL = "http://127.0.0.1:5000"


@click.group()
def cli_pta():
    """
    Player Tech Assignment CLI
    """
    pass


@cli_pta.command()
@click.option("--ipaddr", "-ip", type=str, default="0.0.0.0", help="Specify server ip address", required=False)
@click.option("--port", "-p", type=int, default=5000, help="Specify server port", required=False)
def run_simulation_server(ipaddr, port):
    """
    Run music player update simulation server
    """
    server = MusicPlayerUpdateServer().app
    server.run(host=ipaddr, debug=False, port=port)


@cli_pta.command()
@click.option("--username", "-u", type=str, help="Specify authentification username", required=True)
@click.option("--password", "-p", type=str, help="Specify authentification password", required=True)
@click.option("--input", "-i", type=str, help="Specify input csv file", required=True)
def update_software(input, username, password):
    """
    Update software
    """
    try:
        client = MusicPlayerClient(DEFAULT_BASE_URL, username, password)
        client.update_players(input)
        click.echo("Music players software update successful!")
    except (MusicPlayerClientError, MusicPlayerCsvReaderError) as err:
        click.echo("{0}".format(err))


if __name__ == '__main__':
    cli_pta()
