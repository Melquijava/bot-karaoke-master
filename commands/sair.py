import discord
from discord.ext import commands
from datetime import datetime, time

class Sair(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Cog Sair inicializado!")
        
    def bot_ativo(self):
        agora = datetime.now().time()
        inicio = time(19, 0)
        fim = time(2, 0)
        print(f"agora dentro do COG de sair!: {agora}")
        print(f"começando dentro do COG de sair: {inicio}")
        print(f"fim dentro do COG de sair: {fim}")
       
        ativo = inicio <= agora or agora <= fim
        print (ativo)
        return ativo
    
    @commands.command()
    async def horario_funcionamento(self, ctx):
         if self.bot_ativo():
            await ctx.send("O bot está funcionando nesse momento nesse horário ATIVO!!!!!")

         if not self.bot_ativo():
            await ctx.send("O bot nao está em horario de funcionamento, ATENÇÂO!!!!!")
   

    @commands.command()
    async def sair(self, ctx):
        print("Comando sair foi chamado!")

        if not self.bot_ativo():
            return await ctx.send("Horário de funcionamento do bot: 19:00 às 02:00!")

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
    print("Carregando Cog Sair...")
    await bot.add_cog(Sair(bot))
    print("Cog Sair carregado!")