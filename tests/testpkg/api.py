import requests
import numpy as np

from .database import conn

response = requests.get("https://example.com")

print(np.array([1, 2, 3]))