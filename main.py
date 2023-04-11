import asyncio

import discord

from PyQt5.QtCore import QByteArray, QTextStream, QDataStream, QIODevice

from protocol import Protocol
from server import ClientConnection
from discord.ext import commands
from configure import Configurer, Config
from utils import Utils
from views import MixesView


def run():
    configurer = Configurer("settings.ini")
    bot_config = configurer.configure(Config.Bot)
    network_config = configurer.configure(Config.Network)

    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)
    _bot = commands.Bot(command_prefix=bot_config.prefix, client=client, intents=client.intents)

    client_connection = ClientConnection()
    client_connection.connect_to_host(port=network_config.port)

    msg = QByteArray()
    stream = QDataStream(msg, QIODevice.WriteOnly)
    text = "hello"
    stream.setByteOrder(QDataStream.BigEndian)
    stream.writeQString(text)
    stream.writeInt32(20)

    if not client_connection.send(command=Protocol.Bot.hello.value, data=msg):
        print("failed to send data")

    if not client_connection.socket.waitForReadyRead():
        print("wait to ready read")

    @_bot.event
    async def on_ready():
        print('bot started')

    @_bot.command("mixes")
    async def mixes(ctx):
        view = MixesView()
        message = "A new mix has been scheduled to..."
        title = "MIX"
        embed = discord.Embed(title=title, description=message)
        await ctx.send(view=view, embed=embed)
        await view.wait()
        await asyncio.sleep(1)
        await ctx.author.send("hi this is your channel id: " + str(ctx.author.id))

    #_bot.run(bot_config.token)


if __name__ == '__main__':
    run()
