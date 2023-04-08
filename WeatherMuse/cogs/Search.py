from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands
from WeatherMuse.type import Song, Playlist
from WeatherMuse.load_songs import get_songs
from WeatherMuse.err.errors import EmbedMakeError, InputNotFound


class Search(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    def make_embed(self, song: Song) -> discord.Embed:
        try:
            embed = discord.Embed(title="Weather Muse", description="검색 결과", color=0x00aaaa)
            embed.add_field(name="제목", value=song['title'], inline=False)
            embed.add_field(name="가수", value=song['artist'], inline=False)
            embed.add_field(name="URL", value=song['url'], inline=False)
            return embed
        except:
            raise EmbedMakeError
    
    def search_by_mode(self, mode: str, std: str, std2: Optional[str]= None) -> list[discord.Embed]:
        """_플레이리스트에서 노래를 검색하여 임베드 리스트로 반환하는 함수입니다_

        Args:
            mode (str): _기준을 정하는 파라미터입니다._
                't': 타이틀을 기준으로 검색합니다.
                'a': 아티스트를 기준으로 검색합니다.
                'm': 타이틀과 아티스트 두 가지 기준으로 검색합니다.
            std (str): _검색할 입력값입니다._
            std2 (Optional[str], optional): _기준이 'm'일 시 입력할 또다른 검색입니다._. Defaults to None.

        Raises:
            InputNotFound: _입력값이 플레이리스트에 없을 때 발생하는 에러입니다._

        Returns:
            list[discord.Embed]: _검색 결과입니다._
        """
        results = []
        songs: Playlist = get_songs()
        
        match mode:
            case 't':
                group: str= 'title'
            case 'a':
                group: str= 'artist'
            case 'm':
                group: list[str] = ['title', 'artist']
            
        for weather in songs:
            for song in songs[weather]:
                if mode == 'm':
                    if song[group[0]].lower() == std.lower() and song[group[1]].lower() == std2.lower():
                        results.append(song)
                else:
                    if song[group].lower() == std.lower():
                        results.append(song)
        
        if len(results):
            embeds: list[discord.Embed] = [self.make_embed(result) for result in results]
            return embeds
        
        raise InputNotFound
        
    @app_commands.command(name="종합_검색", description="제목과 가수에 부합하는 곡을 찾습니다.")
    @app_commands.describe(song_name="노래 제목", artist="가수")
    async def search_song(self, interaction: discord.Interaction, song_name: str, artist: str):
        embeds: list[discord.Embed] = self.search_by_mode('m', song_name, artist)
        
        for embed in embeds:
            await interaction.response.send_message(embed=embed)
            
    @app_commands.command(name="제목으로_검색", description="제목에 부합하는 곡을 찾습니다.")
    @app_commands.describe(song_name="노래 제목")
    async def search_by_name(self, interaction: discord.Interaction, song_name: str):
        embeds: list[discord.Embed] = self.search_by_mode('t', song_name)

        await interaction.response.send_message(embeds=embeds)
    
    @app_commands.command(name="가수로_검색", description="가수에 부합하는 곡을 찾습니다.")
    @app_commands.describe(artist="가수")
    async def search_by_artist(self, interaction: discord.Interaction, artist: str):
        embeds: list[discord.Embed] = self.search_by_mode('a', artist)
        
        await interaction.response.send_message(embeds=embeds)
    
    @search_song.error
    async def search_song_error(self, interaction: discord.Interaction, error: commands.CommandInvokeError):
        custom_err = error.original
        if isinstance(custom_err, InputNotFound):
            await interaction.response.send_message("이 곡은 플레이리스트에 없어요...")
        elif isinstance(custom_err, EmbedMakeError):
            await interaction.response.send_message("임베드 생성 에러! 다시 시도해주세요...")
        else:
            await interaction.response.send_message("에러! 다시 시도해주세요...")
    
    @search_by_name.error
    async def search_name_error(self, interaction: discord.Interaction, error: commands.CommandInvokeError):
        custom_err = error.original
        if isinstance(custom_err, InputNotFound):
            await interaction.response.send_message("이 노래 제목은 플레이리스트에 없어요...")
        elif isinstance(custom_err, EmbedMakeError):
            await interaction.response.send_message("임베드 생성 에러! 다시 시도해주세요...")
        else:
            await interaction.response.send_message("에러! 다시 시도해주세요...")

    @search_by_artist.error
    async def search_artist_error(self, interaction: discord.Interaction, error):
        custom_err = error.original
        if isinstance(custom_err, InputNotFound):
            await interaction.response.send_message("이 가수는 플레이리스트에 없어요...")
        elif isinstance(custom_err, EmbedMakeError):
            await interaction.response.send_message("임베드 생성 에러! 다시 시도해주세요...")
        else:
            await interaction.response.send_message("에러! 다시 시도해주세요...")


async def setup(bot: commands.Bot):
    await bot.add_cog(
        Search(bot),
        guilds= [discord.Object(id= bot.id)]
    )