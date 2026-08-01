import pathlib
import logging

logger = logging.getLogger(__name__)


def load_file(path):
    return pathlib.Path(path).read_text()