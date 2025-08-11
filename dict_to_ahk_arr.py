import json, os

with open("bookmarks.json") as f: #load json
    book = json.load(f)

cache_dir = os.path.join(os.getcwd(), "cache_") #to save the arrays to txt
os.makedirs(cache_dir, exist_ok=True)

#json -> txt
def write_json_to_files(json_data):
    with open(os.path.join(cache_dir, "titles.txt"), "w", encoding="utf-8") as ft, \
         open(os.path.join(cache_dir, "nkeys.txt"), "w", encoding="utf-8") as fn, \
         open(os.path.join(cache_dir, "links.txt"), "w", encoding="utf-8") as fl:
        
        for key, val in json_data.items():
            ft.write(f"{key}\n")
            fn.write(f"{val['nkey']}\n")
            fl.write(f"{val['link']}\n")
