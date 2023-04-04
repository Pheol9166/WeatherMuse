import discord
from discord import app_commands
from discord.ext import commands
import json

  
class Edit(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="타이틀_변경", description="곡의 제목을 수정합니다.")
    @app_commands.describe(weather="날씨", song_name="변경할 노래", new_title="바꿀 제목")
    @app_commands.choices(weather=[
        app_commands.Choice(name="Clear", value="Clear"),
        app_commands.Choice(name="Clouds", value="Clouds"),
        app_commands.Choice(name="Rain", value="Rain"),
        app_commands.Choice(name="Snow", value="Snow")
    ])
    async def change_title(self, interaction: discord.Interaction, weather: app_commands.Choice[str], song_name: str, new_title: str):
        try:
            with open("./DB/songs.json", "r") as f:
                songs = json.load(f)
                
            for song in songs[weather.value]:
                if song['title'] == song_name:
                    song['title'] = new_title
                    with open("./DB/songs.json", "w") as fw:
                        json.dump(songs, fw, ensure_ascii=False, indent=4)
                    embed = discord.Embed(title="🎵 곡 제목 변경", description=f"{song_name}의 제목이 {new_title}로 변경되었습니다!", color=0x00aaaa)
                    await interaction.response.send_message(embed=embed)   
                    return
                
            raise ValueError
        except ValueError:
            await interaction.response.send_message(f"{song_name}라는 노래는 플레이리스트에 없어요...")
                  
    @app_commands.command(name="가수_변경", description="곡의 가수를 수정합니다.")
    @app_commands.describe(weather="날씨", song_name="변경할 노래", new_artist="바꿀 가수")
    @app_commands.choices(weather=[
        app_commands.Choice(name="Clear", value="Clear"),
        app_commands.Choice(name="Clouds", value="Clouds"),
        app_commands.Choice(name="Rain", value="Rain"),
        app_commands.Choice(name="Snow", value="Snow")
    ])
    async def change_artist(self, interaction: discord.Interaction, weather:app_commands.Choice[str], song_name: str, new_artist: str):
        try:
            with open("./DB/songs.json", "r") as f:
                songs = json.load(f)
                
            for song in songs[weather.value]:
                if song['title'] == song_name:
                    song['artist'] = new_artist
                    with open("./DB/songs.json", "w") as fw:
                        json.dump(songs, fw, ensure_ascii=False, indent=4)
                    embed = discord.Embed(title="🎤 가수명 변경", description=f"{song_name}의 가수가 {new_artist}로 변경되었습니다!", color=0x00aaaa)
                    await interaction.response.send_message(embed=embed)
                    return
            raise ValueError
        except ValueError:
            await interaction.response.send_message(f"{song_name}라는 노래는 플레이리스트에 없어요...")
            
    @app_commands.command(name="url_변경", description="곡의 URL를 수정합니다.")
    @app_commands.describe(weather="날씨", song_name="변경할 노래", new_url="바꿀 URL")
    @app_commands.choices(weather=[
        app_commands.Choice(name="Clear", value="Clear"),
        app_commands.Choice(name="Clouds", value="Clouds"),
        app_commands.Choice(name="Rain", value="Rain"),
        app_commands.Choice(name="Snow", value="Snow")
    ])
    async def change_url(self, interaction: discord.Interaction, weather:app_commands.Choice[str], song_name: str, new_url: str):
        try:
            with open("./DB/songs.json", "r") as f:
                songs = json.load(f)
                
            for song in songs[weather.value]:
                if song['title'] == song_name:
                    song['url'] = new_url
                    with open("./DB/songs.json", "w") as fw:
                        json.dump(songs, fw, ensure_ascii=False, indent=4)
                    embed = discord.Embed(title="📌 URL 변경", description=f"{song_name}의 URL이 {new_url}로 변경되었습니다!", color=0x00aaaa)
                    await interaction.response.send_message(embed=embed)
                    return
            raise ValueError
        except ValueError:
            await interaction.response.send_message(f"{song_name}라는 노래는 플레이리스트에 없어요...")
        
    @app_commands.command(name="곡_추가", description="플레이리스트에 새로운 곡을 추가합니다.")
    @app_commands.describe(weather="날씨", title="곡 제목", artist="가수", url="URL")
    @app_commands.choices(weather=[
        app_commands.Choice(name="Clear", value="Clear"),
        app_commands.Choice(name="Clouds", value="Clouds"),
        app_commands.Choice(name="Rain", value="Rain"),
        app_commands.Choice(name="Snow", value="Snow")
    ])
    async def add_song(self, interaction: discord.Interaction, weather: app_commands.Choice[str], title: str, artist: str, url: str):
        try:
            with open("./DB/songs.json", "r+") as f:
                songs = json.load(f)
                
                if title in songs[weather.value]:
                    await interaction.response.send_message(f"{title} already exists in playlist!")
                    return
                 
                new_song = {
                    "title": title,
                    "artist": artist,
                    "url": url
                }
                songs[weather.value].append(new_song)
                f.seek(0)
                json.dump(songs, f, ensure_ascii=False, indent=4)
            
            embed = discord.Embed(title="곡 추가", color=0x00aaaa)
            embed.add_field(name="🎵 추가된 곡", value=f"{title}", inline=False)
            embed.add_field(name="🎤 아티스트", value=f"{artist}", inline=False)
            embed.add_field(name="📌 URL", value=f"{url}", inline=False)
            await interaction.response.send_message(embed=embed)
        except:
            await interaction.response.send_message("에러! 다시 시도해주세요...")
    
    @app_commands.command(name="곡_제거", description="플레이리스트의 기존의 곡을 제거합니다.")
    @app_commands.describe(weather="날씨", title="곡 제목")
    @app_commands.choices(weather=[
        app_commands.Choice(name="Clear", value="Clear"),
        app_commands.Choice(name="Clouds", value="Clouds"),
        app_commands.Choice(name="Rain", value="Rain"),
        app_commands.Choice(name="Snow", value="Snow")
    ])
    async def delete_song(self, interaction: discord.Interaction, weather: app_commands.Choice[str], title: str):
        try:
            with open("./DB/songs.json", "r+") as f:
                songs = json.load(f)
                
                for song in songs:
                    if song[weather.value]['title'] == title:
                        songs.remove(song)
                
                json.dump(songs, f, ensure_ascii=False, indent=4)
                
                embed = discord.Embed(title="곡 제거")
                embed.add_field(name="🎵 제거된 곡", value=f"{title}")
            await interaction.response.send_message(embed=embed)
            
        except:
            await interaction.response.send_message("에러! 다시 시도해주십시오...")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Edit(bot),
        guilds= [discord.Object(id= bot.id)]
    )