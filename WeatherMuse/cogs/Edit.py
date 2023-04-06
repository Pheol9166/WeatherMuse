import json
import discord
from discord import app_commands
from discord.ext import commands
from WeatherMuse.load_songs import get_songs
from WeatherMuse.err.errors import SongNotFound


class Edit(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    def write_songs(self, songs: json) -> None:
        with open("./DB/songs.json", "w") as fw:
                json.dump(songs, fw, ensure_ascii=False, indent=4)
                
    def change(self, mode: str, song_name: str, new: str) -> None:
        """_데이터 변경을 위한 함수입니다_

        Args:
            mode (_str_): 무엇을 변경할 지 정하는 파라미터입니다.
                't': 타이틀을 변경합니다.
                'a': 아티스트를 변경합니다.
                'u': URL을 변경합니다.
            weather (app_commands.Choice[str]): _날씨를 받습니다._
            song_name (str): _찾는 노래 제목입니다._
            new (str): _바꿀 내용입니다._
        """
        songs = get_songs()
        
        match mode:
            case 't':
                group = "title"
            case 'a':
                group = "artist"
            case 'u':
                group = "url"
        
        for weather in songs:
            for song in songs[weather]:
                if song['title'].lower() == song_name.lower():
                    song[group] = new
                    self.write_songs(songs)
                    return 
        
        raise SongNotFound

    @app_commands.command(name="타이틀_변경", description="곡의 제목을 수정합니다.")
    @app_commands.describe(song_name="변경할 노래", new_title="바꿀 제목")
    async def change_title(self, interaction: discord.Interaction, song_name: str, new_title: str):
        try:
            self.change('t', song_name, new_title)
            embed = discord.Embed(title="🎵 곡 제목 변경", description=f"{song_name}의 제목이 {new_title}로 변경되었습니다!", color=0x00aaaa)
            await interaction.response.send_message(embed=embed)    
        except SongNotFound:
            await interaction.response.send_message(f"{song_name}라는 노래는 플레이리스트에 없어요...")
                  
    @app_commands.command(name="가수_변경", description="곡의 가수를 수정합니다.")
    @app_commands.describe(song_name="변경할 노래", new_artist="바꿀 가수")
    async def change_artist(self, interaction: discord.Interaction, song_name: str, new_artist: str):
        try:
            self.change('a', song_name, new_artist)
            embed = discord.Embed(title="🎤 가수명 변경", description=f"{song_name}의 가수가 {new_artist}로 변경되었습니다!", color=0x00aaaa)
            await interaction.response.send_message(embed=embed)
        except SongNotFound:
            await interaction.response.send_message(f"{song_name}라는 노래는 플레이리스트에 없어요...")
            
    @app_commands.command(name="url_변경", description="곡의 URL를 수정합니다.")
    @app_commands.describe(song_name="변경할 노래", new_url="바꿀 URL")
    async def change_url(self, interaction: discord.Interaction, song_name: str, new_url: str):
        try:
            self.change('u', song_name, new_url)
            embed = discord.Embed(title="📌 URL 변경", description=f"{song_name}의 URL이 {new_url}로 변경되었습니다!", color=0x00aaaa)
            await interaction.response.send_message(embed=embed)
        except SongNotFound:
            await interaction.response.send_message(f"{song_name}라는 노래는 플레이리스트에 없어요...")
        
    @app_commands.command(name="노래_추가", description="플레이리스트에 새로운 곡을 추가합니다.")
    @app_commands.describe(weather="날씨", title="곡 제목", artist="가수", url="URL")
    @app_commands.choices(weather=[
        app_commands.Choice(name="Clear", value="Clear"),
        app_commands.Choice(name="Clouds", value="Clouds"),
        app_commands.Choice(name="Rain", value="Rain"),
        app_commands.Choice(name="Snow", value="Snow")
    ])
    async def add_song(self, interaction: discord.Interaction, weather: app_commands.Choice[str], title: str, artist: str, url: str):
        try:
            songs = get_songs()
            songs = songs[weather.value]
                          
            elems = [(song["title"].lower(), song["artist"].lower(), song["url"])  for song in songs]
            if (title.lower(), artist.lower(), url) in elems:
                await interaction.response.send_message(f"{title}은 이미 플레이리스트에 있어요!")
                return
                
            new_song = {
                "title": title,
                "artist": artist,
                "url": url
            }
            songs.append(new_song)
            self.write_songs(songs)
            
            embed = discord.Embed(title="노래 추가", color=0x00aaaa)
            embed.add_field(name="🎵 추가된 곡", value=f"{title}", inline=False)
            embed.add_field(name="🎤 아티스트", value=f"{artist}", inline=False)
            embed.add_field(name="📌 URL", value=f"{url}", inline=False)
            await interaction.response.send_message(embed=embed)
        except:
            await interaction.response.send_message("에러! 다시 시도해주세요...")
    
    @app_commands.command(name="노래_제거", description="플레이리스트의 기존의 곡을 제거합니다.")
    @app_commands.describe(weather="날씨", title="곡 제목")
    @app_commands.choices(weather=[
        app_commands.Choice(name="Clear", value="Clear"),
        app_commands.Choice(name="Clouds", value="Clouds"),
        app_commands.Choice(name="Rain", value="Rain"),
        app_commands.Choice(name="Snow", value="Snow")
    ])
    async def delete_song(self, interaction: discord.Interaction, weather: app_commands.Choice[str], title: str):
        try:
            songs = get_songs() 
            for song in songs:
                if song[weather.value]['title'] == title:
                    songs.remove(song)
                    flag = True
            if flag:
                self.write_songs(songs)
                embed = discord.Embed(title="노래 제거")
                embed.add_field(name="🎵 제거된 곡", value=f"{title}")
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(f"{title}이라는 곡은 플레이리스트에 없어요...")
        except:
            await interaction.response.send_message("에러! 다시 시도해주십시오...")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Edit(bot),
        guilds= [discord.Object(id= bot.id)]
    )