"""
# Inicio Importações
from discord.ext.commands import MissingPermissions
import json
"""
import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import AutoShardedBot
import asyncio
import pymysql
import pymysql.cursors


# Pegar Token


def read_token():
    with open("magnet_token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()

# modulos = ["cogs.comandos", "cogs.error_handler"]
modulos = ["cogs.comandos", "cogs.error_handler"]

# Def para os prefixos


def get_prefix(bot, message):
    try:
        db = pymysql.connect(
            host='192.168.0.254',
            user='u500424113_sas',
            password='S4SsW4PH4@K7D*R4SsW4PH4@K7D*',
            db='magnetroles',
            cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()

        server_id = message.guild.id

        cursor.execute(f"SELECT server_prefix FROM `d_servers` WHERE server_id = '{server_id}'")
        s_prefix = cursor.fetchone()
        cursor.close()
        db.close()
        if s_prefix is not None:
            prefixes = str(s_prefix['server_prefix'])
            return prefixes
        else:
            prefixes = 'mr'
            return prefixes

    except Exception as e:
        print(e)
        prefixes = 'mr'
        return prefixes
# fim def


bot = AutoShardedBot(command_prefix=get_prefix, case_insensitive=True)
# bot.remove_command('help')


"""
@bot.listen("on_command_error")
async def error_handler(ctx, error):
    # Testar colocar esses error no arquivo error_handler.py
    error = getattr(error, 'original', error)
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("O Bot não tem permissão para adicionar ou remover todos os cargos.\n"
                       "Coloque o cargo do BOT acima de todos os cargos que o BOT pode adicionar e remover.")

    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem direitos para este comando.")
        # await ctx.message.delete()

    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Comando inválido.")
        await ctx.message.delete()

    elif isinstance(error, discord.Forbidden):
        await ctx.send(f"Alguém tentou adicionar ou remover um cargo, mas não tenho permissão para fazer isso.\n"
                       f"Certifique-se de que tenho um cargo de hierarquia mais alta do que o cargo que devo "
                       f"adicionar ou remover e de que tenho a permissão para `Gerenciar cargos`.")
    elif isinstance(error, discord.errors.Forbidden):
        await ctx.send("Não é permitido fazer isso.")

    if isinstance(error, commands.CommandOnCooldown):
        s = error.retry_after
        s = round(s, 2)
        h, r = divmod(int(s), 3600)
        m, s = divmod(r, 60)
        return await ctx.send(f'Cooldown você precisa esperar **{str(h) + "h : " if h != 0 else ""}{str(m) + "m : " if m != 0 else ""}{str(s) + "s" if s != 0 else ""}** para usar esse comando novamente.')
# """


@bot.event
async def on_ready():
    print('-=-' * 24)
    print(f"BOT: {bot.user.name} | Online.")
    print(f"ID: {bot.user.id}")
    print('-=-' * 10, '[ Vortex ]', '-=-' * 10)
    print('-=-' * 9, '[ Imã de Cargos ]', '-=-' * 9)

    while True:
        await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name='Imã de Cargos'))
        await asyncio.sleep(300)
        await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name='Magnetic of Roles'))
        await asyncio.sleep(300)


@bot.event
async def on_guild_join(guild):
    try:
        db = pymysql.connect(
            host='192.168.0.254',
            user='u500424113_sas',
            password='S4SsW4PH4@K7D*R4SsW4PH4@K7D*',
            db='magnetroles',
            cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()

        server_id = guild.id
        server_name = guild.name

        cursor.execute(f"SELECT * FROM `d_servers` WHERE server_id = '{server_id}'")
        row = cursor.fetchone()

        if row is None:
            sql = "INSERT INTO `d_servers` (server_id, server_nome, server_prefix, server_ativo) VALUES(%s,%s,%s,%s)"
            val = (server_id, server_name, 'mr', 'yes')
            cursor.execute(sql, val)

            db.commit()
            cursor.close()
            db.close()
        else:
            cursor.execute(f"UPDATE `d_servers` SET server_ativo = 'yes', server_nome = '{server_name}' "
                           f"WHERE server_id = '{server_id}'")
            db.commit()
            cursor.close()
            db.close()

    except Exception as e:
        print(e)


@bot.event
async def on_guild_remove(guild):
    try:
        db = pymysql.connect(
            host='192.168.0.254',
            user='u500424113_sas',
            password='S4SsW4PH4@K7D*R4SsW4PH4@K7D*',
            db='magnetroles',
            cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()

        server_id = guild.id
        server_name = guild.name

        cursor.execute(f"SELECT * FROM `d_servers` WHERE server_id = '{server_id}'")
        row = cursor.fetchone()

        if row is not None:
            cursor.execute(f"UPDATE `d_servers` SET server_ativo = 'no', server_nome = '{server_name}' "
                           f"WHERE server_id = '{server_id}'")
            db.commit()
            cursor.close()
            db.close()
        else:
            cursor.close()
            db.close()

    except Exception as e:
        print(e)


@bot.event
async def on_message(message):
    if message.content.startswith('!teste'):
        return
    if message.author == bot.user:
        return
    if message.author.bot:
        return
    await bot.process_commands(message)


@bot.event
async def premium_guild_subscription(ctx):
    # https://discordpy.readthedocs.io/en/latest/api.html#discord.MessageType.premium_guild_subscription
    # https://stackoverflow.com/questions/65385757/get-the-number-of-boosts-in-a-server-discord-py
    server = ctx.guild
    user_booster = server.premium_subscribers
    channel = bot.get_channel(608343855359852566)
    channel.send(f"**{user_booster}** fez um novo Server Boost nesse Discord.\n"
             f"Totalizando **{server.premium_subscription_count}** no {server.name}\n"
             f"Obrigado {user_booster.name} pelo seu apoio!")


'''@commands.guild_only()
@bot.command()
async def creator(ctx):
    """
    Meu criador: VORTEX
    """
    if ctx.author.id == 136933432973459457:
        return await ctx.send(f"Olá meu criador. ❤️")
    return await ctx.send(f"Meu criador se chama: VORTEX\n"
                          f"_Ele não quer ser incomodado então só irei informar o Nick_.")'''


@commands.guild_only()
@bot.command(name='limpar', aliases=['nuke', 'apagar', 'clear'])
async def clean(ctx, amount: int):
    """
    Comando para apagar o histórico de um chat. Limite de 1000
    """
    if ctx.author.guild_permissions.administrator:
        amount = amount + 1
        if amount <= 1001:
            return await ctx.channel.purge(limit=amount)
        elif amount >= 1001:
            amount = 1001
            return await ctx.channel.purge(limit=amount)


@clean.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Por favor informe uma quantidade de mensagens para deletar.')


if __name__ == "__main__":
    for modulo in modulos:
        bot.load_extension(modulo)

    bot.run(token)

"""
1 - Colocar o comando ima de carogs no On user join =D
on_member_join
"""
