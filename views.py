import discord


class MixesView(discord.ui.View):

    @discord.ui.button(label="Will come", style=discord.ButtonStyle.success)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("you have been signed to...")

    @discord.ui.button(label="Won't come", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(":^(")
