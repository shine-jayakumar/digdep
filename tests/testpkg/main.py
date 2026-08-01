import os
import json
import pathlib

from .config import Config
from .parser import parse_file
from .helpers.math_utils import add

parse_file("input.txt")

x = add(10, 20)

print(os.getcwd())