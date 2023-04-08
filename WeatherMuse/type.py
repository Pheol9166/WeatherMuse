from typing import Union
from typing import TypedDict, Union

JSON = dict[str, Union[str, int, bool, float, list, dict, None]]

class Config(TypedDict):
    OpenWeatherAPI: dict[str, str]
    WeatherMuse: dict[str, Union[int, str]]

class Song(TypedDict):
    title: str
    artist: str
    url: str   
    
class Playlist(TypedDict):
    Clear: list[Song]
    Clouds: list[Song]
    Rain: list[Song]
    Snow: list[Song]
    
               