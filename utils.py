import discord


def channel(ctx):
    return discord.utils.get(ctx.guild.channels)


def channel_id(ctx):
    return channel(ctx=ctx).id
