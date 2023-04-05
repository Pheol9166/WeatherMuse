import json

def get_songs() -> json:
    with open("./DB/songs.json", "r") as f:
        return json.load(f)