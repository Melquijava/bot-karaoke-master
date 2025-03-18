import discord
from discord.ext import commands
from datetime import datetime, time

class Entrar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Cog Entrar inicializado!")

    def bot_ativo(self):
        agora = datetime.now().time()
        inicio = time(19, 0)
        fim = time(2, 0)
         
        print(f"agora dentro do COG de entrar!: {agora}")
        print(f"começando dentro do COG de entrar: {inicio}")
        print(f"fim dentro do COG de entrar: {fim}")
       

        ativo = inicio <= agora or agora <= fim
        return ativo

    @commands.command()
    async def horario_funcionamento(self, ctx):
         if self.bot_ativo():
            await ctx.send("O bot está funcionando nesse momento nesse horário ATIVO!")
         if not self.bot_ativo():
            await ctx.send("O bot nao está em horario de funcionamento, ATENÇÂO")

    @commands.command()
    async def entrar(self, ctx):
        print("Comando entrar foi chamado!")

        if not self.bot_ativo():
            return await ctx.send("Horário de funcionamento do bot: 19:00 às 02:00!")
        
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
    print("Carregando Cog Entrar...")
    await bot.add_cog(Entrar(bot))
    print("Cog Entrar carregado!")