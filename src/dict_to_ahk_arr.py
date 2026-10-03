import json, os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BOOKMARKS_JSON = os.path.join(BASE_DIR, "data", "bookmarks.json")
cache_dir = os.path.join(BASE_DIR, "cache_")

os.makedirs(cache_dir, exist_ok=True)


def load_bookmarks():
    with open(BOOKMARKS_JSON, encoding="utf-8") as f:
        return json.load(f)


def write_json_to_files(json_data):
    with open(os.path.join(cache_dir, "titles.txt"), "w", encoding="utf-8") as ft, \
         open(os.path.join(cache_dir, "nkeys.txt"), "w", encoding="utf-8") as fn, \
         open(os.path.join(cache_dir, "links.txt"), "w", encoding="utf-8") as fl:

        for key, val in json_data.items():
            ft.write(f"{key}\n")
            fn.write(f"{val['nkey']}\n")
            fl.write(f"{val['link']}\n")
