from discord.ext import commands

class SongNotFound(commands.CommandError):
    def __str__(self) -> str:
        return "노래가 플레이리스트에 없습니다."

class EmbedMakeError(commands.CommandError):
    def __str__(self) -> str:
        return "임베드 오류!"

class WeatherAPIError(commands.CommandError):
    def __str__(self) -> str:
        return "날씨 API에 문제가 생겼습니다."
    
class WeatherNotFound(commands.CommandError):
    def __str__(self) -> str:
        return "날씨가 플레이리스트에 없습니다."

class InputNotFound(commands.CommandError):
    def __str__(self) -> str:
        return "입력한 값이 플레이리스트에 없습니다."