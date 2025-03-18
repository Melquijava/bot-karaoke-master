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
sp = spotipy.Spotify(auth_manager=spotipy.SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

from config import LETRA

def bot_ativo():
    from datetime import datetime, time
    agora = datetime.now().time()
    inicio = time(19, 0)  # 19:00 (7 da noite)
    fim = time(2, 0)      # 02:00 (2 da madrugada)
    return inicio <= agora or agora <= fim

@commands.command()
async def karaoke(ctx, *, musica: str):
    if not bot_ativo():
        await ctx.send("O bot só funciona das 19h às 2h!")
        return
    if ctx.voice_client is None:
        await ctx.send("O bot precisa estar em um canal de voz! Use !entrar.")
        return
    
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
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(pesquisa, download=True)
            url = info['entries'][0]['url']

            # Caminho absoluto do arquivo
            caminho_absoluto = os.path.abspath('music.mp3')
            print(f"Caminho absoluto do arquivo: {caminho_absoluto}")

            # Verificar se o arquivo existe e tem tamanho maior que zero
            if os.path.exists(caminho_absoluto) and os.path.getsize(caminho_absoluto) > 0:
                print("Arquivo baixado com sucesso!")

                # Reproduzir áudio
                ffmpeg_options = {'options': '-vn'}
                ctx.voice_client.play(discord.FFmpegPCMAudio(caminho_absoluto, **ffmpeg_options))
                
                await ctx.send(f'Tocando: {pesquisa}')
                
                # Mostrar letra sincronizada
                for tempo, linha in LETRA.items():
                    await asyncio.sleep(tempo)
                    await ctx.send(linha)
            else:
                print("Erro: Arquivo não encontrado ou vazio após o download.")
                await ctx.send("Ocorreu um erro ao baixar ou encontrar o arquivo de áudio.")

    except Exception as e:
        print(f"Erro ao executar o comando karaoke: {e}")
        await ctx.send(f"Ocorreu um erro ao executar o comando karaoke: {e}")
        
def setup(bot):
    bot.add_command(karaoke)