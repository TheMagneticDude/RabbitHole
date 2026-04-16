import discord
from discord.ext import commands, tasks
from discord import app_commands
import os


#========================= Constants =========================
#will fill in after to avoid secret being in repo
botToken = '';
#grab token from local env variable
botToken = os.getenv("RABBITHOLE_TOKEN");

GUILD_ID = discord.Object(id=1474226483491897446);

#========================= Global States =========================




#========================= Class =========================
class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!');
        try:
            synced = await self.tree.sync(guild=GUILD_ID)
            print(f"Synced {len(synced)} command(s) to guild.")
        except Exception as e:
            print(e)
        
    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('!rabbithole'):
            await message.channel.send(
                f'Command Recieved: {message.author} executed: {message.content}'
            )

        await self.process_commands(message)
        

#========================= UI Components =========================

    
class ChecklistButton(discord.ui.Button):
    def __init__(self, item_name: str):
        # Start the button as gray (secondary) with an X
        super().__init__(style=discord.ButtonStyle.secondary, label=item_name, emoji="✖️")
        self.item_name = item_name
        self.is_checked = False

    async def callback(self, interaction: discord.Interaction):
        # Toggle the internal state
        self.is_checked = not self.is_checked
        
        # Update the button's appearance based on the new state
        if self.is_checked:
            self.style = discord.ButtonStyle.success # Turns green
            self.emoji = "✅"
        else:
            self.style = discord.ButtonStyle.secondary # Turns gray
            self.emoji = "✖️"
            
        # Edit the message to reflect the new button state
        await interaction.response.edit_message(view=self.view)

class ChecklistView(discord.ui.View):
    def __init__(self, item_list: list):
        super().__init__(timeout=None) # timeout=None prevents the buttons from dying after 3 minutes
        
        # Dynamically create and add a button for every item in the list
        for item in item_list:
            self.add_item(ChecklistButton(item))

#========================= Init =========================
intents = discord.Intents.default();
intents.message_content = True;
client = Client(command_prefix = "!rabbithole", intents = intents);





#========================= Commands =========================
@client.tree.command(name="test", description="hur hur hur", guild = GUILD_ID)
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("hur hur hur.");

@client.tree.command(name="checklist", description="Creates an interactive checklist", guild=GUILD_ID)
@app_commands.describe(title="The title of the checklist", items="Comma-separated list of items")
async def checklistCommand(interaction: discord.Interaction, title: str, items: str):
    
    # 1. Split the string by commas and strip any accidental extra spaces
    item_list = [item.strip() for item in items.split(",") if item.strip()]
    
    # Discord has a strict limit of 25 buttons per message (5 rows of 5)
    if len(item_list) > 25:
        await interaction.response.send_message("❌ You can only have up to 25 items in a checklist!", ephemeral=True)
        return
    elif len(item_list) == 0:
        await interaction.response.send_message("❌ You must provide at least one item!", ephemeral=True)
        return

    # 2. Build a nice embed for the title
    embed = discord.Embed(
        title=f"📋 {title}", 
        description="Click the buttons below to toggle items on and off.",
        color=discord.Color.blurple()
    )
    
    # 3. Create our dynamic view and send it!
    view = ChecklistView(item_list)
    await interaction.response.send_message(embed=embed, view=view)












#run bot
client.run(botToken);
