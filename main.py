import discord
from discord.ext import commands
from discord.ext.commands import bot
from configure import Configurer


configurer = Configurer("settings.ini")
configurer.configure()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix=configurer.prefix, client=client, intents=client.intents)

@bot.event
async def on_ready():
    print('Hello world')


@bot.event
async def on_message(message):
    if message.author != bot.user:
        await message.channel.send('Hello!')


if __name__ == '__main__':
    bot.run(configurer.token)
