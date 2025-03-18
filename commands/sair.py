import discord
from discord.ext import commands
from datetime import datetime, time
from config import WORKING_HOURS_START, WORKING_HOURS_END

class Sair(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Cog Sair inicializado!")

    def is_within_working_hours(self):
        now = datetime.now().time()
        start_time = time(WORKING_HOURS_START, 0)
        end_time = time(WORKING_HOURS_END, 0)
        if WORKING_HOURS_START < WORKING_HOURS_END:
            return start_time <= now <= end_time
        else:  # Se cruza a meia-noite
            return start_time <= now or now <= end_time

    @commands.command()
    async def sair(self, ctx):
        if not self.is_within_working_hours():
            await ctx.send(f"O bot funciona das {WORKING_HOURS_START:02d}:00 às {WORKING_HOURS_END:02d}:00!")
            return
        try:
            if ctx.voice_client:
                await ctx.voice_client.disconnect()
                await ctx.send('Saí do canal de voz.')
            else:
                await ctx.send('Não estou em um canal de voz.')
        except Exception as e:
            print(f"Erro ao sair do canal de voz: {e}")
            await ctx.send(f"Ocorreu um erro ao sair do canal de voz. Erro: {e}")

async def setup(bot):
    await bot.add_cog(Sair(bot))