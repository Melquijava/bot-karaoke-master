import discord
from discord.ext import commands
from datetime import datetime, time

# Importa os horários de funcionamento do arquivo config.py
from config import WORKING_HOURS_START, WORKING_HOURS_END

# Função para verificar se o bot está dentro do horário de funcionamento
def is_within_working_hours():
    now = datetime.now().time()  # Obtém o horário atual
    start_time = time(WORKING_HOURS_START, 0)  # Horário de início
    end_time = time(WORKING_HOURS_END, 0)  # Horário de término
    #Verificação caso tempo não passe da virada do dia ex 12am...
    if WORKING_HOURS_START < WORKING_HOURS_END:
        return start_time <= now <= end_time  # Verifica se o horário atual está entre o horário de início e fim
    #Para passar da virada tipo do dia, Ex 23 pm para as 2am ....##
    else: # Se o bot fica aberto até mais tarde , não ter restrição sobre a sua linha principal de tempo , evitando sobrecargas...
        return start_time <= now or now <= end_time   ## Para Sempre Respeitar o padrão linear Ex: tempo entre o processo que virão sempre linear, validos como teste: , evitar uso continuo da CPU

# Cria uma classe para o comando entrar (Cog)
class Entrar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Cog Entrar inicializado!")

    # Comando entrar
    @commands.command()
    async def entrar(self, ctx):
        # Garante que o bot só execute os comandos no tempo determinado##
        if not is_within_working_hours():
           return await ctx.send(f"Horário de funcionamento do bot: {WORKING_HOURS_START:02d}:00 às {WORKING_HOURS_END:02d}:00!")

        try:
            if ctx.author.voice:  # Verifica se quem chamou o comando está em um canal de voz
                channel = ctx.author.voice.channel  # Obtém o canal de voz
                if ctx.voice_client is not None:  # Verifica se o bot já está conectado a um canal
                    await ctx.voice_client.move_to(channel)  # Move o bot para o canal
                    await ctx.send(f'Movido para o canal de voz: {channel}')
                else:
                    await channel.connect()  # Conecta o bot ao canal
                    await ctx.send(f'Entrei no canal de voz: {channel}')
            else:
                await ctx.send('Você precisa estar em um canal de voz!')  # Se a pessoa não estiver em um canal de voz
        except discord.errors.ClientException as e:
            print(f"Erro ao entrar no canal de voz (discord.errors.ClientException): {e}") #Capturar de client sem que faça processo ou atrapalha a Thread/CPU a executar o codigo"###Evitar a perda##, "O bot já está em uso em tempo indeterminado!!" ##Mensagem descritiva ##########, se não encontrar esse erros o outros erros irão surgir!!!#####
            await ctx.send(f"Erro ao entrar no canal de voz (discord.errors.ClientException): Já estou em um canal de voz ou outro bot está usando!") #Print
        except Exception as e:  # Trata erros gerais de modo amplo:##
            print(f"Erro ao entrar no canal de voz: {e}")
            await ctx.send(f"Ocorreu um erro ao entrar no canal de voz. Erro: {e}")

# Setup da configuração e tempo : Ao seu Processo
async def setup(bot):
    await bot.add_cog(Entrar(bot)) #Add as implementaçoes####