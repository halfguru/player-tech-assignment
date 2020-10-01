"""
Tests for  CLI commands.
"""

from click.testing import CliRunner
import unittest

from player_tech_assignment import cli


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

        result = self.runner.invoke(cli.cli_pta, ['update-software', '--macaddr', '1234'])
        output = result.output
        expected_output = 'MAC address format is not valid'
        assert expected_output in output
        assert result.exit_code is 0

        result = self.runner.invoke(cli.cli_pta, ['update-software', '--macaddr', '1B:7E:10:62:06:31'])
        output = result.output
        expected_output = 'Token is not defined'
        assert expected_output in output
        assert result.exit_code is 0


# ------------------------- Scripts ---------------------------------#
if __name__ == '__main__':
    unittest.main()
