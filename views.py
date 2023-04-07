import discord
from discord.ext import tasks, commands


class MixesView(discord.ui.View):

    @discord.ui.button(label="Will come", style=discord.ButtonStyle.success)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("msg")
        self.stop()
