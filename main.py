from itertools import cycle
import discord
from discord import activity
from discord.ext import commands, tasks
import random

#Variables globales a usar.
client = commands.Bot(command_prefix='$');

# <<-- EVENTOS -->> #

#Cuando el bot esta activo por primera vez.
@client.event
async def on_ready():
    print(f'Bot listo! {client.user.name} ON!');
    await client.change_presence(status = discord.Status.online);
    cambiarEstado.start();

#Cuando alguien se une a un servidor.
@client.event
async def on_member_join(user):
    print(f"{user} ha aterrizado en el servidor!");

#Cuando alguien abandona un servidor.
@client.event
async def on_member_remove(user):
    print(f"{user} ha abandonado el servidor :(");

# <<-- RUTINAS -->> #

mensajes = cycle(['$ayuda para lista de comandos.','$? para lista de comandos.'])

@tasks.loop(seconds = 30)
async def cambiarEstado():
    await client.change_presence(activity = discord.Game(next(mensajes)));


# <<-- COMANDOS -->> #

@client.command(aliases = ['ayuda','?'])
async def _ayuda(ctx):
    await ctx.send('**Lista de comandos actuales:**'+
                   '\nping : Devuelve la latencia actual del bot.' +
                   '\nanime : Sugerencia de un anime.' +
                   '\nborrar : Borra el numero epecificado del canal actual.' +
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

    await ctx.send(f'Te recomiendo el anime: *{random.choice(lista_animes)}*.');                    

#Comando para borrar mensajes de un canal.
@client.command()
async def borrar(ctx, cantidad = 2):
    await ctx.channel.purge(limit = cantidad);

#Comando para expulsar a alguien de un servidor.
@client.command()
async def kick(ctx, usuario : discord.Member, *, razon = 'Sin especificar.'):
    await usuario.kick(reason = razon);
    await ctx.send(f'{usuario.mention} ha sido expulsado del servidor.');

#Comando para banear a alguien de un servidor.
@client.command()
async def ban(ctx, usuario : discord.Member, *, razon = 'Sin especificar.'):
    await usuario.ban(reason = razon);
    await ctx.send(f'{usuario.mention} ha sido baneado del servidor.');

#Comando para desbanear a alguien de un servidor.
@client.command()
async def unban(ctx, *, usuario):
    lista_baneados = await ctx.guild.bans();

    for baneado in lista_baneados:
        us = baneado.user
        if(us.name == usuario):
            await ctx.guild.unban(us);
            await ctx.send(f'{usuario} ha sido desbaneado del servidor.');
            return

#Comando para encender el bot.
client.run('ODU5MzY0MzU1OTc5NjA4MDY0.YNrnbA.BLVtoKYapRDhoCUFe7Q_h4PanyA')