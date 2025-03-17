import discord
from discord.ext import commands

class Entrar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def entrar(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f'Entrei no canal de voz: {channel}')
        else:
            await ctx.send('Você precisa estar em um canal de voz!')

async def setup(bot):
    await bot.add_cog(Entrar(bot))

# faça um print para saber que esse arquivo foi executado
print('entrar.py foi executado!')