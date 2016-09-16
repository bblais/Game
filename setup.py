
import Game

from distutils.core import setup
from distutils.extension import Extension

setup(
  name = 'Game',
  version=Game.__version__,
  description="Game Simulation Engine",
  author="Brian Blais",
  packages=['Game'],
)

