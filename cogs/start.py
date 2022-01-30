import discord
from discord.ext import commands
import asyncio
import json
import random
from words import words
import sqlite3

db_path = 'guild.db'

conn = sqlite3.connect(db_path)

c = conn.cursor()

def getGuild(guild):
    c.execute(
        f"SELECT * FROM guild WHERE guild = ?", (guild,))
    return c.fetchone()


def insertGuild(guild, new, ongoing, remaining, current, guess):
    with conn:
        c.execute(f"INSERT INTO guild VALUES (?, ?, ?, ?, ?, ?)", (guild, new, ongoing, remaining, current, guess))


def removeGuild(guild):
    with conn:
        c.execute(f"DELETE from guild WHERE guild = ?", (guild,))

def updateLeft(guild, val):
    c.execute(f"SELECT * FROM guild WHERE guild = ?", (guild,))
    check = c.fetchone()
    check = check[3]
    with conn:
        c.execute(f"""UPDATE guild SET remaining = {check-val}
                WHERE guild = {guild}
                """)

def updateCurrent(guild, new):
    with conn:
        c.execute(f"""UPDATE guild SET current = ?
                WHERE guild = ?
                """, (new, guild))

def updateGuess(guild):
    c.execute(f"SELECT * FROM guild WHERE guild = ?", (guild,))
    check = c.fetchone()
    check = check[5]
    with conn:
        c.execute(f"""UPDATE guild SET guess = ?
                WHERE guild = ?
                """, (check - 1, guild))

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

def formEmbed(randword, guess):
    embed = discord.Embed(
            name = 'Hangman!',
            description = f'{lenWO_(randword)} letter word!',
            color = discord.Colour.dark_blue()
        )
    embed.add_field(name='Guess a letter', value = f'{randword}', inline= False)
    embed.set_footer(text=f'You have {guess} guesses left!')
    return embed

class start(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.word = words()



    @commands.command(aliases=['g'])
    async def guess(self, ctx, letter = None) -> None:
        c.execute(f"SELECT * FROM guild WHERE guild = {ctx.message.guild.id}")
        check = c.fetchone()
        count = 0
        if (letter == check[1]):
            removeGuild(ctx.message.guild.id)
            message = await ctx.send("You win!")
            return
        str = ''
        if (not(check[2] == 1)):
            message = await ctx.send("Incorrect usage. Start a new game with [>start new]")
            await asyncio.sleep(4)
            await message.delete()
            return
        if (letter == None):
            message = await ctx.send("Incorrect usage. Guess a letter with [>guess <letter>]")
            await asyncio.sleep(4)
            await message.delete()
            return
        if letter not in check[1]:
            updateGuess(ctx.message.guild.id)
            if check[5] <= 1:
                removeGuild(ctx.message.guild.id)
                message = await ctx.send("You lose :(")
                return
            await ctx.send("Guess again!")
            return
        else:
            for i in range(len(check[1])):
                if (check[1][i] == letter):
                    str += f'{letter}'
                    count += 1
                else:
                    str += check[4][i]
            if (letter not in check[4]):
                updateLeft(ctx.message.guild.id, count)
            else:
                updateGuess(ctx.message.guild.id)
            updateCurrent(ctx.message.guild.id, str)
            c.execute(f"SELECT * FROM guild WHERE guild = {ctx.message.guild.id}")
            check = c.fetchone()
            await ctx.send(embed = formEmbed(check[4], check[5]))
        c.execute(f"SELECT * FROM guild WHERE guild = {ctx.message.guild.id}")
        check = c.fetchone()
        if (check[3] == 0):
            message = await ctx.send("You win!")
            removeGuild(ctx.message.guild.id)
            return
        if check[5] <= 0:
            removeGuild(ctx.message.guild.id)
            message = await ctx.send("You lose :(")
            return
        



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
