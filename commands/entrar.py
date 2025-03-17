import discord
from discord.ext import commands

class Entrar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Cog Entrar inicializado!")  # Log para depuração

    @commands.command()
    async def entrar(self, ctx):
        print("Comando entrar foi chamado!")  # Log para depuração
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f'Entrei no canal de voz: {channel}')
        else:
            await ctx.send('Você precisa estar em um canal de voz!')

async def setup(bot):
    print("Carregando Cog Entrar...")  # Log para depuração
    await bot.add_cog(Entrar(bot))
    print("Cog Entrar carregado!")  # Log para depuração

# faça um print para saber que esse arquivo foi executado
print('entrar.py foi executado!')