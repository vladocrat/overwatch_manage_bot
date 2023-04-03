import discord
from discord.ext import commands
from discord.ext.commands import bot
from configure import Configurer
from views import MixesView


def run():
    configurer = Configurer("settings.ini")
    config = configurer.configure()

    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)
    _bot = commands.Bot(command_prefix=config.prefix, client=client, intents=client.intents)

    @_bot.event
    async def on_ready():
        print('started')

    @_bot.command("mixes")
    async def mixes(ctx):
        view = MixesView()
        message = "Mixes are scheduled to..."
        await ctx.send(message, view=view)
        await view.wait()

    _bot.run(config.token)


if __name__ == '__main__':
    run()
