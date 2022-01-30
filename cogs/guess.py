from email import message
import discord
from discord.ext import commands
from cogs.start import start
from cogs.words import words
import asyncio
import sqlite3

db_path = 'guild.db'

conn = sqlite3.connect(db_path)

c = conn.cursor()

#sqlite Methods

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

#Text editing methods

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

class guess(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['g'])
    async def guess(self, ctx, letter = None) -> None:
        if (letter == None):
            message = await ctx.send("Incorrect usage. Guess a letter with [>guess <letter>]")
            await asyncio.sleep(4)
            await message.delete()
            return
        c.execute(f"SELECT * FROM guild WHERE guild = {ctx.message.guild.id}")
        check = c.fetchone()
        count = 0
        if (not(check[2] == 1)):
            message = await ctx.send("Incorrect usage. Start a new game with [>start new]")
            await asyncio.sleep(4)
            await message.delete()
            return
        if (letter == check[1]):
            c.execute(f"SELECT * FROM guild WHERE guild = {ctx.message.guild.id}")
            check = c.fetchone()
            await ctx.send(embed = formEmbed(check[1], check[5]))
            removeGuild(ctx.message.guild.id)
            message = await ctx.send("You win!")
            return
        elif (len(letter) > 1):
            updateGuess(ctx.message.guild.id)
            c.execute(f"SELECT * FROM guild WHERE guild = {ctx.message.guild.id}")
            check = c.fetchone()
            if check[5] <= 0:
                removeGuild(ctx.message.guild.id)
                message = await ctx.send("You lose :(")
                return

            await ctx.send(f"Guess again! {check[5]} guesses remaining")
            return
        str = ''
        if (not(check[2] == 1)):
            message = await ctx.send("Incorrect usage. Start a new game with [>start new]")
            await asyncio.sleep(4)
            await message.delete()
            return
        if letter not in check[1]:
            updateGuess(ctx.message.guild.id)
            c.execute(f"SELECT * FROM guild WHERE guild = {ctx.message.guild.id}")
            check = c.fetchone()
            if check[5] <= 0:
                removeGuild(ctx.message.guild.id)
                message = await ctx.send("You lose :(")
                return
            
            await ctx.send(f"Guess again! {check[5]} guesses remaining")
            return
        elif check[3] > 0:
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
            if (check[3] == 0):
                await ctx.send(embed = formEmbed(check[4], check[5]))
                await ctx.send("You win!")
                removeGuild(ctx.message.guild.id)
                return
            else:
                await ctx.send(embed = formEmbed(check[4], check[5]))
        else:
            c.execute(f"SELECT * FROM guild WHERE guild = {ctx.message.guild.id}")
            check = c.fetchone()
            if (check[3] == 0):
                await ctx.send(embed = formEmbed(check[4], check[5]))
                await ctx.send("You win!")
                removeGuild(ctx.message.guild.id)
                return
            if check[5] <= 0:
                removeGuild(ctx.message.guild.id)
                message = await ctx.send("You lose :(")
                return

