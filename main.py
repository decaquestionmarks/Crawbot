# bot.py
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from pathlib import Path

from downloading import get_ts

BASETARGET = 'https://raw.githubusercontent.com/matteoruscitti/Dawn/master/data/'
SANCTTARGET = 'https://raw.githubusercontent.com/matteoruscitti/Dawn/master/data/mods/gen9sanctified/'
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
#AUTH = os.getenv('GIT_AUTH')

#if not Path("baseabilities.ts").exists():
#    get_ts(BASETARGET, "abilities", AUTH , "base")
#if not Path("baselearnsets.ts").exists():
#    get_ts(BASETARGET, "learnsets", AUTH, "base")
#if not Path("basemoves.ts").exists():
#    get_ts(BASETARGET, "moves", AUTH, "base")
#if not Path("basepokedex.ts").exists():
#    get_ts(BASETARGET, "pokedex", AUTH, "base")




intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True
intents.all()

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name = GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
@bot.command(name='info', help='Tells you about the bot')
async def info(ctx):
    await ctx.channel.send(f"{ctx.author.mention} I'm the base 640 bot.")

@bot.command(name='wiki', help='Shows the wiki link')
async def wiki(ctx):
    await ctx.channel.send(f"{ctx.author.mention} https://docs.google.com/document/d/1iY0VdTwpo1d-LvCg-Isl-zxfPQZ3nuafMLdyB044npQ/edit?usp=sharing")

@bot.command(name='sprite', help='Shows a sprite')
async def sprite(ctx, arg):
    await ctx.channel.send(f"https://play.dawn-ps.com/sprites/custom/{arg.lower()}.png")



bot.run(TOKEN)