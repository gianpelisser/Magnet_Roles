"""
from discord.ext.commands import MissingPermissions
from discord import File
import json
import asyncio
"""
import discord
import discord.role
from discord.ext import commands
import pymysql
import pymysql.cursors
import locales.pt_br
import locales.en


class Comandos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(rate=30, per=1.0, type=commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='imadecargos', aliases=['recuperarmeuscargos', 'recuperarcargos', 'recoverroles',
                                                      'cargorrecuperar', 'rolesrecover', 'recovermyroles'])
    async def imacargos(self, ctx):
        """Recuperar todos os cargos salvos do usuário no servidor do discord.

                ATENÇÃO
                ------------
                remover: cargos
                    Os administradores devem sempre remover cargos usando comando desse bot.
        """
        try:
            db = pymysql.connect(
                host='127.0.0.1',
                user='usuario',
                password='Senha-password',
                db='magnetroles',
                cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()
            user = ctx.author
            server = ctx.guild

            cursor.execute(f"SELECT id_server FROM `d_servers` WHERE server_id = '{server.id}'")
            row_id = cursor.fetchone()
            id_server = row_id['id_server']

            cursor.execute(f"SELECT * FROM d_roles WHERE discord_id = '{user.id}' "
                           f"and user_ban = 'yes' or role_ban = 'yes'")
            rows_role_banned_from_user = cursor.fetchall()

            user_is_ban = 'no'
            role_ban_list = []
            if rows_role_banned_from_user is not None:
                sayonetime = 1
                for row_ur_ban in rows_role_banned_from_user:
                    user_ban = row_ur_ban['user_ban']
                    role_ban = row_ur_ban['role_ban']
                    if user_ban == 'yes':
                        user_is_ban = 'yes'
                        if sayonetime == 1:
                            await ctx.send(f"Desculpe **{user.mention}**. Você está proibido de usar esse comando.")
                        sayonetime += 1

                    if role_ban == 'yes':
                        role_ban_list.append(row_ur_ban['role_id'])
                        roleban = discord.utils.get(ctx.guild.roles, id=row_ur_ban['role_id'])
                        await ctx.send(f"Cargo _Bloqueado_: {roleban}")

            if user_is_ban == 'yes':
                return

            cursor.execute(f"SELECT * FROM d_roles_adm WHERE id_server = '{id_server}' and role_can_use = 'no'")
            rows_role_adm = cursor.fetchall()
            roles_adm_list = []
            if rows_role_adm is not None:
                for roles in rows_role_adm:
                    roles_adm_list.append(roles['role_id_adm'])

            cursor.execute(f"SELECT role_id FROM `d_roles` WHERE discord_id = '{user.id}' and id_server = '{id_server}'")
            row_user = cursor.fetchall()

            if row_user is not None:
                for row in row_user:
                    role_id = row['role_id']

                    roleadd = discord.utils.get(ctx.guild.roles, id=role_id)
                    if not roleadd in ctx.author.roles:
                        for role in ctx.guild.roles:
                            if role.id == role_id:
                                if not role == ctx.guild.default_role:
                                    if not role.id in role_ban_list:
                                        if not role.id in roles_adm_list:
                                            try:
                                                await ctx.author.add_roles(roleadd, reason='BOT: Magnetic of Role')
                                            except discord.Forbidden:
                                                meg_error_forbidden = f"Tentei adicionar um cargo, " \
                                                                      f"mas não tenho permissão para fazer isso.\n" \
                                                                      f"Certifique-se de que tenho um cargo de hierarquia mais " \
                                                                      f"alta do que o cargo que devo adicionar e que " \
                                                                      f"tenho a permissão para `Gerenciar cargos`.\n" \
                                                                      f"Discord Server ID: {server.id}\n" \
                                                                      f"Discord Server Name: {server.name}\n" \
                                                                      f"Cargo: `{role.name}`\n" \
                                                                      f"Cargo ID: {role_id}"
                                                print(meg_error_forbidden)
                                                return await ctx.send(meg_error_forbidden)
                                            await ctx.send(f"<@{user.id}> O cargo `{role.name}` foi adicionado.")
                                    """elif role == ctx.guild.default_role:
                                    await ctx.send("Cargo: Everyone")"""
            else:
                return await ctx.send(f"<@{user.id}> não foi encontrado cargos salvo para você nesse discord.\n"
                                      f"Use o comando `mrsaveroles` para salvar seus cargos.")

        except Exception as error:
            raise error

    @commands.cooldown(rate=60, per=1.0, type=commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='saveroles', aliases=['salvarcargos', 'salvar', 'salvarmeuscargos', 'salvemyroles'])
    async def myroles(self, ctx):
        """
        Salva todos os cargos do usuário, apenas do discord onde o comando foi usado.
        """
        try:
            db = pymysql.connect(
                host='127.0.0.1',
                user='usuario',
                password='Senha-password',
                db='magnetroles',
                cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()
            user = ctx.author
            server = ctx.guild

            cursor.execute(f"SELECT id_server FROM `d_servers` WHERE server_id = '{server.id}'")
            row_id = cursor.fetchone()
            id_server = row_id['id_server']

            cursor.execute(f"SELECT * FROM `d_roles` WHERE discord_id = '{user.id}' and id_server = '{id_server}'")
            row_user = cursor.fetchone()

            if row_user['user_ban'] == 'yes':
                return await ctx.send(f"{user.mention} desculpe, mas você está proibido de usar este comando.")

            cursor.execute(f"SELECT * FROM d_roles_adm WHERE id_server = '{id_server}' and role_can_use = 'no'")
            rows_role_adm = cursor.fetchall()
            roles_adm_list = []
            if rows_role_adm is not None:
                for roles in rows_role_adm:
                    roles_adm_list.append(roles['role_id_adm'])
            # print(f"Os Cargos {roles_adm_list}, não podem ser salvos no Ima de Cargos.")
            if row_user is None:
                for role in ctx.author.roles:
                    if not role.id in roles_adm_list:
                        if not role == ctx.guild.default_role:
                            await ctx.send(f"Cargo: {role}\n"
                                           f"ID: {role.id}")

                            sql = "INSERT INTO d_roles (id_server, discord_id, discord_nome, role_id) VALUES(%s,%s,%s,%s)"
                            val = (id_server, user.id, user.name, role.id)
                            cursor.execute(sql, val)

                            db.commit()
                cursor.close()
                db.close()
            elif row_user is not None:
                for role in ctx.author.roles:
                    if not role.id in roles_adm_list:
                        if not role == ctx.guild.default_role:
                            await ctx.send(f"Cargo: {role}\n"
                                           f"ID: {role.id}")
                            cursor.execute(f"SELECT * FROM `d_roles` WHERE role_id = '{role.id}' and id_server = '{id_server}' and discord_id = '{user.id}'")
                            row_role = cursor.fetchone()
                            if row_role is None:
                                sql = "INSERT INTO d_roles (id_server, discord_id, discord_nome, role_id) VALUES(%s,%s,%s,%s)"
                                val = (id_server, user.id, user.name, role.id)
                                cursor.execute(sql, val)
                                db.commit()
                            else:
                                pass
                cursor.close()
                db.close()

            try:
                cursor.close()
                db.close()
            except:
                pass
            return await ctx.send(f"<@{user.id}> Pronto!\n_Cargos salvos!_")

        except Exception as e:
            return await ctx.send(e)

    @commands.guild_only()
    @commands.command(name='changeprefix', aliases=['mudarprefixo', 'mudarprefix'])
    async def prefix(self, ctx, *, prefix):
        """
        Alterar o prefixo do BOT.
        Exemplo: mrchangeprefix v
        """
        if ctx.author.guild_permissions.administrator:
            try:
                db = pymysql.connect(
                    host='127.0.0.1',
                    user='usuario',
                    password='Senha-password',
                    db='magnetroles',
                    cursorclass=pymysql.cursors.DictCursor)
                cursor = db.cursor()

                user = ctx.author
                server_id = ctx.guild.id
                server_name = ctx.guild.name

                cursor.execute(f"SELECT * FROM `d_servers` WHERE server_id = '{server_id}'")
                row = cursor.fetchone()

                if row is not None:
                    cursor.execute(f"UPDATE `d_servers` SET server_prefix = '{str(prefix)}', server_nome = '{server_name}' WHERE server_id = '{server_id}'")
                    db.commit()
                    cursor.close()
                    db.close()
                    return await ctx.send(f"<@{user.id}> o prefixo do BOT foi alterado.\n"
                                          f"**Novo prefixo:** {str(prefix)}")
                else:
                    cursor.close()
                    db.close()
                    return

            except Exception as e:
                return await ctx.send(e)

    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.channel)
    @commands.guild_only()
    @commands.command(name='removerole', aliases=['tirarcargo'])
    async def roleromeve(self, ctx, role: discord.Role = None, member: discord.Member = None):
        """
        Remove um cargo de um usuário mencionado.
            É necessario remover o cargo dos usuários com esse comando para que:
            o usuário não pegue novamente com o comando "ima de cargos"
        """
        if role is None:
            return await ctx.send(f"OPS. Você não informou um Cargo (Role).")
        if member is None:
            member = ctx.author
        if ctx.author.guild_permissions.administrator:
            try:
                db = pymysql.connect(
                    host='127.0.0.1',
                    user='usuario',
                    password='Senha-password',
                    db='magnetroles',
                    cursorclass=pymysql.cursors.DictCursor)
                cursor = db.cursor()

                guild = ctx.guild
                # server_name = ctx.guild.name

                cursor.execute(f"SELECT id_server FROM d_servers WHERE server_id = '{guild.id}'")
                rowserver = cursor.fetchone()
                id_server = rowserver['id_server']

                cursor.execute(f"SELECT * FROM d_roles WHERE discord_id = '{member.id}'"
                               f"and id_server = '{id_server}' and role_id = '{role.id}'")
                row = cursor.fetchone()
                if row is not None:
                    cursor.execute(f"""
                        UPDATE d_roles SET role_ban = 'yes'
                        WHERE role_id = '{role.id}' and discord_id = '{member.id}' and id_server = '{id_server}'
                    """)
                    db.commit()
                    cursor.close()
                    db.close()
                    for role1 in ctx.guild.roles:
                        if role1.id == role.id:
                            if not role == ctx.guild.default_role:
                                try:
                                    await ctx.author.remove_roles(role, reason='BOT: Magnetic of Role')
                                except discord.Forbidden:
                                    meg_error_forbidden = f"Tentei remover um cargo, " \
                                                          f"mas não tenho permissão para fazer isso.\n" \
                                                          f"Certifique-se de que tenho um cargo de hierarquia mais " \
                                                          f"alto do que o cargo que devo remover e que " \
                                                          f"tenho a permissão para `Gerenciar cargos`.\n" \
                                                          f"Discord Server ID: {guild.id}\n" \
                                                          f"Discord Server Name: {guild.name}\n" \
                                                          f"Cargo: `{role.name}`\n" \
                                                          f"Cargo ID: {role.id}"
                                    print(meg_error_forbidden)
                                    return await ctx.send(meg_error_forbidden)
                                await ctx.send(f"<@{ctx.author.id}> o cargo `{role.name}` foi removido do usuário: "
                                               f"{member.mention}")
                    return await ctx.send(f"{ctx.author.mention} esse cargo foi bloqueado do `Ima de Cargos`"
                                          f" o usuário {member.mention} não poderá receber esse cargo novamente.")
                else:
                    cursor.close()
                    db.close()
                    for role1 in ctx.guild.roles:
                        if role1.id == role.id:
                            if not role == ctx.guild.default_role:
                                try:
                                    await ctx.author.remove_roles(role, reason='BOT: Magnetic of Role')
                                except discord.Forbidden:
                                    meg_error_forbidden = f"Tentei remover um cargo, " \
                                                          f"mas não tenho permissão para fazer isso.\n" \
                                                          f"Certifique-se de que tenho um cargo de hierarquia mais " \
                                                          f"alto do que o cargo que devo remover e que " \
                                                          f"tenho a permissão para `Gerenciar cargos`.\n" \
                                                          f"Discord Server ID: {guild.id}\n" \
                                                          f"Discord Server Name: {guild.name}\n" \
                                                          f"Cargo: `{role.name}`\n" \
                                                          f"Cargo ID: {role.id}"
                                    print(meg_error_forbidden)
                                    return await ctx.send(meg_error_forbidden)
                                await ctx.send(f"<@{ctx.author.id}> o cargo `{role.name}` foi removido do usuário: "
                                               f"{member.mention}")
                    return await ctx.send(f"{ctx.author.mention} esse cargo não foi salvo no `Ima de Cargos`"
                                          f" para o usuário {member.mention}")
            except Exception as e:
                print(e)
                return await ctx.send(e)

    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.channel)
    @commands.guild_only()
    @commands.command(name='addrole', aliases=['acidionarcargo', 'acidionarrole'])
    async def roleadd(self, ctx, role: discord.Role = None, member: discord.Member = None):
        """
        Adiciona um cargo para um usuário mencionado.
            É necessario adicionar o cargo dos usuários com esse comando quando:
            For removido um cargo do usuário usando o comando `removerole`
        """
        if role is None:
            return await ctx.send(f"OPS. Você não informou um Cargo (Role).")
        if member is None:
            member = ctx.author
        if ctx.author.guild_permissions.administrator:
            try:
                db = pymysql.connect(
                    host='127.0.0.1',
                    user='usuario',
                    password='Senha-password',
                    db='magnetroles',
                    cursorclass=pymysql.cursors.DictCursor)
                cursor = db.cursor()

                guild = ctx.guild
                # server_name = ctx.guild.name

                cursor.execute(f"SELECT id_server FROM d_servers WHERE server_id = '{guild.id}'")
                rowserver = cursor.fetchone()
                id_server = rowserver['id_server']

                cursor.execute(f"SELECT * FROM d_roles WHERE discord_id = '{member.id}'"
                               f"and id_server = '{id_server}' and role_id = '{role.id}'")
                row = cursor.fetchone()
                if row is not None:
                    cursor.execute(f"""
                            UPDATE d_roles SET role_ban = 'no'
                            WHERE role_id = '{role.id}' and discord_id = '{member.id}' and id_server = '{id_server}'
                        """)
                    db.commit()
                    cursor.close()
                    db.close()
                    for role1 in ctx.guild.roles:
                        if role1.id == role.id:
                            if not role == ctx.guild.default_role:
                                try:
                                    await ctx.author.add_roles(role, reason='BOT: Magnetic of Role')
                                except discord.Forbidden:
                                    meg_error_forbidden = f"Tentei adicionar um cargo, " \
                                                          f"mas não tenho permissão para fazer isso.\n" \
                                                          f"Certifique-se de que tenho um cargo de hierarquia mais " \
                                                          f"alto do que o cargo que devo adicionar. E que " \
                                                          f"tenho a permissão para `Gerenciar cargos`.\n" \
                                                          f"Discord Server ID: {guild.id}\n" \
                                                          f"Discord Server Name: {guild.name}\n" \
                                                          f"Cargo: `{role.name}`\n" \
                                                          f"Cargo ID: {role.id}"
                                    print(meg_error_forbidden)
                                    return await ctx.send(meg_error_forbidden)
                                await ctx.send(f"<@{ctx.author.id}> o cargo `{role.name}` foi adicionado para o usuário: "
                                               f"{member.mention}")
                    return await ctx.send(f"{ctx.author.mention} esse cargo foi desbloqueado do `Ima de Cargos`"
                                          f" o usuário {member.mention} poderá receber esse cargo novamente.\n"
                                          f"_Se ele sair do servidor e usar o `Ima de Cargos`_.")
                else:
                    for role1 in ctx.guild.roles:
                        if role1.id == role.id:
                            if not role == ctx.guild.default_role:
                                try:
                                    await ctx.author.add_roles(role, reason='BOT: Magnetic of Role')
                                except discord.Forbidden:
                                    meg_error_forbidden = f"Tentei remover um cargo, " \
                                                          f"mas não tenho permissão para fazer isso.\n" \
                                                          f"Certifique-se de que tenho um cargo de hierarquia mais " \
                                                          f"alto do que o cargo que devo remover e que " \
                                                          f"tenho a permissão para `Gerenciar cargos`.\n" \
                                                          f"Discord Server ID: {guild.id}\n" \
                                                          f"Discord Server Name: {guild.name}\n" \
                                                          f"Cargo: `{role.name}`\n" \
                                                          f"Cargo ID: {role.id}"
                                    print(meg_error_forbidden)
                                    return await ctx.send(meg_error_forbidden)
                                await ctx.send(f"<@{ctx.author.id}> o cargo `{role.name}` foi adicionado para o usuário: "
                                               f"{member.mention}")
                    sql = "INSERT INTO d_roles (id_server, discord_id, discord_nome, role_id)" \
                          "VALUES (%s,%s,%s,%s)"
                    val = (id_server, member.id, member.name, role.id)
                    cursor.execute(sql, val)
                    db.commit()
                    cursor.close()
                    db.close()
                    return await ctx.send(f"{ctx.author.mention} esse cargo foi salvo no `Ima de Cargos`"
                                          f" para o usuário {member.mention}")
            except Exception as e:
                print(e)
                return await ctx.send(e)

    @roleadd.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.RoleNotFound):
            print(error)
            return await ctx.send("Você não informou um Cargo existente nesse Servidor.")

    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.channel)
    @commands.guild_only()
    @commands.command(name='addbanrole', aliases=['blockrole', 'banirrole'])
    async def roleban(self, ctx, *, role: discord.Role = None):
        """
        Bloqueia (ban) um cargo (role) de ser salvo no servidor.
            Os Administradores podem usar esse comando para bloquear cargos com ADM e outros.
            Mesmo que o cargo já tenha sido salvo, ele não será adicionado.
        """
        if role is None:
            return await ctx.send(f"OPS. Você não informou um Cargo (Role).")
        member = ctx.author
        if ctx.author.guild_permissions.administrator:
            try:
                db = pymysql.connect(
                    host='127.0.0.1',
                    user='usuario',
                    password='Senha-password',
                    db='magnetroles',
                    cursorclass=pymysql.cursors.DictCursor)
                cursor = db.cursor()

                server_id = ctx.guild.id
                # server_name = ctx.guild.name

                cursor.execute(f"SELECT id_server FROM d_servers WHERE server_id = '{server_id}'")
                rowserver = cursor.fetchone()
                id_server = rowserver['id_server']

                cursor.execute(f"SELECT * FROM d_roles_adm WHERE role_id_adm = '{role.id}'"
                               f"and id_server = '{id_server}'")
                row = cursor.fetchone()
                if row is None:
                    sql = "INSERT INTO d_roles_adm (role_id_adm, role_name_adm, role_can_use, id_server)" \
                          "VALUES (%s,%s,%s,%s)"
                    val = (role.id, role.name, 'no', id_server)
                    cursor.execute(sql, val)
                    db.commit()
                    cursor.close()
                    db.close()
                    return await ctx.send(f"O Cargo (Role) **{role.name}** foi bloqueada do Ima de cargos.")
                else:
                    cursor.close()
                    db.close()
                    return await ctx.send(f"O Cargo (Role) **{role.name}** já está bloqueado do Ima de cargos.")
            except Exception as e:
                return await ctx.send(e)
        else:
            await ctx.message.delete()
            return await ctx.send(f"{member.mention} Somente Administradores podem usar esse comando.", delete_after=10)

    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.channel)
    @commands.guild_only()
    @commands.command(name='removebanrole', aliases=['removeblockrole', 'desbanirrole'])
    async def removeroleban(self, ctx, *, role: discord.Role = None):
        """
        Remove o Bloqueio (ban) de um cargo (role), permitindo que ele sejá salvo no ima de cargos.
            Os Administradores podem usar esse comando para desbloquear cargos bloqueados.
        """
        if role is None:
            return await ctx.send(f"OPS. Você não informou um Cargo (Role).")
        member = ctx.author
        if ctx.author.guild_permissions.administrator:
            try:
                db = pymysql.connect(
                    host='127.0.0.1',
                    user='usuario',
                    password='Senha-password',
                    db='magnetroles',
                    cursorclass=pymysql.cursors.DictCursor)
                cursor = db.cursor()

                server_id = ctx.guild.id
                # server_name = ctx.guild.name

                cursor.execute(f"SELECT id_server FROM d_servers WHERE server_id = '{server_id}'")
                rowserver = cursor.fetchone()
                id_server = rowserver['id_server']

                cursor.execute(f"SELECT * FROM d_roles_adm WHERE role_id_adm = '{role.id}' "
                               f"and id_server = '{id_server}'")
                row = cursor.fetchone()
                if row is not None:
                    cursor.execute(f"DELETE FROM d_roles_adm WHERE role_id_adm = '{role.id}'")
                    db.commit()
                    cursor.close()
                    db.close()
                    return await ctx.send(f"O Cargo (Role) **{role.name}** foi desbloqueado do Ima de cargos.")
                else:
                    cursor.close()
                    db.close()
                    return await ctx.send(f"O Cargo (Role) **{role.name}** não sstá bloqueado do Ima de cargos.")
            except Exception as e:
                return await ctx.send(e)
        else:
            await ctx.message.delete()
            return await ctx.send(f"{member.mention} Somente Administradores podem usar esse comando.", delete_after=10)

    @removeroleban.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.RoleNotFound):
            print(error)
            return await ctx.send("Você não informou um Cargo existente nesse Servidor.")

    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.channel)
    @commands.guild_only()
    @commands.command(name='removebanuser', aliases=['removeblockuser', 'desbaniruser'])
    async def removeuserban(self, ctx, *, member: discord.Member = None):
        """
        Remove o Bloqueio (ban) de um usuário, permitindo que ele use os comandos no servidor.
            Referente ao comando 'addbanuser'
        """
        if member is None:
            return await ctx.send(f"OPS. Você não informou um usuário.")

        if ctx.author.guild_permissions.administrator:
            member_adm = ctx.author
            try:
                db = pymysql.connect(
                    host='127.0.0.1',
                    user='usuario',
                    password='Senha-password',
                    db='magnetroles',
                    cursorclass=pymysql.cursors.DictCursor)
                cursor = db.cursor()

                server_id = ctx.guild.id

                cursor.execute(f"SELECT id_server FROM d_servers WHERE server_id = '{server_id}'")
                rowserver = cursor.fetchone()
                id_server = rowserver['id_server']

                cursor.execute(f"SELECT * FROM d_roles_adm WHERE role_id_adm = '{member.id}' "
                               f"and id_server = '{id_server}'")
                row = cursor.fetchone()
                if row is not None:
                    cursor.execute(f"UPDATE d_roles SET user_ban = 'no' WHERE discord_id = '{member.id}' "
                                   f"and id_server = '{id_server}'")
                    db.commit()
                    cursor.close()
                    db.close()
                    return await ctx.send(f"{member_adm.mention} O usuário **{member.mention}** foi desbloqueado do Ima de cargos.")
                else:
                    cursor.close()
                    db.close()
                    return await ctx.send(f"O usuário **{member.name}** não usou o comando `saveroles` ainda.")
            except Exception as e:
                return await ctx.send(e)
        else:
            try:
                await ctx.message.delete()
            except:
                pass
            return await ctx.send(f"{member.mention} Somente Administradores podem usar esse comando.", delete_after=10)

    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.channel)
    @commands.guild_only()
    @commands.command(name='addbanuser', aliases=['adicionarblockuser', 'dbaniruser'])
    async def adduserban(self, ctx, *, member: discord.Member = None):
        """
        Banir um usuário, bloqueando que ele use os comandos do bot nesse servidor discord.
            Os Administradores podem usar esse comando para bloquear usuários que fica entrando e saindo sem motivo.
            use `removebanuser` para desbanir.
        """
        if member is None:
            return await ctx.send(f"OPS. Você não informou um usuário.")

        if ctx.author.guild_permissions.administrator:
            member_adm = ctx.author
            try:
                db = pymysql.connect(
                    host='127.0.0.1',
                    user='usuario',
                    password='Senha-password',
                    db='magnetroles',
                    cursorclass=pymysql.cursors.DictCursor)
                cursor = db.cursor()

                server_id = ctx.guild.id

                cursor.execute(f"SELECT id_server FROM d_servers WHERE server_id = '{server_id}'")
                rowserver = cursor.fetchone()
                id_server = rowserver['id_server']

                cursor.execute(f"SELECT * FROM d_roles_adm WHERE role_id_adm = '{member.id}' "
                               f"and id_server = '{id_server}'")
                row = cursor.fetchone()
                if row is not None:
                    cursor.execute(f"UPDATE d_roles SET user_ban = 'yes' WHERE discord_id = '{member.id}' "
                                   f"and id_server = '{id_server}'")
                    db.commit()
                    cursor.close()
                    db.close()
                    return await ctx.send(
                        f"{member_adm.mention} O usuário **{member.mention}** foi bloqueado do BOT **Ima de cargos**"
                        f" nesse servidor discord.\nVocê pode usar `removebanuser` para desbanir.")
                else:
                    # talvez fazer um insert aqui, para adicionar ban a um usuário.
                    cursor.close()
                    db.close()
                    return await ctx.send(f"O usuário **{member.name}** não usou o comando `saveroles` ainda.")
            except Exception as e:
                return await ctx.send(e)
        else:
            try:
                await ctx.message.delete()
            except:
                pass
            return await ctx.send(f"{member.mention} Somente Administradores podem usar esse comando.", delete_after=10)

    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.channel)
    @commands.guild_only()
    @commands.command(name='memberjoinon', aliases=['memberjoinallow'])
    async def turonmemberjoin(self, ctx):
        """
        Habilitar On Member Join - Para os cargos serem adicionados ao entrar no servidor discord.
        """
        if ctx.author.guild_permissions.administrator:
            member = ctx.author
            try:
                db = pymysql.connect(
                    host='127.0.0.1',
                    user='usuario',
                    password='Senha-password',
                    db='magnetroles',
                    cursorclass=pymysql.cursors.DictCursor)
                cursor = db.cursor()

                server_id = ctx.guild.id

                cursor.execute(f"SELECT * FROM d_servers WHERE server_id = '{server_id}'")
                rowserver = cursor.fetchone()

                if rowserver is not None:
                    cursor.execute(f"UPDATE `d_servers` SET `on_member_join` = 'yes' WHERE `server_id` = '{server_id}'")
                    db.commit()
                    cursor.close()
                    db.close()
                    return await ctx.send(
                        f"{member.mention} Pronto. Agora quando um usuário entrar no servidor se ele(a) ter cargos"
                        f" salvos, vai receber automaticamente.")
                else:
                    # talvez fazer um insert aqui, para adicionar ban a um usuário.
                    cursor.close()
                    db.close()
                    return await ctx.send(f"Tem algo errado: Erro #01 - On Member Join")
            except Exception as e:
                return await ctx.send(e)
        else:
            try:
                await ctx.message.delete()
            except:
                pass
            return await ctx.send(f"{ctx.author.mention} Somente Administradores podem usar esse comando.", delete_after=10)

    @commands.cooldown(rate=1, per=1.0, type=commands.BucketType.channel)
    @commands.guild_only()
    @commands.command(name='memberjoinoff', aliases=['memberjoindeny'])
    async def turoffmemberjoin(self, ctx):
        """
        Desativar On Member Join - Para os cargos não sejá adicionado ao entrar no servidor discord.
        """
        if ctx.author.guild_permissions.administrator:
            member = ctx.author
            try:
                db = pymysql.connect(
                    host='127.0.0.1',
                    user='usuario',
                    password='Senha-password',
                    db='magnetroles',
                    cursorclass=pymysql.cursors.DictCursor)
                cursor = db.cursor()

                server_id = ctx.guild.id

                cursor.execute(f"SELECT * FROM d_servers WHERE server_id = '{server_id}'")
                rowserver = cursor.fetchone()

                if rowserver is not None:
                    cursor.execute(f"UPDATE `d_servers` SET `on_member_join` = 'no' WHERE `server_id` = '{server_id}'")
                    db.commit()
                    cursor.close()
                    db.close()
                    return await ctx.send(
                        f"{member.mention} Pronto. Receber cargos automaticamente foi desativado.")
                else:
                    # talvez fazer um insert aqui, para adicionar ban a um usuário.
                    cursor.close()
                    db.close()
                    return await ctx.send(f"Tem algo errado: Erro #02 - On Member Join")
            except Exception as e:
                return await ctx.send(e)
        else:
            try:
                await ctx.message.delete()
            except:
                pass
            return await ctx.send(f"{ctx.author.mention} Somente Administradores podem usar esse comando.",
                                  delete_after=10)


def setup(bot):
    bot.add_cog(Comandos(bot))
