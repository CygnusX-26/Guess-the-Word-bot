import discord
from discord.ext import commands


class bot(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('This bot is online!')
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Game("Generating words..."))

    @commands.command(aliases=['h'])
    async def help(self, ctx):
        pass
