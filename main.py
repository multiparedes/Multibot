from itertools import cycle
import discord
from discord.ext import commands, tasks

import time
import random
import requests
import json

from requests.api import request

#Variables globales a usar.
with open('secret.env', 'r', encoding='utf-8') as secret:
    botToken = secret.read();

prefix = '$'
client = commands.Bot(command_prefix=prefix);
cgUrl = 'https://api.coingecko.com/api/v3'

# <<-- EVENTOS -->> #

#Cuando el bot esta activo por primera vez.
@client.event
async def on_ready():
    print(f'Bot listo! {client.user.name} ON!');
    await client.change_presence(status = discord.Status.online);
    cambiarEstado.start();

#Mensaje de bienvenida del bot a un servidor.
@client.event
async def on_guild_join(servidor):
    for channel in servidor.text_channels:
        if channel.permissions_for(servidor.me).send_messages:
            await channel.send(f'Hola soy **MultiBot**, encantado de estar en {servidor}! 🤙' +
            '\nEscribe $ayuda o $? para una lista con los comandos actuales.' +
            '\n*~ Bot aún en contrucción, para feedback Multiparedes#1982 <3*');
        break

@client.event
async def on_message(mem : discord.Message):
    if(mem.content.startswith(prefix)):
        if(mem.author.id != client.user.id):
            print(f'El usuario {mem.author.name} ha pedido el comando {mem.content}.')
            await client.process_commands(mem)

# <<-- RUTINAS -->> #
mensajes = cycle(['$ayuda para lista de comandos.','$? para lista de comandos.']);

@tasks.loop(seconds = 30)
async def cambiarEstado():
    await client.change_presence(activity = discord.Game(next(mensajes)));

# <<-- COMANDOS -->> #

@client.command(aliases = ['ayuda','?'])
async def _ayuda(ctx):
    await ctx.send('**Lista de comandos actuales:**'+
                   '\nping : Devuelve la latencia actual del bot.' +
                   '\nanime : Sugerencia de un anime.' +
                   '\nborrar : Borra el numero especificado de mensajes del canal actual.' +
                   '\nnuke : Borra todos los mensajes del canal actual.' +
                   '\ncn : Chistes de Chuck Norris en Ingles.'
                   '\nprecio : Devuelve el precio de la criptomoneda en euros y dolares.'
                   '\n**Comandos de administrador (rol Admin):**'
                   '\nkick : Expulsa a un usuario del servidor.' +
                   '\nban : Banea a un usuario del servidor.' +
                   '\nunban : Desbanea a un usuario del servidor.')              

#Comando para ver si el bot esta activo y la latencia del mismo.
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency*1000)}ms');

#Comando que devuelve un anime random de una lista.
@client.command()
async def anime(ctx):
    lista_animes = ['Naruto','Naruto Shippuden','Boruto','Hunter X Hunter'
                    ,'One Piece','Demon Slayer','Black Clover','Bleach'];
                 
    await ctx.send(f'Te recomiendo el anime: *{random.choice(lista_animes)}*.')             

#Comando para borrar mensajes de un canal.
@client.command()
async def borrar(ctx, cantidad : int):
    await ctx.channel.purge(limit = cantidad);

@borrar.error
async def borrar_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Debes introducir el número de mensajes a borrar.\nEjemplo: *$borrar 20*')
        return
    
#Comando para expulsar a alguien de un servidor.
@client.command()
@commands.has_role('Admin')
async def kick(ctx, usuario : discord.Member, *, razon = 'Sin especificar.'):
    await usuario.kick(reason = razon);
    await ctx.send(f'{usuario.mention} ha sido expulsado del servidor.');

#Manjeo de excepciones, muestra el correcto uso del comando kick.
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Debes introducir el nombre del usuario a expulsar.\nEjemplo: *$kick multiparedes*')
        return

#Comando para banear a alguien de un servidor.
@client.command()
@commands.has_role('Admin')
async def ban(ctx, usuario : discord.Member, *, razon = 'Sin especificar.'):
    await usuario.ban(reason = razon);
    await ctx.send(f'{usuario.mention} ha sido baneado del servidor.');

#Manjeo de excepciones, muestra el correcto uso del comando ban.
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Debes introducir el nombre del usuario a banear.\nEjemplo: *$ban multiparedes*')
        return

#Comando para desbanear a alguien de un servidor.
@client.command()
@commands.has_role('Admin')
async def unban(ctx, *, usuario):
    lista_baneados = await ctx.guild.bans();

    encontrado = False;

    for baneado in lista_baneados:
        us = baneado.user
        if(us.name == usuario):
            await ctx.guild.unban(us);
            await ctx.send(f'{usuario} ha sido desbaneado del servidor.');
            encontrado = True;
            return

    if(encontrado == False):
        await ctx.send(f'No se ha encontrado al usuario {usuario} en la lista de baneados.');

#Manjeo de excepciones, muestra el correcto uso del comando unban.
@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Debes introducir el nombre del usuario a desbanear.\nEjemplo: *$unban multiparedes*')
        return

#Comando para borrar un canal entero.
@client.command()
async def nuke(ctx):

    await ctx.send('NUKE EN 3 ...');
    time.sleep(1)
    await ctx.send('2...')    
    time.sleep(1)
    await ctx.send('1...')
    time.sleep(1)
    await ctx.channel.purge(limit = 2147483647);

#Comando para chiste random de Chuck Norris usando una api 👌
@client.command()
async def cn(ctx):
    url = 'https://api.chucknorris.io/jokes/random'

    raw_response = requests.get(url)
    json_reponse = json.loads(raw_response.text)

    await ctx.send(json_reponse['value'])

@client.command()
async def precio(ctx, *, moneda = 'Bitcoin'):
    parametros = f'?ids={moneda}&vs_currencies=eur%2Cusd'

    incluirCambio24h = True;
    if(incluirCambio24h):
        parametros = parametros + f'&include_24hr_change=true'

    precio_raw = requests.get(cgUrl+'/simple/price'+parametros)
    precio = json.loads(precio_raw.text)

    if(len(precio) == 0):
        await ctx.send('Moneda no encontrada, debes poner el nombre de la criptomoneda no su simbolo.')
        return

    mensaje = f"{moneda} esta actualmente a {precio[moneda.lower()]['eur']}€, cambio a dolares: {precio[moneda.lower()]['usd']}$.\n"

    if(incluirCambio24h):
        if(precio[moneda.lower()]['eur_24h_change'] >= 0):
            emoji = '👍🏼';
        else:
            emoji = '👎🏼';    

        mensaje = mensaje + f"El cambio en las últimas 24h ha sido del {round(precio[moneda.lower()]['eur_24h_change'],2)}% {emoji}. "

    await ctx.send(mensaje)

#Comando para encender el bot.
client.run(botToken)