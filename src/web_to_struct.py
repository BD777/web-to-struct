from typing import Any, Callable, Optional, Union, List, Dict, Tuple
from bs4 import BeautifulSoup


# built-in functions
def string_to_element(content: Union[str, bytes], feature: str = "html5lib") -> BeautifulSoup:
    return BeautifulSoup(content, feature)


def css(content: BeautifulSoup, pattern: Union[str, List[str]]) -> Optional[BeautifulSoup, List[BeautifulSoup]]:
    resp = content.select(pattern)
    if len(resp) == 0:
        return None
    elif len(resp) == 1:
        return resp[0]
    else:
        return resp


def xpath():  # TODO
    raise NotImplementedError


def index(content: Union[Dict, Tuple], pattern: str) -> Any:
    # TODO
    if isinstance(content, dict):
        pass
    elif isinstance(content, tuple):
        pass
    else:
        raise TypeError(f"Dict or Tuple accepted in function index, found {type(content)}")


class Parser:
    funcs = {}
    builtin_functions = [
        ("string-to-element", string_to_element),
        ("css", css),
    ]

    def __init__(self):
        for name, func in self.builtin_functions:
            self.register(name, func)

    def register(self, name: str, func: Callable):
        self.funcs[name] = func

    def parse(self, content: Any, config: dict) -> dict:
        resp = {}

        name = config["name"]
        value = content
        for map_func in config["map"]:
            if map_func["function"] not in self.funcs:
                raise NotImplementedError(f"function {map_func['function']} not registered")

            func = self.funcs[map_func["function"]]
            value = func(value, **map_func["kwargs"])

        if "children" in config and len(config["children"]) > 0:
            children = config["children"]
            if len(children) == 1:
                if isinstance(value, list):
                    resp[name] = []
                    for v in value:
                        resp[name].append(self.parse(v, children[0]))
                else:
                    resp[name] = self.parse(value, children[0])
            else:
                resp[name] = []
                for child in children:
                    if isinstance(value, list):
                        for v in value:
                            resp[name].append(self.parse(v, child))
                    else:
                        resp[name].append(self.parse(value, child))
        else:
            resp[name] = value

        return resp
