import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém o token do Discord do arquivo .env
TOKEN = os.getenv('DISCORD_TOKEN')

# Verifica se o token foi definido
if TOKEN is None:
    raise EnvironmentError("A variável DISCORD_TOKEN deve estar definida no .env")

# Importa o prefixo do bot do arquivo config.py
from config import PREFIX

# Define as permissões que o bot precisa ter
intents = discord.Intents.default()
intents.members = True  # Precisa para acessar informações de membros do servidor
intents.message_content = True  # Precisa para ler o conteúdo das mensagens
intents.presences = True  # Permite que o bot veja o status dos usuários
intents.voice_states = True #Permite reconhecer usuários no canal de Voz (Precisa)

# Cria o bot
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Evento chamado quando o bot fica online
@bot.event
async def on_ready():
    print(f'Bot {bot.user} está online!')

# Função para carregar os comandos do bot
async def load_extensions():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'commands.{filename[:-3]}')  # Carrega o comando
                print(f'Cog {filename} carregado: {filename}')  # Mensagem de sucesso
            except Exception as e:
                print(f'Erro ao carregar o cog {filename}: {e}')  # Mensagem de erro

# Função principal do bot
async def main():
    await load_extensions()  # Carrega os comandos
    await bot.start(TOKEN)  # Inicia o bot

# Executa a função principal
if __name__ == '__main__':
    asyncio.run(main())