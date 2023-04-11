import asyncio
import encodings

import discord
import json

from PyQt5.QtCore import QByteArray, QDataStream
from PyQt5.QtNetwork import QHostAddress, QAbstractSocket

from protocol import Protocol
from server import ClientConnection
from discord.ext import commands
from configure import Configurer
from views import MixesView


def run():
    configurer = Configurer("settings.ini")
    config = configurer.configure()

    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)
    _bot = commands.Bot(command_prefix=config.prefix, client=client, intents=client.intents)

    client_connection = ClientConnection()
    client_connection.connect_to_host(port=8082)

    msg = QByteArray()
    msg.append("Hello")

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

    #_bot.run(config.token)


if __name__ == '__main__':
    run()
