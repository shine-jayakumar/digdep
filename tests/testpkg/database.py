import sqlite3
import json

from .models import User

conn = sqlite3.connect(":memory:")