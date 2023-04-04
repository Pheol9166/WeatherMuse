import discord
from discord.ext import commands
import json


class WeatherMuse(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='/',
            intents= discord.Intents.all()
            )
        
        with open("./config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            self.token = config['WeatherMuse']['token']
            self.id = config['WeatherMuse']['id']
    
    def run(self):
        super().run(self.token)
    
    async def setup_hook(self):
        await self.load_extension("cogs.Recommend")
        await self.load_extension("cogs.Edit")
        await bot.tree.sync(guild= discord.Object(id=self.id))
    
    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")

bot = WeatherMuse()
bot.run()