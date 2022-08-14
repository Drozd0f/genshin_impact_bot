from discord.ext import commands


@commands.command()
async def ping(ctx: commands.context.Context):
    await ctx.send('pong')


def jopa():
    return 'popa'
