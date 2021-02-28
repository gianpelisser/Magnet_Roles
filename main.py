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
import locales.pt_br
import locales.en

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
            host='127.0.0.1',
            user='usuario',
            password='Senha-password',
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


intents = discord.Intents.default()
intents.members = True

# bot = AutoShardedBot(command_prefix=get_prefix, case_insensitive=True, intents=discord.Intents.all())
bot = AutoShardedBot(command_prefix=get_prefix, case_insensitive=True, intents=intents)
# bot.remove_command('help')


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
async def on_member_join(member):
    guild = member.guild
    try:
        db = pymysql.connect(
            host='127.0.0.1',
            user='usuario',
            password='Senha-password',
            db='magnetroles',
            cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()

        server_id = guild.id
        cursor.execute(f"SELECT on_member_join FROM d_servers WHERE server_id = '{server_id}'")
        rowserver = cursor.fetchone()
        member_join = rowserver['on_member_join']
        cursor.close()
        db.close()
        if member_join == 'no':
            return
    except:
        return
    try:
        if guild.system_channel is not None:
            to_send = f"Bem Vindo(a) {member.mention} | Discord Server: {guild.name}!"
            await guild.system_channel.send(to_send)
            try:
                db = pymysql.connect(
                    host='127.0.0.1',
                    user='usuario',
                    password='Senha-password',
                    db='magnetroles',
                    cursorclass=pymysql.cursors.DictCursor)
                cursor = db.cursor()

                cursor.execute(f"SELECT id_server FROM `d_servers` WHERE server_id = '{guild.id}'")
                row_id = cursor.fetchone()
                id_server = row_id['id_server']

                cursor.execute(f"SELECT * FROM d_roles WHERE discord_id = '{member.id}' "
                               f"and user_ban = 'yes' or role_ban = 'yes'")
                rows_role_banned_from_user = cursor.fetchall()

                user_is_ban = 'no'
                role_ban_list = []
                if rows_role_banned_from_user is not None:
                    await guild.system_channel.send(f"Os cargos que o(a) **{member.mention}** não pode receber são:\n"
                                   f"||_Ou não tem cargos para adicionar._||")
                    sayonetime = 1
                    for row_ur_ban in rows_role_banned_from_user:
                        user_ban = row_ur_ban['user_ban']
                        role_ban = row_ur_ban['role_ban']
                        if user_ban == 'yes':
                            user_is_ban = 'yes'
                            if sayonetime == 1:
                                await guild.system_channel.send(f"Desculpe **{member.mention}**. Você está proibido de usar esse comando.")
                            sayonetime += 1

                        if role_ban == 'yes':
                            role_ban_list.append(row_ur_ban['role_id'])
                            roleban = discord.utils.get(guild.roles, id=row_ur_ban['role_id'])
                            await guild.system_channel.send(f"Cargo _Bloqueado_: {roleban}")

                if user_is_ban == 'yes':
                    return

                cursor.execute(f"SELECT * FROM d_roles_adm WHERE id_server = '{id_server}' and role_can_use = 'no'")
                rows_role_adm = cursor.fetchall()
                roles_adm_list = []
                if rows_role_adm is not None:
                    for roles in rows_role_adm:
                        roles_adm_list.append(roles['role_id_adm'])

                cursor.execute(
                    f"SELECT role_id FROM `d_roles` WHERE discord_id = '{member.id}' and id_server = '{id_server}'")
                row_user = cursor.fetchall()

                if row_user is not None:
                    for row in row_user:
                        role_id = row['role_id']

                        roleadd = discord.utils.get(guild.roles, id=role_id)
                        if not roleadd in member.roles:
                            for role in guild.roles:
                                if role.id == role_id:
                                    if not role == guild.default_role:
                                        if not role.id in role_ban_list:
                                            if not role.id in roles_adm_list:
                                                try:
                                                    await member.add_roles(roleadd, reason='BOT: Magnetic of Role')
                                                except discord.Forbidden:
                                                    meg_error_forbidden = f"Tentei adicionar um cargo, " \
                                                                          f"mas não tenho permissão para fazer isso.\n" \
                                                                          f"Certifique-se de que tenho um cargo de hierarquia mais " \
                                                                          f"alta do que o cargo que devo adicionar e que " \
                                                                          f"tenho a permissão para `Gerenciar cargos`.\n" \
                                                                          f"Discord Server ID: {guild.id}\n" \
                                                                          f"Discord Server Name: {guild.name}\n" \
                                                                          f"Cargo: `{role.name}`\n" \
                                                                          f"Cargo ID: {role_id}"
                                                    print(meg_error_forbidden)
                                                    return await guild.system_channel.send(meg_error_forbidden)
                                                await guild.system_channel.send(f"<@{member.id}> O cargo `{role.name}` foi adicionado.")
                                        """elif role == ctx.guild.default_role:
                                        await ctx.send("Cargo: Everyone")"""
                '''else:
                    return await guild.system_channel.send(f"<@{member.id}> não foi encontrado nem um cargo salvo "
                                                           f"para você nesse discord.")'''
            except Exception as error:
                raise error
    except Exception as e:
        print(e)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Informa quando que um membro entrou no Servidor Discord."""
    await ctx.send('Discord: {0.name}\nEntrou no servidor: {0.joined_at}'.format(member))


@bot.event
async def on_member_remove(member):
    pass


@bot.event
async def on_guild_join(guild):
    try:
        db = pymysql.connect(
            host='127.0.0.1',
            user='usuario',
            password='Senha-password',
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
            host='127.0.0.1',
            user='usuario',
            password='Senha-password',
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


'''
@commands.guild_only()
@bot.command()
async def creator(ctx):
    """
    Meu criador: VORTEX
    """
    if ctx.author.id == 136933432973459457:
        return await ctx.send(f"Olá meu criador. ❤️")
    return await ctx.send(f"Meu criador se chama: VORTEX\n"
                          f"_Ele não quer ser incomodado então só irei informar o Nick_.")
'''


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
        return await ctx.send('Por favor informe uma quantidade de mensagens para deletar.')


if __name__ == "__main__":
    for modulo in modulos:
        bot.load_extension(modulo)

    bot.run(token)
