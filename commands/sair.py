import discord
from discord.ext import commands

class Sair(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sair(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send('Saí do canal de voz.')
        else:
            await ctx.send('Não estou em um canal de voz.')

async def setup(bot):
    await bot.add_cog(Sair(bot))