from email import message
import discord
from discord.ext import commands
from cogs.start import start
from words import words


class guess(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # @commands.command(aliases=['g'])
    # async def guess(self, ctx):
    #     word = words()
    #     wordCur = word.getCurrent()
    #     print(wordCur)

