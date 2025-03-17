import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    raise EnvironmentError("A variável DISCORD_TOKEN deve estar definida no .env")

from config import PREFIX

# Crie um objeto Intents e especifique as intents que você precisa
intents = discord.Intents.default()
intents.members = True  # Habilita a Server Members Intent
intents.message_content = True  # Habilita a Message Content Intent (se precisar)
intents.presences = True  # Habilita a Presence Intent (se precisar)

# Inicialize o bot com as intents
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} está online!')

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
    await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())