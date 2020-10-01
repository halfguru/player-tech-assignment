"""
Tests for CLI commands.
"""

from click.testing import CliRunner
from pathlib import Path
import unittest

from player_tech_assignment import cli

WORKING_DIR = Path.cwd()
TEST_DATA_DIR = WORKING_DIR / "tests" / "test_data"
TEST_CSV_FILE = TEST_DATA_DIR / "test_local_data.csv"


class TestCli(unittest.TestCase):
    """
    Test music player cli
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the cli
        """
        cls.runner = CliRunner()

    def test_basic_cli(self):
        """
        Test the CLI basic interface
        """
        result = self.runner.invoke(cli.cli_pta)
        assert result.exit_code == 0
        assert 'Player Tech Assignment CLI' in result.output

        help_result = self.runner.invoke(cli.cli_pta, ['--help'])
        assert help_result.exit_code == 0
        assert "Usage: cli-pta" in help_result.output

    def test_cli_update_command(self):
        """
        Test update_software command
        """
        cli_result = self.runner.invoke(cli.cli_pta, ['update-software', '--help'])
        assert not cli_result.exception
        assert "software" in cli_result.output

        # Invalid command arguments
        result = self.runner.invoke(cli.cli_pta, ['update-software', '--username', '1234'])
        output = result.output
        expected_output = "Missing option '--password"
        assert expected_output in output
        assert result.exit_code is not 0

        result = self.runner.invoke(cli.cli_pta, ['update-software', '--username', '1234', '--password', '1234'])
        output = result.output
        expected_output = "Missing option '--input"
        assert expected_output in output
        assert result.exit_code is not 0

        # Invalid authentification credentials
        result = self.runner.invoke(cli.cli_pta, ['update-software', '--username', '1234', '--password', '1234', '--input', TEST_CSV_FILE])
        output = result.output
        expected_output = "Could not get token because of invalid credentials"
        assert expected_output in output
        assert result.exit_code is 0

        # Valid credentials
        result = self.runner.invoke(cli.cli_pta, ['update-software', '--username', '1234', '--password', 'password', '--input', TEST_CSV_FILE])
        output = result.output
        expected_output = "Music players software update successful!"
        assert expected_output in output
        assert result.exit_code is 0


# ------------------------- Scripts ---------------------------------#
if __name__ == '__main__':
    unittest.main()
