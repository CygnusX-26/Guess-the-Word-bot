import discord
import os
from discord.ext import commands
from cogs.bot import bot
from cogs.start import start
from cogs.guess import guess
from cogs.close import close
import sqlite3
from os.path import join, dirname, abspath

#db_path = join(dirname(dirname(abspath(__file__))), 'data/guild.db')
db_path = 'guild.db'

conn = sqlite3.connect(db_path)

c = conn.cursor()


# creates a new user table if one doesn't currently exist
try:
    c.execute("""CREATE TABLE guild (
            guild int,
            new text,
            ongoing int,
            remaining int,
            current text,
            guess int
            )""")

except:
    pass


intents = discord.Intents.all()
client = commands.Bot(command_prefix= os.getenv("DISCORD_BOT_PREFIX"), intents=intents)
client.remove_command('help')


client.add_cog(bot(client))
client.add_cog(start(client))
client.add_cog(close(client))
client.add_cog(guess(client))

client.run(os.getenv("DISCORD_BOT_TOKEN"))