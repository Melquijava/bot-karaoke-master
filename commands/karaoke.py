import discord
from discord.ext import commands
import asyncio
import yt_dlp
import spotipy
import os
from dotenv import load_dotenv
from config import LETRA, WORKING_HOURS_START, WORKING_HOURS_END
from datetime import datetime, time

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

def is_within_working_hours():
    """Verifica se o horário atual está dentro do horário de funcionamento do bot."""
    now = datetime.now().time()
    start_time = time(WORKING_HOURS_START, 0)
    end_time = time(WORKING_HOURS_END, 0)
    if WORKING_HOURS_START < WORKING_HOURS_END:
        return start_time <= now <= end_time
    else:
        return start_time <= now or now <= end_time

class Karaoke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spotify = None  # Inicializa o cliente Spotify como None
        if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET:
            try:
                self.spotify = spotipy.Spotify(auth_manager=spotipy.SpotifyClientCredentials(
                    client_id=SPOTIFY_CLIENT_ID,
                    client_secret=SPOTIFY_CLIENT_SECRET
                ))
                print("Cliente Spotify inicializado com sucesso.")
            except Exception as e:
                print(f"Erro ao inicializar o cliente Spotify: {e}")
        else:
            print("Aviso: As variáveis SPOTIFY_CLIENT_ID e SPOTIFY_CLIENT_SECRET não estão definidas. O bot não poderá usar o Spotify.")

    @commands.command()
    async def karaoke(self, ctx, *, musica: str):
        """Toca uma música de karaokê no canal de voz."""

        if not is_within_working_hours():
            await ctx.send(f"O bot funciona das {WORKING_HOURS_START:02d}:00 às {WORKING_HOURS_END:02d}:00!")
            return

        if not ctx.author.voice:
            await ctx.send("Você precisa estar em um canal de voz para usar este comando.")
            return

        if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
            await ctx.send("As variáveis SPOTIFY_CLIENT_ID e SPOTIFY_CLIENT_SECRET não estão configuradas. A busca no Spotify não estará disponível.")

        try:
            await ctx.send(f"Procurando a música: {musica}")

            # Tentar buscar a música no Spotify
            pesquisa = musica  # Inicializa com a pesquisa original
            if self.spotify:
                try:
                    results = self.spotify.search(q=musica, limit=1, type='track')
                    if results['tracks']['items']:
                        track = results['tracks']['items'][0]
                        nome_musica = track['name']
                        artista = track['artists'][0]['name']
                        pesquisa = f"{nome_musica} {artista} instrumental"
                        await ctx.send(f"Encontrada no Spotify: {nome_musica} - {artista}")
                    else:
                        await ctx.send("Não encontrada no Spotify, procurando no YouTube...")
                except Exception as e:
                    print(f"Erro ao buscar no Spotify: {e}")
                    await ctx.send("Erro ao buscar no Spotify. Tentando no YouTube...")

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

async def setup(bot):
    await bot.add_cog(Karaoke(bot))