import asyncio
import encodings

import discord
import json

from PyQt5.QtCore import QByteArray, QDataStream
from PyQt5.QtNetwork import QHostAddress, QAbstractSocket

from protocol import Protocol
from server import PendingConnection
from discord.ext import commands
from configure import Configurer
from views import MixesView


def p():
    print("data received")


def run():
    configurer = Configurer("settings.ini")
    config = configurer.configure()

    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)
    _bot = commands.Bot(command_prefix=config.prefix, client=client, intents=client.intents)

    sclient = PendingConnection()
    sclient.socket.connectToHost(QHostAddress('127.0.0.1'), 8082)

    if not sclient.socket.waitForConnected(1000):
        raise Exception('failed to connect')

    sclient.socket.readyRead.connect(p)
    msg = QByteArray()
    msg.append("Hello")

    if not sclient.send(command=Protocol.Bot.hello.value, data=msg):
        print("failed to send data")

    # server = Server(QHostAddress('127.0.0.1'), 8083)
    # server.listen()

    @_bot.event
    async def on_ready():
        print('started')

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

    _bot.run(config.token)


if __name__ == '__main__':
    run()
