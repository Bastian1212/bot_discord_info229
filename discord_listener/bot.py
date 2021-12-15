import os

import discord
from discord import message
from dotenv import load_dotenv
from discord.ext import commands
import threading
import pika
import descargar_musica 
import complementos
import youtube_dl


############ CONEXION RABBITMQ ##############

HOST = os.environ['RABBITMQ_HOST']
print("rabbit:"+HOST)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=HOST))
channelMQ = connection.channel()


#Creamos el exchange 'cartero' de tipo 'fanout'
channelMQ.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)



#############################################

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

    for channel in bot.get_all_channels():
        print(channel)
        print(channel.id)

    channel = bot.get_channel(920687216022417408)
    ###await channel.send('¡Hola!')



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == 'pizza' or message.content == 'cerveza' or message.content == 'donuts':
        response = "!mmm..."+message.content+"!"
        await message.channel.send(response)

    await bot.process_commands(message)

@bot.command(name='birthday', help='Muestra la fecha de cumpleaño del miembro de la GUILD que se pasa en parámetro. Ejemplo: !birthday MatthieuVernier')
async def cumpleaños(ctx):
    message =  ctx.message.content
    print("send a new mesage to rabbitmq: "+message)

    channelMQ.basic_publish(exchange='cartero', routing_key="birthday", body=message)

@bot.command(name='add-birthday', help='Permite añadir el cumpleaño de un nuevo miembro de la GUILD que se pasa en parámetro. Ejemplo: !birthday MatthieuVernier 1985-02-13')
async def cumpleaños(ctx):
    message =  ctx.message.content
    print("send a new mesage to rabbitmq: "+message)
    channelMQ.basic_publish(exchange='cartero', routing_key="birthday", body=message)












####### Musica ####################################

@bot.command()
async def play(ctx, url : str):


    bol = descargar_musica.descargaMusic(url)
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='general')
    await voiceChannel.connect()
    voice = discord.utils.get(bot.voice_clients)


    

    


    
    if bol == True:
        voice.play(discord.FFmpegPCMAudio("song.mp3"))

       
    else: 
        await ctx.send("Ocurrio un Error..... :( ")
    

############################################################



###### Imagen de google ##########


@bot.command(aliases=["show"])
async def showpic(ctx, *, search):
    
    url = complementos.buscarImagen(search)
    
    embed1 = discord.Embed(title=f"Imagen de {search} ")
    embed1.set_image(url=url)
    await ctx.send(embed=embed1)

###################################################################

##################wiki#############################################


@bot.command(aliases=["wiki"])
async def wikiS(ctx, *, search):
    
    message =  search
    print("send a new mesage to rabbitmq: "+message)

    channelMQ.basic_publish(exchange='cartero', routing_key="wiki", body=message)
    await ctx.send("a")
    ##embed1 = discord.Embed(title=f" {search} ", description=f" {respuesta}" )
    ##await ctx.send(embed=embed1)



############ CONSUMER ###############

import threading
import asyncio

def writer(bot):
    """thread worker function"""
    print('Worker')

    HOST = os.environ['RABBITMQ_HOST']

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST))
    channelMQ = connection.channel()

    #Creamos el exchange 'cartero' de tipo 'fanout'
    channelMQ.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)

    #Se crea un cola temporaria exclusiva para este consumidor (búzon de correos)
    result = channelMQ.queue_declare(queue="discord_writer", exclusive=True, durable=True)
    queue_name = result.method.queue

    #La cola se asigna a un 'exchange'
    channelMQ.queue_bind(exchange='cartero', queue=queue_name, routing_key="discord_writer")


    print(' [*] Waiting for messages. To exit press CTRL+C')

    async def write(message):
        #channel = bot.get_channel(908505071887732768)#913706828502814760
        channel = bot.get_channel(920687216022417408)
        mens = message.split("$")
        if(len(mens)==3):
            embed = discord.Embed(
                title=mens[0],
                description=mens[2],
            )

            embed.set_image(url=mens[1])
            await channel.send(embed=embed)
        else:
            await channel.send(message)

    def callback(ch, method, properties, body):
        message=body.decode("UTF-8")
        print(message)

        bot.loop.create_task(write(message))

    channelMQ.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channelMQ.start_consuming()

t = threading.Thread(target=writer, args=[bot])
t.start()

########################################
bot.run(TOKEN)