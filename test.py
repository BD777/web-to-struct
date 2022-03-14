import requests
import json
from web_to_struct import Parser


if __name__ == '__main__':
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    }
    r = requests.get("https://copymanga.org/recommend", headers=headers)

    config = {
        "name": "data",
        "map": [
            {"function": "string-to-element"},
            {"function": "css", "kwargs": {"patterns": ["#comic > .row > .exemptComicItem"]}},
        ],
        "children": [{
            "name": "title",
            "map": [
                {"function": "css", "kwargs": {"patterns": ["p[title]"]}},
            ]
        }, {
            "name": "img",
            "map": [
                {"function": "css", "kwargs": {"patterns": [".exemptComicItem-img > a > img"]}},
                {"function": "attr", "kwargs": {"attr_name": "data-src"}},
            ]
        }, {
            "name": "comic_id",
            "map": [
                {"function": "css", "kwargs": {"patterns": [".exemptComicItem-img > a"]}},
                {"function": "attr", "kwargs": {"attr_name": "href"}},
                {"function": "regex", "kwargs": {"pattern": r"comic/(.*?)$"}},
            ]
        }, {
            "name": "author",
            "map": [
                {"function": "css", "kwargs": {"patterns": [".exemptComicItem-txt > span.exemptComicItem-txt-span > a[href^=\"/author\"]"]}},
            ],
        }]
    }
    parser = Parser()
    resp = parser.parse(r.text, config)
    print(json.dumps(resp, ensure_ascii=False, indent=2))
