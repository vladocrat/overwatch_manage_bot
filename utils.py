import struct

import discord


class Utils:
    class Discord:
        @staticmethod
        def channel(ctx):
            return discord.utils.get(ctx.guild.channels)

        @staticmethod
        def channel_id(ctx):
            return Utils.Discord.channel(ctx=ctx).id

    class General:
        @staticmethod
        def to_uint32(number: int):
            return struct.pack(">I", number)
