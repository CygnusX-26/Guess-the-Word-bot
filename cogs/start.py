import discord
from discord.ext import commands
import asyncio
import json
import random
from cogs.words import words
import sqlite3

db_path = 'guild.db'

conn = sqlite3.connect(db_path)

c = conn.cursor()

#sqlite Methods

def insertGuild(guild, new, ongoing, remaining, current, guess):
    with conn:
        c.execute(f"INSERT INTO guild VALUES (?, ?, ?, ?, ?, ?)", (guild, new, ongoing, remaining, current, guess))

#Text editing methods
def underScore(word: str, letter = None) -> str:
    st = ""
    if (letter == None):
        for i in range(len(word)):
            st += "?"
        return st
    for i in range(len(word)):
        if (word[i] == letter):
            st += f'{letter} '
        else:
            st += word[i]
    return st

def lenWO_(word: str) -> int:
    count = 0
    for i in range(len(word)):
        if word[i] == " ":
            continue
        else:
            count += 1
    return count

def add_space(text):
    str = ""
    for i in range(len(text)):
        str += f"`{text[i]}` "
    return str

def formEmbed(randword, guess):
    embed = discord.Embed(
            name = 'Hangman!',
            description = f'{lenWO_(randword)} letter word!',
            color = discord.Colour.dark_blue()
        )
    embed.add_field(name='Guess a letter', value = f'{add_space(randword)}', inline= False)
    embed.set_footer(text=f'You have {guess} guesses left!')
    return embed

class start(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.word = words()

    @commands.command(aliases=['s'])
    async def start(self, ctx, new = None) -> None:
        if new != "new":
            message = await ctx.send("Incorrect usage. Start a new game with [>start new]")
            await asyncio.sleep(4)
            await message.delete()
            return
        id = ctx.message.guild.id
        c.execute(f"SELECT * FROM guild WHERE guild = {id}")
        check = c.fetchall()
        if (len(check) == 0):
            word = self.word.getNewWord()
            insertGuild(id, word, 1, len(word), underScore(word), 10)

            c.execute(f"SELECT * FROM guild WHERE guild = {id}")
            check = c.fetchone()
            print(check)

            embed = formEmbed(underScore(check[1]), check[5])

            await ctx.send(embed=embed)
        else:
            c.execute(f"SELECT * FROM guild WHERE guild = {id}")
            check = c.fetchone()
            if (check[2] == 1):
                message = await ctx.send("There is currently an ongoing game! Please wait for it to finish.")
                await asyncio.sleep(4)
                await message.delete()
                return
            else:
                word = self.word.getNewWord()
                insertGuild(id, word, 1, len(word), underScore(word))

                c.execute(f"SELECT * FROM guild WHERE guild = {id}")
                check = c.fetchone()
                print(check)

                embed = formEmbed(underScore(check[1]), check[5])

                await ctx.send(embed=embed)
