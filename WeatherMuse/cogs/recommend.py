from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands
import requests
import json
import random


class Recommend(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        with open("./config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            self.weather_api_key = config['OpenWeatherAPI']['token']
        self.songs_data: json = self.get_songs_data()

    def get_songs_data(self):
        with open('./DB/songs.json', 'r') as f:
            data = json.load(f)
        return data

    def get_weather(self, city: str) -> Optional[str]:
        try:
            weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric'
            response = requests.get(weather_url)
            weather_data = response.json()
            weather_main = weather_data['weather'][0]['main']

            return weather_main
        except:
            return None

    def recommend(self, weather: str) -> Optional[str]:
        try:
            if weather in ["Rain", "Drizzle", "Squall", "Tornado", "Thunderstorm"]:
                return self.songs_data["Rain"]
            elif weather == "Snow":
                return self.songs_data["Snow"]
            elif weather in ["Clouds", "Haze", "Fog", "Mist", "Ash", "Dust", "Smoke", "Sand"]:
                return self.songs_data["Clouds"]
            elif weather == "Clear":
                return self.songs_data["Clear"]
            else:
                return None
        except:
            return None
    
    @app_commands.command(name="추천", description="오늘 날씨에 맞는 노래를 추천합니다. (기본은 서울)")
    @app_commands.describe(city="The city to get weather")
    async def recommend_command(self, interaction: discord.Interaction, city: str="Seoul") -> None:
        weather: str= self.get_weather(city)
        songs: str= self.recommend(weather)
    
        if songs is None:
            await interaction.response.send_message("미안해요... 이 날씨에 맞는 노래는 없어요...")
        else:
            song = random.choice(songs)
            embed = discord.Embed(title="Weather Muse", description="날씨에 따른 음악 추천", color=0x00aaaa)
            embed.add_field(name="🌦️ 날씨", value=f"{weather}({city})", inline=False)
            embed.add_field(name="🎵 제목", value=song["title"], inline=False)
            embed.add_field(name="🎤 가수", value=song["artist"], inline=False)
            embed.add_field(name="📌 URL", value=song["url"], inline=False)
            await interaction.response.send_message(embed=embed)      

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Recommend(bot),
        guilds= [discord.Object(id= bot.id)]
    )
    