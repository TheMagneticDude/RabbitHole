import discord
from discord.ext import commands, tasks
from discord import app_commands
import os


#========================= Constants =========================
#will fill in after to avoid secret being in repo
botToken = '';
#grab token from local env variable
botToken = os.getenv("DISCORD_TOKEN");

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

        if message.content.startswith('!rabbit'):
            await message.channel.send(
                f'Command Recieved: {message.author} executed: {message.content}'
            )

        await self.process_commands(message)
        

#========================= UI Components =========================

    
    

#========================= Init =========================
intents = discord.Intents.default();
intents.message_content = True;
client = Client(command_prefix = "!rabbit", intents = intents);





#========================= Commands =========================
@client.tree.command(name="test", description="hur hur hur", guild = GUILD_ID)
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("hur hur hur.");














#run bot
client.run(botToken);
