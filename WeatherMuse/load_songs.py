import json
from type import Playlist


def get_songs() -> Playlist:
    with open("./DB/songs.json", "r") as f:
        return json.load(f)