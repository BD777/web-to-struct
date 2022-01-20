import json
import re
from typing import Any, Callable, Optional, Union, List, Dict, Tuple
from bs4 import BeautifulSoup


# built-in functions
def string_to_element(content: Union[str, bytes], feature: str = "html5lib") -> BeautifulSoup:
    return BeautifulSoup(content, feature)


def css(content: BeautifulSoup, pattern: Union[str, List[str]]) -> Union[BeautifulSoup, List[BeautifulSoup], None]:
    value = content.select(pattern)
    if len(value) == 0:
        return None
    elif len(value) == 1:
        return value[0]
    else:
        return value


def xpath():  # TODO
    raise NotImplementedError


def index(content: Union[Dict, Tuple, List], pattern: str) -> Any:
    keys = []
    tmp = ""
    for c in pattern:
        if c == ".":
            if len(tmp) > 0:
                keys.append(tmp)
                tmp = ""
        elif c == "[":
            if len(tmp) > 0:
                keys.append(tmp)
                tmp = ""
        elif c == "]":
            if len(tmp) > 0:
                try:
                    keys.append(int(tmp))
                except:
                    keys.append(tmp)
                tmp = ""
        else:
            tmp += c

    if len(tmp) > 0:
        keys.append(tmp)

    value = content
    for key in keys:
        if isinstance(value, dict):
            value = value[key]
        elif isinstance(value, tuple) or isinstance(value, list):
            if isinstance(key, str):
                raise TypeError(f"int index is required for tuple, str found")
            value = value[key]
        else:
            raise TypeError(f"Dict, Tuple or List accepted in function index, found {type(value)}")

    return value


def text(content: BeautifulSoup, strip: bool = True) -> str:
    return content.get_text(strip=strip)


def html(content: BeautifulSoup) -> str:
    return content.prettify()


def attr(content: BeautifulSoup, attr_name: str) -> Any:
    if content.has_attr(attr_name):
        return content[attr_name]
    return None


def regex(content: str, pattern: str):
    value = re.findall(pattern, content)
    if len(value) == 0:
        return None
    elif len(value) == 1:
        return value[0]
    else:
        return value


def tuple_to_string(content: Tuple, pattern: str):
    value = pattern
    for i in range(len(content)):
        value = value.replace(f"${i + 1}", content[i])
    return value


def json_parse(content: str):
    return json.loads(content.strip())


class Parser:
    funcs = {}
    builtin_functions = [
        ("string-to-element", string_to_element),
        ("css", css),
        ("index", index),
        ("text", text),
        ("html", html),
        ("attr", attr),
        ("regex", regex),
        ("tuple-to-string", tuple_to_string),
        ("json-parse", json_parse),
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
            value = func(value, **map_func.get("kwargs", {}))
            # TODO maybe print value in debug mode
            # print(map_func["function"])
            # print(value)

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


if __name__ == '__main__':
    import requests
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    }
    r = requests.get("https://detail.tmall.com/item.htm?id=637516470472", headers=headers)
    # print(r.text)
    # print(re.findall(r"TShop.Setup\((.*?)\);", r.text))

    config = {
        "name": "data",
        "map": [
            {"function": "regex", "kwargs": {"pattern": r"TShop.Setup\(\s*(.*?)\s*\);"}},
            {"function": "json-parse"}
        ]
    }
    parser = Parser()
    resp = parser.parse(r.text, config)
    print(resp)
