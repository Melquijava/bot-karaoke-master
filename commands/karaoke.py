import discord
from discord.ext import commands
import asyncio
import yt_dlp
import spotipy
import os
from dotenv import load_dotenv
load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

if SPOTIFY_CLIENT_ID is None or SPOTIFY_CLIENT_SECRET is None:
    raise EnvironmentError("As variáveis SPOTIFY_CLIENT_ID e SPOTIFY_CLIENT_SECRET devem estar definidas no .env")

sp = spotipy.Spotify(auth_manager=spotipy.SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

from config import LETRA
from datetime import datetime, time

def bot_ativo():
    agora = datetime.now().time()
    inicio = time(19, 0)  # 19:00 (7 da noite)
    fim = time(2, 0)      # 02:00 (2 da madrugada)
    return inicio <= agora or agora <= fim

class Karaoke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def karaoke(self, ctx, *, musica: str):
        if not bot_ativo():
            await ctx.send("O bot só funciona das 19h às 2h!")
            return
        if ctx.voice_client is None:
            await ctx.send("O bot precisa estar em um canal de voz! Use !entrar.")
            return

        try:
            # Buscar no Spotify
            results = sp.search(q=musica, limit=1, type='track')
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                nome_musica = track['name']
                artista = track['artists'][0]['name']
                pesquisa = f"{nome_musica} {artista} instrumental"
            else:
                pesquisa = f"{musica} instrumental"

            # Buscar no YouTube
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': 'music.mp3',
                'default_search': 'ytsearch',
                'quiet': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(pesquisa, download=True)
                url = info['entries'][0]['url']

            # Reproduzir áudio
            ffmpeg_options = {'options': '-vn'}
            ctx.voice_client.play(discord.FFmpegPCMAudio('music.mp3', **ffmpeg_options))

            await ctx.send(f'Tocando: {pesquisa}')

            # Mostrar letra sincronizada
            for tempo, linha in LETRA.items():
                await asyncio.sleep(tempo)
                await ctx.send(linha)

        except Exception as e:
            print(f"Erro ao executar o comando karaoke: {e}")
            await ctx.send("Ocorreu um erro ao executar o comando karaoke.")

async def setup(bot):
    await bot.add_cog(Karaoke(bot))