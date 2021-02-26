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


class Comandos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
                password='SENHA',
                db='magnetroles',
                cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()
            user = ctx.author
            server = ctx.guild

            cursor.execute(f"SELECT id_server FROM `d_servers` WHERE server_id = '{server.id}'")
            row_id = cursor.fetchone()
            id_server = row_id['id_server']

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
                                elif role == ctx.guild.default_role:
                                    await ctx.send("Cargo: Everyone")
            else:
                return await ctx.send(f"<@{user.id}> não foi encontrado nem um cargo salvo para você nesse discord.")

        except Exception as error:
            raise error

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
                password='SENHA',
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

            if row_user is None:
                for role in ctx.author.roles:
                    if not role == ctx.guild.default_role:
                        await ctx.send(f"Cargo: {role}\n"
                                       f"ID: {role.id}")

                        sql = "INSERT INTO `d_roles` (id_server, discord_id, discord_nome, role_id) VALUES(%s,%s,%s,%s)"
                        val = (id_server, user.id, user.name, role.id)
                        cursor.execute(sql, val)

                        db.commit()
                cursor.close()
                db.close()
            elif row_user is not None:
                for role in ctx.author.roles:
                    if not role == ctx.guild.default_role:
                        await ctx.send(f"Cargo: {role}\n"
                                       f"ID: {role.id}")
                        cursor.execute(f"SELECT * FROM `d_roles` WHERE role_id = '{role.id}' and id_server = '{id_server}' and discord_id = '{user.id}'")
                        row_role = cursor.fetchone()
                        if row_role is None:
                            sql = "INSERT INTO `d_roles` (id_server, discord_id, discord_nome, role_id) VALUES(%s,%s,%s,%s)"
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
                    password='SENHA',
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

    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.channel)
    @commands.guild_only()
    @commands.command(name='teste', aliases=['teste1', 'teste2'])
    async def test(self, ctx):
        """
        Comando de teste geral.
        """
        # a
        """
        embed = discord.Embed(description=f"olá {ctx.author.name} isso é um teste.", color=0x2F3136)
        embed.set_image(url=f"https://sasbrasil.tk/sasimg/holita/blackholita_1920x1080.png")
        embed.add_field(name=f"Reason: aaaaaa", value='aaa')
        await ctx.send(embed=embed)

        if ctx.author.guild_permissions.administrator:
            await ctx.send("Parabéns você é um Administrador nesse discord.")
        else:
            await ctx.send("Você não é um Administrador nesse discord.")
        """

    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.channel)
    @commands.guild_only()
    @commands.command(name='roleromeve', aliases=['tirarcargo'])
    async def removerole(self, ctx, *, role: discord.Role):
        if role is None:
            await ctx.send('Escreve corretamente o nome de um cargo (role)')
        elif role is not None:
            await ctx.send(f"Role Name: {role.name}\n"
                           f"Role ID: {role.id}")


def setup(bot):
    bot.add_cog(Comandos(bot))


"""
            
            
            

            3 - criar o comando para add cargo (onde somente adm pode usar), e salvar automaticamente na banco de dados (no membro que foi adicionado).

            3.1 - Criar o comando para remover o cargo da DB (onde somente adm pode usar). para que o usuário, 
            não peque o cargo novamente apos os administradores do discord remover este cargo.
            3.2 - ao em vez de remover, banir o cargo do usuario. E ao add novamente, verificar se já não está ali.
            e alterar o status para "não banido"
            3.3 - E deixar claro que se for usar esse bot, todo e qualquer cargo, deverá ser adicionado e removido usando comando do bot.
            Principalmente para remover.
            
            adicionar até poderá ser manualmente, mas para remover deve-se usar o comando do bot para remover o cargo do usuário.
            E essa remoção vai funcionar por @ao_mencionar_o_discord do usuário ou por discord_id do usuário.
            usar discord_id do usuário será possivel remover cargos, caso o jogador tenha sido expulso ou que ele(a) 
            tenha saido por conta propria do servidor discord.

            4 - pronto

            5 - Criar 1 comando de mass role.
            
            6.7 - usar as colunas ban_user e ban_role para proibir um usuario de usar o bot e de um cargo ser adicionado para determinado usuario.
            
            7 - expulsar, e banir usuarios do discord.
            7.1 - Em caso de banir, banir o usuario dos cargos do bot para o discord onde o comando foi usado.
            7.2 - ou não. criar 1 comando diferente de banir do discord, para banir apenas o usuario de usar o imadecargos
            
            8 - Colocar o comando ima de carogs no On user join =D
            
            """
