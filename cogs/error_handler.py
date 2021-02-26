import discord
import traceback
import sys
from discord.ext import commands


class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Evento disparado quando um erro é gerado ao invocar um comando.
        """
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} foi desabilitado.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} não pode ser usado em mensagens privadas.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                await ctx.send('Não consegui encontrar esse membro. Por favor, tente novamente.')

        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("O Bot não tem permissão para adicionar ou remover todos os cargos.\n"
                           "Coloque o cargo do BOT acima de todos os cargos que o BOT pode adicionar e remover.")

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Você não tem direitos para este comando.")
            # await ctx.message.delete()

        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("Comando inválido.")
            await ctx.message.delete()

        elif isinstance(error, discord.Forbidden):
            return await ctx.send(f"Tentei adicionar ou remover um cargo, mas não tenho permissão para fazer isso.\n"
                           f"Certifique-se de que tenho um cargo de hierarquia mais alta do que o cargo que devo "
                           f"adicionar ou remover e de que tenho a permissão para `Gerenciar cargos`.")
        elif isinstance(error, discord.errors.Forbidden):
            return await ctx.send("Não é permitido fazer isso.")
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            return await ctx.send("Está faltando alguma coisa.")

        if isinstance(error, commands.CommandOnCooldown):
            s = error.retry_after
            s = round(s, 2)
            h, r = divmod(int(s), 3600)
            m, s = divmod(r, 60)
            return await ctx.channel.send(f'<@{ctx.author.id}> **Cooldown** você precisa esperar **{str(h) + "h : " if h != 0 else ""}{str(m) + "m : " if m != 0 else ""}{str(s) + "s" if s != 0 else ""}** para usar esse comando novamente.')

        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command(name='repeat', aliases=['fale', 'copy', 'falar', 'repetir'])
    async def do_repeat(self, ctx, *, inp: str):
        """Um comando simples que repete sua entrada!
        Parâmetros
        ------------
        Tipo de entrada: texto
            A mensagem que você deseja repetir.
        """
        await ctx.send(inp)

    @do_repeat.error
    async def do_repeat_handler(self, ctx, error):
        """Um manipulador de erros local para o comando do_repeat.
         Isso só ouvirá erros em do_repeat.
         O on_command_error global ainda será invocado depois.
        """

        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'inp':
                await ctx.send("Você se esqueceu de me informar alguma coisa para repetir!")


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
