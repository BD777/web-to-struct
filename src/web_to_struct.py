from typing import Union

from bs4 import BeautifulSoup


class Parser:
    def __init__(self, features=None):
        self.features = features

    def parse(self, content: Union[bytes, str], config: dict):
        soup = BeautifulSoup(content, self.features)
        resp = {}

