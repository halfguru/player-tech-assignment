"""Top-level package for player-tech-assignment."""

__author__ = """Simon Ho"""
__email__ = 'simon.dk.ho@gmail.com'
__version__ = '0.1.0'

try:
    from .client import *
    from .csv_reader import *
except ImportError: # pragma: no cover
    # Workaround to avoid ImporError in setup.py
    pass # pragma: no cover
