import discord
from discord.ext import commands

class Sair(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Cog Sair inicializado!")

    @commands.command()
    async def sair(self, ctx):
        print("Comando sair foi chamado!")
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send('Saí do canal de voz.')
        else:
            await ctx.send('Não estou em um canal de voz.')

async def setup(bot):
    print("Carregando Cog Sair...")
    await bot.add_cog(Sair(bot))
    print("Cog Sair carregado!")