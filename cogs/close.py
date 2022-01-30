import discord
from discord.ext import commands
import asyncio
import sqlite3

db_path = 'guild.db'

conn = sqlite3.connect(db_path)

c = conn.cursor()

def removeGuild(guild):
    with conn:
        c.execute(f"DELETE from guild WHERE guild = ?", (guild,))



class close(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(aliases=['c'])
    async def close(self, ctx) -> None:
        c.execute(f"SELECT * FROM guild WHERE guild = {ctx.message.guild.id}")
        check = c.fetchone()
        if (check == None):
            message = await ctx.send("There is currently no active game!")
            await asyncio.sleep(4)
            await message.delete()
            return
        if (check[2] == 1):
            message = await ctx.send("Game closed!")
            removeGuild(ctx.message.guild.id)
            await asyncio.sleep(4)
            await message.delete()
            return
        else:
            message = await ctx.send("There is currently no active game!")
            await asyncio.sleep(4)
            await message.delete()
            return




