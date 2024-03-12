# bot.py
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from pathlib import Path

import scrapers
import filters
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

pokemon = scrapers.pokemon_to_dict("basepokedex.ts", {})
pokemon = scrapers.pokemon_to_dict("pokedex.ts", pokemon)
learnsets = scrapers.learnset_to_dict("baselearnsets.ts", {})
learnsets = scrapers.learnset_to_dict("learnsets.ts", learnsets)
moves = scrapers.moves_to_dict("basemoves.ts",{})
moves = scrapers.moves_to_dict("moves.ts", moves)
abilities = scrapers.abilities_to_dict("baseabilities.ts", {})
abilities = scrapers.abilities_to_dict("abilities.ts", abilities)
justnewpokemon = scrapers.pokemon_to_dict("pokedex.ts", {})
oldpokemon = scrapers.pokemon_to_dict("basepokedex.ts", {})
abtext = scrapers.abilities_to_dict("abilitytext.ts",{})
motext = scrapers.moves_to_dict("movestext.ts",{})

def name_convert(arg:str)->str:
    return arg.replace("-", "").replace(" ", "").lower()

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
    try:
        if (arg.lower() in justnewpokemon.keys() or arg.replace("-","").lower() in justnewpokemon.keys()) and arg.lower() not in oldpokemon.keys():
            await ctx.channel.send(f"https://play.dawn-ps.com/sprites/custom/{arg.lower()}.png")
        else:
            await ctx.channel.send("I cannot find that sprite")
    except Exception as e:
        await ctx.channel.send(f"An Error has occurred, {e.__class__.__name__}: {e}")

@bot.command(name='dt', help='Shows info about a Pokemon')
async def data(ctx, *args):
    try:
        arg = " ".join(args)
        arg = name_convert(arg)
        print(arg)
        embed = discord.Embed()
        if arg in pokemon.keys():
            embed = discord.Embed(title = pokemon[arg]["name"][1:-1])
            embed.add_field(name = "Type", value = "/".join(pokemon[arg]["types"]).replace("'",""), inline = False)
            embed.add_field(name = "Abilities", value = str(pokemon[arg]["abilities"])[1:-1].replace("'",""), inline = False)
            embed.add_field(name = "Stats", value = "/".join(str(value) for value in list(pokemon[arg]["baseStats"].values())))
            embed.add_field(name = "Total", value=sum(list(pokemon[arg]["baseStats"].values())), inline = True)
        elif arg in moves.keys():
            embed = discord.Embed(title = moves[arg]["name"][1:-1])
            try:
                embed.description = motext[arg]["shortDesc"][1:-1]
            except KeyError:
                embed.description = "Unchanged"
            embed.add_field(name = "Type", value = moves[arg]["type"][1:-1], inline = True)
            embed.add_field(name = "Power", value = moves[arg]["basePower"], inline = True)
            embed.add_field(name = "Category", value = moves[arg]["category"][1:-1], inline = True)
            embed.add_field(name = "Accuracy", value = str(moves[arg]["accuracy"])+"%", inline=True)
            embed.add_field(name = "PP", value = int(int(moves[arg]["pp"])*(16/10)),inline = True)
            embed.add_field(name = "Priority", value = int(moves[arg]["priority"]), inline = True)
            embed.add_field(name = "flags", value = ", ".join(list(moves[arg]["flags"].keys())), inline= False)

        elif arg in abilities.keys():
            embed = discord.Embed(title = abilities[arg]["name"][1:-1])
            try:
                embed.description = abtext[arg]["shortDesc"][1:-1]
            except KeyError:
                embed.description = "Unchanged"
        else:
            await ctx.channel.send("No data could be found in Pokemon, Moves, or Abilities")
        if embed.title is not None:
            await ctx.channel.send(embed = embed)
    except Exception as e:
        await ctx.channel.send(f"An Error has occurred, {e.__class__.__name__}: {e}")

@bot.command(name='ds', help='Searches for pokemon that match the criteria')
async def dexsearch(ctx, *args):
    pass

@bot.command(name = 'ms', help = 'Searches for moves that match the criteria')
async def movesearch(ctx, *args):
    pass

@bot.command(name = 'learn', help = 'Tells if a pokemon can learn a move')
async def learn(ctx, *args):
    try:
        args = " ".join(args)
        args = args.split(",")
        print(args)
        args[0] = name_convert(args[0])
        if args[0] in learnsets.keys() and args[0] in pokemon.keys():
            args[1] = name_convert(args[1])
            if args[1] in moves.keys():
                if name_convert(args[1]) in learnsets[args[0]]:
                    await ctx.channel.send(f"{moves[args[1]]["name"][1:-1]} is learnable by {pokemon[args[0]]["name"][1:-1]}")
                else:
                    await ctx.channel.send(
                        f"{moves[args[1]]["name"][1:-1]} is not learnable by {pokemon[args[0]]["name"][1:-1]}")
            else:
                await ctx.channel.send(f"Move {args[1]} cannot be found in the database")
        else:
            await ctx.channel.send(f"Pokemon {args[0]} cannot be found in the database")
    except Exception as e:
        await ctx.channel.send(f"An Error has occurred, {e.__class__.__name__}: {e}")

@bot.command(name = 'weak', help = 'Shows a pokemon\'s or type\'s weaknesses')
async def weakness(ctx, *args):
    pass

@bot.command(name = 'coverage', help = 'Shows the type coverage for a set of types')
async def coverage(ctx, *args):
    pass

@bot.command(name = 'randpoke', help = 'Returns a random pokemon that matches the criteria')
async def randompokemon(ctx, *args):
    pass

bot.run(TOKEN)