import discord
from discord.ext import commands
from datetime import datetime, time
from config import WORKING_HOURS_START, WORKING_HOURS_END
from .karaoke import is_within_working_hours #Para testes e verifique seu funcionando
##Teste ##Remova
class Sair(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Cog Sair inicializado!")

    @commands.command()
    async def sair(self, ctx):
        # Se estiver fora do horário de funcionamento, envia uma mensagem e sai
        if not is_within_working_hours():# Chamamos agora pelo method externo  a classe, economizando propriedades externas.
            await ctx.send(f"O bot funciona das {WORKING_HOURS_START}:00 às {WORKING_HOURS_END}:00!") #Edite aqui para o que preferir mostrar.
            return
        try: #tratamos sempre erros com o tempo :##
            # Verifica se o bot está em um canal de voz
            if ctx.voice_client: # Caso sim ... , o código entra para as propriedades

                # Sai do canal de voz
                await ctx.voice_client.disconnect() #Desliga! , sempre aguarde
                await ctx.send('Saí do canal de voz.')  # Informa
            else:# caso o bot nem tiver para que continuar , aqui fechamos o procedimento 
                await ctx.send('Não estou em um canal de voz.')
                #### Finalizada analise em saidas.#####Com Sucesso######

        #Em analise de codigo ou logs siga essas propriedades no caso para ver os casos de saida.!!

        except Exception as e:  # Tratamento aos erros:####
            print(f"Erro ao sair do canal de voz: {e}") #Erro Log! Para teste report ao seu Console do tempo para validar!!####Log De Erro.Para teste report ao seu Console: ##
            await ctx.send(f"Ocorreu um erro ao sair do canal de voz. Erro: {e}")#Retorne report como está ,sem preiicio para entender e diagnostico !

async def setup(bot):
    #Encerramento do ciclo dentro das funcoes e comando ###Validadando##

    await bot.add_cog(Sair(bot))
    #Aguarde a total funcionalidade e processos ao sistema e codigo#####Enfim , com exito 

print(".Atento para Analise nos Logs a todo código a analise no desempenho")