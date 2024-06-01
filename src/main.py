import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import psycopg2
bot = commands.Bot(command_prefix=';', intents=discord.Intents.all())

load_dotenv()
@bot.event
async def on_ready():
    try:
        s = await bot.tree.sync()
        print(f'Synced {len(s)} commands')
    except Exception as e:
        print(f'Error syncing commands: {e}')
    
    print(f'Logged in as {bot.user.name}')

conn = psycopg2.connect(database = "skyblock", 
                        user = os.getenv("USER"), 
                        host= 'localhost',
                        password = os.getenv("PWD"),
                        port = 5432)

@bot.tree.command(name='bank', description='Returns the skyblock bank')
async def bank(interaction: discord.Interaction):
    cur = conn.cursor()
    cur.execute("SELECT * FROM bank")
    rows = cur.fetchall()
    str = "## THE BANK\n";
    total = 0;
    for row in rows:
        player, amount = row
        total += amount
        str += f"**{player}** : {amount}\n"
    str += f"**Total** : {total}"
    await interaction.response.send_message(str)

TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)