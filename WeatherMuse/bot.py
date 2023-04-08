import discord
from discord.ext import commands
from type import Config
import os
import json


class WeatherMuse(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='/',
            intents= discord.Intents.all()
            )
        
        with open("./config.json", "r", encoding="utf-8") as f:
            config: Config = json.load(f)
            self.token: str = config['WeatherMuse']['token']
            self.id: str = config['WeatherMuse']['id']
    
    def run(self):
        super().run(self.token)
    
    async def setup_hook(self):
        for file in os.listdir("./WeatherMuse/cogs"):
            if file.endswith(".py"):
                await self.load_extension(f"WeatherMuse.cogs.{file.split('.')[0]}", )
        
        await self.tree.sync(guild= discord.Object(id=self.id))
    
    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")

    