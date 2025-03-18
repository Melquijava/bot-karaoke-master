import discord
from discord.ext import commands
import asyncio
import yt_dlp
import spotipy
import os
from dotenv import load_dotenv
from config import LETRA, PREFIX  # Importar LETRA e PREFIX do config.py
from datetime import datetime, time

load_dotenv()

# Recuperar tokens do .env
TOKEN = os.getenv('DISCORD_TOKEN')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

# Verificar se as variáveis de ambiente estão definidas
if not all([TOKEN, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET]):
    print("Erro: Variáveis de ambiente (DISCORD_TOKEN, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET) não estão definidas.")
    exit()

# Configurar Spotipy
sp = spotipy.Spotify(auth_manager=spotipy.SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# Inicializar o bot
bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())

def bot_ativo():
    agora = datetime.now().time()
    inicio = time(19, 0)  # 19:00 (7 da noite)
    fim = time(2, 0)      # 02:00 (2 da madrugada)
    return inicio <= agora or agora <= fim

@bot.event
async def on_ready():
    print(f'Bot {bot.user} está online!')

@bot.command()
async def karaoke(ctx, *, musica: str):
    try:
        if not bot_ativo():
            await ctx.send("O bot só funciona das 19h às 2h!")
            return
        if ctx.voice_client is None:
            await ctx.send("O bot precisa estar em um canal de voz! Use !entrar.")
            return

        print(f"Procurando a música: {musica}")

        # Buscar no Spotify
        results = sp.search(q=musica, limit=1, type='track')
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            nome_musica = track['name']
            artista = track['artists'][0]['name']
            pesquisa = f"{nome_musica} {artista} instrumental"
            print(f"Encontrada no Spotify: {pesquisa}")
        else:
            pesquisa = f"{musica} instrumental"
            print(f"Não encontrada no Spotify, procurando no YouTube por: {pesquisa}")

        # Configurar yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'music.mp3',
            'default_search': 'ytsearch',
            'quiet': True,
        }

        # Baixar música do YouTube
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(pesquisa, download=True)
                if 'entries' in info:
                    url = info['entries'][0]['url']
                else:
                    url = info['url']
                print(f"URL do vídeo: {url}")
        except Exception as e:
            print(f"Erro ao baixar a música do YouTube: {e}")
            await ctx.send("Erro ao baixar a música do YouTube.")
            return

        # Caminho absoluto do arquivo
        caminho_absoluto = os.path.abspath('music.mp3')
        print(f"Caminho absoluto do arquivo: {caminho_absoluto}")

        # Verificar se o arquivo existe e tem tamanho maior que zero
        if os.path.exists(caminho_absoluto) and os.path.getsize(caminho_absoluto) > 0:
            print("Arquivo baixado com sucesso!")

            # Reproduzir áudio
            ffmpeg_options = {'options': '-vn'}
            try:
                ctx.voice_client.play(discord.FFmpegPCMAudio(caminho_absoluto, **ffmpeg_options))

                await ctx.send(f'Tocando: {pesquisa}')

                # Mostrar letra sincronizada
                for tempo, linha in LETRA.items():
                    await asyncio.sleep(tempo)
                    await ctx.send(linha)
            except Exception as e:
                print(f"Erro ao reproduzir o áudio: {e}")
                await ctx.send("Erro ao reproduzir o áudio.")

        else:
            print("Erro: Arquivo não encontrado ou vazio após o download.")
            await ctx.send("Ocorreu um erro ao baixar ou encontrar o arquivo de áudio.")

    except Exception as e:
        print(f"Erro geral no comando karaoke: {e}")
        await ctx.send("Ocorreu um erro ao executar o comando karaoke.")

@bot.command()
async def entrar(ctx):
    if not bot_ativo():
        await ctx.send("O bot só funciona das 19h às 2h!")
        return
    if ctx.author.voice:
        canal = ctx.author.voice.channel
        await canal.connect()
        await ctx.send(f'Entrei no canal de voz: {canal}')
    else:
        await ctx.send('Você precisa estar em um canal de voz!')

@bot.command()
async def sair(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send('Saí do canal de voz.')
    else:
        await ctx.send('Não estou em um canal de voz.')

async def load_extensions():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'commands.{filename[:-3]}')
                print(f'Comando {filename} carregado: {filename}')
            except Exception as e:
                print(f'Erro ao carregar o comando {filename}: {e}')

async def main():
    await load_extensions()
    if TOKEN:  # Verificar se o token foi carregado corretamente
        await bot.start(TOKEN)
    else:
        print("Erro: Token do Discord não encontrado. Verifique o arquivo .env.")

if __name__ == '__main__':
    asyncio.run(main())