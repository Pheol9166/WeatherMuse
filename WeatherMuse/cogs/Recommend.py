from typing import Optional
import requests
import json
import random
import discord
from discord import app_commands
from discord.ext import commands
from WeatherMuse.type import Config, JSON, Playlist
from WeatherMuse.load_songs import get_songs
from WeatherMuse.err.errors import WeatherAPIError, WeatherNotFound, SongNotFound


class Recommend(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("./config.json", "r", encoding="utf-8") as f:
            config: Config = json.load(f)
            self.weather_api_key: str = config['OpenWeatherAPI']['token']


    def get_weather(self, city: str) -> str:
        try:
            weather_url: str = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric'
            response: requests.Response = requests.get(weather_url)
            weather_data: JSON = response.json()
            weather_main: str = weather_data['weather'][0]['main']

            return weather_main
        except:
            raise WeatherAPIError

    def recommend(self, weather: str) -> str:
        try:
            songs_data: Playlist = get_songs()
            if weather in ["Rain", "Drizzle", "Squall", "Tornado", "Thunderstorm"]:
                return songs_data["Rain"]
            elif weather == "Snow":
                return songs_data["Snow"]
            elif weather in ["Clouds", "Haze", "Fog", "Mist", "Ash", "Dust", "Smoke", "Sand"]:
                return songs_data["Clouds"]
            elif weather == "Clear":
                return songs_data["Clear"]
            else:
                raise WeatherNotFound
        except:
            raise SongNotFound
    
    @app_commands.command(name="추천", description="오늘 날씨에 맞는 노래를 추천합니다. (기본은 서울)")
    @app_commands.describe(city="The city to get weather")
    async def recommend_command(self, interaction: discord.Interaction, city: str="Seoul") -> None:
        weather: str= self.get_weather(city)
        songs: str= self.recommend(weather)
    
        song: str = random.choice(songs)
        embed = discord.Embed(title="Weather Muse", description="날씨에 따른 음악 추천", color=0x00aaaa)
        embed.add_field(name="🌦️ 날씨", value=f"{weather}({city})", inline=False)
        embed.add_field(name="🎵 제목", value=song["title"], inline=False)
        embed.add_field(name="🎤 가수", value=song["artist"], inline=False)
        embed.add_field(name="📌 URL", value=song["url"], inline=False)
        await interaction.response.send_message(embed=embed)    
        
    @recommend_command.error
    async def recommend_error(self, interaction: discord.Interaction, error: commands.CommandInvokeError):
        custom_err = error.original
        if isinstance(custom_err, SongNotFound):
            await interaction.response.send_message("미안해요... 이 날씨에 맞는 노래는 없어요...")
        elif isinstance(custom_err, WeatherAPIError):
            await interaction.response.send_message("API 에러! 다시 시도해주세요...")
        elif isinstance(custom_err, WeatherNotFound):
            await interaction.response.send_message("해당 날씨는 플레이리스트에 없어요...")
        else:
            await interaction.response.send_message("에러! 다시 시도해주세요!")      

async def setup(bot: commands.Bot):
    await bot.add_cog(
        Recommend(bot),
        guilds= [discord.Object(id= bot.id)]
    )
    
