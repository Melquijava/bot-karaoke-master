import discord
from discord.ext import commands
from datetime import datetime, time
from config import WORKING_HOURS_START, WORKING_HOURS_END

class Entrar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Cog Entrar inicializado!")

    def is_within_working_hours(self):
        now = datetime.now().time()
        start_time = time(WORKING_HOURS_START, 0)
        end_time = time(WORKING_HOURS_END, 0)
        if WORKING_HOURS_START < WORKING_HOURS_END:
            return start_time <= now <= end_time
        else:  # Se cruza a meia-noite
            return start_time <= now or now <= end_time

    @commands.command()
    async def entrar(self, ctx):
        if not self.is_within_working_hours():
            await ctx.send(f"O bot funciona das {WORKING_HOURS_START:02d}:00 às {WORKING_HOURS_END:02d}:00!")
            return
        try:
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                if ctx.voice_client is not None:
                    await ctx.voice_client.move_to(channel)
                    await ctx.send(f'Movido para o canal de voz: {channel}')
                else:
                    await channel.connect()
                    await ctx.send(f'Entrei no canal de voz: {channel}')
            else:
                await ctx.send('Você precisa estar em um canal de voz!')
        except discord.errors.ClientException as e:
            print(f"Erro ao entrar no canal de voz (discord.errors.ClientException): {e}")
            await ctx.send(f"Erro ao entrar no canal de voz (discord.errors.ClientException): Já estou em um canal de voz ou outro bot está usando!")
        except Exception as e:
            print(f"Erro ao entrar no canal de voz: {e}")
            await ctx.send(f"Ocorreu um erro ao entrar no canal de voz. Erro: {e}")

async def setup(bot):
    await bot.add_cog(Entrar(bot))