import discord
from discord.ext import commands, tasks

from itertools import cycle
import time
import requests
import json

#Variables globales a usar.
with open('secret.env', 'r', encoding='utf-8') as secret:
    botToken = secret.read();

prefix = '$'
client = commands.Bot(command_prefix=prefix);
cgUrl = 'https://api.coingecko.com/api/v3'
cnUrl = 'https://api.chucknorris.io/jokes/random'

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
    print(f'{client.user.name} ha sido añadido a {servidor}.')
    for channel in servidor.text_channels:
        if channel.permissions_for(servidor.me).send_messages:
            await channel.send(f'Hola soy **MultiBot**, encantado de estar en {servidor}! 🤙' +
            '\nEscribe $ayuda o $? para una lista con los comandos actuales.' +
            '\n*~ Bot aún en contrucción, para feedback Multiparedes#1982 <3*');
        break

#Muestra por consola los comandos que se le piden al bot.
@client.event
async def on_message(mem : discord.Message):
    if(mem.content.startswith(prefix)):
        if(mem.author.id != client.user.id):
            print(f'El usuario {mem.author.name} ha pedido el comando {mem.content}.')
            await client.process_commands(mem)

# <<-- RUTINAS -->> #
mensajes = cycle(['$ayuda para lista de comandos.','$? para lista de comandos.']);

#Rutina para cambiar el estado del bot.
@tasks.loop(seconds = 30)
async def cambiarEstado():
    await client.change_presence(activity = discord.Game(next(mensajes)));

# <<-- COMANDOS -->> #

#Comando de ayuda.
@client.command(aliases = ['ayuda','?'])
async def _ayuda(ctx):
     
    mensaje_ayuda = discord.Embed(title = 'Lista de comandos actuales :', color = discord.Color.teal());             
    
    contenido_vario = '''ayuda : Muestra este mensaje.
                        \u200bping : Devuelve la latencia actual del bot.
                        \u200bborrar : Borra el numero especificado de mensajes del canal actual.
                        \u200bnuke : Borra todos los mensajes del canal actual.
                        \u200bnick : Comando para poner un nick a algun usuario.
                        \u200bunnick : Comando para quitar el nick a algun usuario.                        
                        \u200bprecio : Devuelve el precio de la criptomoneda en euros y dolares.'''

    mensaje_ayuda.add_field(name = 'Comandos varios', value = contenido_vario, inline= False)

    contenido_admin = '''kick : Expulsa a un usuario del servidor.
                        \u200bban : Banea a un usuario del servidor.
                        \u200bunban : Desbanea a un usuario del servidor.'''

    mensaje_ayuda.add_field(name = 'Comandos de administrador (necesario rol Admin)', value = contenido_admin, inline= False)                    
    mensaje_ayuda.add_field(name = f'Nota: Para todos los comandos necesitas poner el prefijo {prefix} delante.', value = '*[Link al codigo fuente del bot.](https://github.com/multiparedes/cositasBot)*', inline= False)
    mensaje_ayuda.set_footer(text = '~ Bot aún en contrucción, para feedback Multiparedes#1982 <3')

    await ctx.send(embed = mensaje_ayuda)
    
#Comando para ver si el bot esta activo y la latencia del mismo.
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency*1000)}ms');          

#Comando para borrar mensajes de un canal.
@client.command()
async def borrar(ctx, cantidad : int):
    await ctx.channel.purge(limit = cantidad);

@borrar.error
async def borrar_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Debes introducir el número de mensajes a borrar.\nEjemplo: *$borrar 20*')
        return
    
#Comando para borrar un canal entero.
@client.command()
async def nuke(ctx):

    msg = await ctx.send('Estas seguro de que quieres borrar TODOS los mensajes de este canal?')
    await msg.add_reaction('✔')
    await msg.add_reaction('❌')

    await ctx.send('NUKE EN 3 ...');
    time.sleep(1)
    await ctx.send('2...')    
    time.sleep(1)
    await ctx.send('1...')
    time.sleep(1)
    await ctx.channel.purge(limit = 2147483647);

#Comando para poner un nick a algun usuario.
@client.command()
async def nick(ctx, usuario : discord.Member, *,nuevo_nombre):
    await ctx.send(f"{usuario.display_name.capitalize()} ha sido bendecido como '**{nuevo_nombre}**'.")
    await usuario.edit(nick = nuevo_nombre)

@nick.error
async def nick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Debes introducir el nombre del usuario y el nick.\nEjemplo: *$nick @multiparedes rastaman*')

#Comando para quitar un nick a algun usuario (en caso de tener alguno).
@client.command()
async def unnick(ctx, usuario: discord.Member):
    if(usuario.display_name == usuario.name):
        await ctx.send(f'{usuario.display_name.capitalize()} no posee ningún nick.')
        return

    await ctx.send(f'{usuario.display_name.capitalize()} ha recuperado su nombre original.')    
    await usuario.edit(nick = usuario.name)

@unnick.error
async def unnick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Debes introducir el nombre del usuario a quitar el nick.\nEjemplo: *$unnick @multiparedes*')

#Comando ponde dado una criptomoneda te devuelve el precio y el cambio 24h.
@client.command(aliases = ['precio','price'])
async def _precio(ctx, moneda = 'Bitcoin'):
    parametros = f'?ids={moneda}&vs_currencies=eur%2Cusd'
    urlCG = f'https://www.coingecko.com/es/monedas/{moneda.lower()}'

    incluirCambio24h = True;
    if(incluirCambio24h):
        parametros = parametros + f'&include_24hr_change=true'

    precio_raw = requests.get(cgUrl+'/simple/price'+parametros)
    precio = json.loads(precio_raw.text)

    if(len(precio) == 0):
        await ctx.send('Moneda no encontrada, debes poner el nombre de la criptomoneda no su simbolo.')
        return

    mensaje_precio = discord.Embed(title = f"Precio actual de {moneda.capitalize()}")

    mensaje_precio.description = f"Precio actual en euros : {precio[moneda.lower()]['eur']}€.\nPrecio actual en dolares : {precio[moneda.lower()]['eur']}$"  
    
    if(incluirCambio24h):
        if(precio[moneda.lower()]['eur_24h_change'] >= 0):
            emoji = '👍🏼';
            mensaje_precio.color = discord.Color.green();
        else:
            emoji = '👎🏼';                
            mensaje_precio.color = discord.Color.red();

        mensaje_precio.add_field(name = 'Cambio últimas 24h:',value = f"El cambio en las últimas 24h ha sido del {round(precio[moneda.lower()]['eur_24h_change'],2)}% {emoji}.")

    mensaje_precio.set_footer(text = f'{urlCG}', icon_url = 'https://static.coingecko.com/s/thumbnail-007177f3eca19695592f0b8b0eabbdae282b54154e1be912285c9034ea6cbaf2.png')

    await ctx.send(embed = mensaje_precio)

# <<-- COMANDOS DE ADMIN -->>

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
        await ctx.send('Debes introducir el nombre del usuario a expulsar.\nEjemplo: *$kick @multiparedes*')
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
        await ctx.send('Debes introducir el nombre del usuario a banear.\nEjemplo: *$ban @multiparedes*')
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

#Comando para encender el bot.
client.run(botToken)