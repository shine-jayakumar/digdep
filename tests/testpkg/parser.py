import xml.etree
import re

from .utils import load_file

data = load_file("test.txt")

xml.etree.parse("sample.xml")

print(re.match("a", "abc"))