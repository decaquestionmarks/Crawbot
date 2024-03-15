# bot.py
import os
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands
from pathlib import Path

import scrapers
from matchups import CHART
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
TYPES = ["normal","fire","water","grass","electric","psychic","ice","fighting","flying","poison","ground","rock","bug","ghost","dragon","dark","steel","fairy","elastic","clean"]
CATEGORIES = ["physical","special","status"]
STATS = ["atk","def","hp","spa","spd","spe"]
FLAGS = ['gravity', 'recharge', 'mirror', 'failencore', 'bite', 'mustpressure', 'failmimic', 'failinstruct', 'metronome', 'bypasssub', 'nonsky', 'nosleeptalk', 'reflectable', 'noparentalbond', 'distance', 'snatch', 'futuremove', 'wind', 'defrost', 'noassist', 'allyanim', 'protect', 'heal', 'punch', 'contact', 'failmefirst', 'failcopycat', 'pledgecombo', 'dance', 'charge', 'sound', 'pulse', 'slicing', 'bullet', 'powder', 'cantusetwice']

def name_convert(arg:str)->str:
    return arg.replace("-", "").replace(" ", "").lower()

def getweak(types:list) -> list[set]:
    types = [name_convert(i) for i in types]
    if types == ["bird","normal"]:
        types = ["normal"]
    ret = [set(),set(TYPES),set(),set()]
    for i in types:
        #print(ret)
        ret[0] |= CHART[i]["def"][0]
        ret[2] |= CHART[i]["def"][1]
        ret[3] |= CHART[i]["def"][2]
        for e in ret[0].copy():
            if e in ret[2]:
                ret[0].remove(e)
                ret[2].remove(e)
                ret[1].add(e)
        for e in ret[3]:
            if e in ret[2]:
                ret[2].remove(e)
            if e in ret[0]:
                ret[0].remove(e)
        ret[1] -= ret[0]
        ret[1] -= ret[2]
        ret[1] -= ret[3]
        #print(ret)
    return ret
def getcoverage(types:list) -> list[set]:
    pass

def chainlearn(p:str, move:str):
    if "prevo" not in pokemon[p].keys() or name_convert(pokemon[p]["prevo"][1:-1]) not in learnsets.keys():
        return move in learnsets[p]
    else:
        return move in learnsets[p] or chainlearn(name_convert(pokemon[p]["prevo"][1:-1]),move)

def dsearch(keys:list, values:list):
    keys = set(keys)
    for value in values:
        if "|" in value:
            newvalues = value.split("|")
            newkeys = set()
            for v in newvalues:
                newkeys = newkeys | set(dsearch(keys, [v]))
            keys = newkeys
        elif name_convert(value).startswith("!"):
            newvalues = []
            newvalues.append(value.strip()[1:])
            keys = keys - set(dsearch(keys,newvalues))
        elif name_convert(value) in TYPES:
            value = name_convert(value)
            value = value[:1].upper() + value[1:]
            keys = {key for key in keys if value in pokemon[key]["types"]}
        elif name_convert(value) in abilities.keys():
            value = name_convert(value)
            keys = {key for key in keys if value in [name_convert(ab) for ab in pokemon[key]["abilities"].values()]}
        elif name_convert(value) in moves.keys():
            value = name_convert(value)
            keys = {key for key in keys if (key in learnsets.keys() and chainlearn(key, value))}
        elif ">=" in value:
            value = value.split(">=")
            if name_convert(value[0]) in STATS:
                keys = {key for key in keys if (pokemon[key]["baseStats"][name_convert(value[0])]>=int(value[1]))}
            if name_convert(value[0]) == "weight":
                keys = {key for key in keys if (float(pokemon[key]["weightkg"]) >= float(value[1]))}
            if name_convert(value[0]) == "height":
                keys = {key for key in keys if (float(pokemon[key]["heightm"]) >= float(value[1]))}
        elif "<=" in value:
            value = value.split("<=")
            if name_convert(value[0]) in STATS:
                keys = {key for key in keys if
                        (pokemon[key]["baseStats"][name_convert(value[0])] <= int(value[1]))}
            if name_convert(value[0]) == "weight":
                keys = {key for key in keys if (float(pokemon[key]["weightkg"]) <= float(value[1]))}
            if name_convert(value[0]) == "height":
                keys = {key for key in keys if (float(pokemon[key]["heightm"]) <= float(value[1]))}
        elif "=" in value:
            value = value.split("=")
            if name_convert(value[0]) in STATS:
                keys = {key for key in keys if
                        (pokemon[key]["baseStats"][name_convert(value[0])] == int(value[1]))}
            if name_convert(value[0]) == "weight":
                keys = {key for key in keys if (float(pokemon[key]["weightkg"]) == float(value[1]))}
            if name_convert(value[0]) == "height":
                keys = {key for key in keys if (float(pokemon[key]["heightm"]) == float(value[1]))}
        elif ">" in value:
            value = value.split(">")
            if name_convert(value[0]) in STATS:
                keys = {key for key in keys if
                        (pokemon[key]["baseStats"][name_convert(value[0])] > int(value[1]))}
            if name_convert(value[0]) == "weight":
                keys = {key for key in keys if (float(pokemon[key]["weightkg"]) > float(value[1]))}
            if name_convert(value[0]) == "height":
                keys = {key for key in keys if (float(pokemon[key]["heightm"]) > float(value[1]))}
        elif "<" in value:
            value = value.split("<")
            if name_convert(value[0]) in STATS:
                keys = {key for key in keys if
                        (pokemon[key]["baseStats"][name_convert(value[0])] < int(value[1]))}
            if name_convert(value[0]) == "weight":
                keys = {key for key in keys if (float(pokemon[key]["weightkg"]) < float(value[1]))}
            if name_convert(value[0]) == "height":
                keys = {key for key in keys if (float(pokemon[key]["heightm"]) < float(value[1]))}
        elif name_convert(value) == "hasset":
            keys = {key for key in keys if key in learnsets.keys() and len(learnsets[key])>0}
        elif name_convert(value) == "fe":
            keys = {key for key in keys if "evos" not in pokemon[key].keys()}
        elif name_convert(value) == "nfe":
            keys = {key for key in keys if "evos" in pokemon[key].keys() and "prevo" in pokemon[key].keys()}
        elif name_convert(value) == "lc":
            keys = {key for key in keys if "evos" in pokemon[key].keys() and "prevo" not in pokemon[key].keys()}
        elif name_convert(value).startswith("weak"):
            t = name_convert(value.split(" ")[1])
            keys = {key for key in keys if t in getweak(pokemon[key]["types"])[0]}
        elif name_convert(value).startswith("resists"):
            t = name_convert(value.split(" ")[1])
            keys = {key for key in keys if t in getweak(pokemon[key]["types"])[2] or t in getweak(pokemon[key]["types"])[3]}
    return sorted(list(keys))

def msearch(keys:list, values:list):
    keys = set(keys)
    for value in values:
        if "|" in value:
            newvalues = value.split("|")
            newkeys = set()
            for v in newvalues:
                newkeys = newkeys | set(msearch(keys, [v]))
            keys = newkeys
        elif name_convert(value).startswith("!"):
            newvalues = []
            newvalues.append(name_convert(value)[1:])
            keys = keys - set(msearch(keys,newvalues))
        elif name_convert(value) in TYPES:
            value = name_convert(value)
            value = value[:1].upper() + value[1:]
            keys = {key for key in keys if moves[key]["type"][1:-1]==value}
        elif name_convert(value) in learnsets.keys():
            value = name_convert(value)
            keys = {key for key in keys if (value in learnsets.keys() and chainlearn(value, key))}
            #keys &= set(learnsets[value])
        elif name_convert(value) in CATEGORIES:
            value = name_convert(value)
            value = value[:1].upper() + value[1:]
            keys = {key for key in keys if moves[key]["category"][1:-1] == value}
        elif name_convert(value) in FLAGS:
            value = name_convert(value)
            keys = {key for key in keys if type(moves[key]["flags"]) == dict and value in moves[key]["flags"].keys()}
        elif ">=" in value:
            value = value.split(">=")
            if name_convert(value[0]) == "bp":
                keys = {key for key in keys if (float(moves[key]["basePower"]) >= float(value[1]))}
            if name_convert(value[0]) == "acc":
                keys = {key for key in keys if (moves[key]["accuracy"]=="true" or float(moves[key]["accuracy"]) >= float(value[1]))}
            if name_convert(value[0]) == "pp":
                keys = {key for key in keys if (float(moves[key]["pp"]) >= float(value[1]))}
            if name_convert(value[0]) == "priority":
                keys = {key for key in keys if (float(moves[key]["priority"]) >= float(value[1]))}
        elif "<=" in value:
            value = value.split("<=")
            if name_convert(value[0]) == "bp":
                keys = {key for key in keys if (float(moves[key]["basePower"]) <= float(value[1]))}
            if name_convert(value[0]) == "acc":
                keys = {key for key in keys if (moves[key]["accuracy"]!="true" and float(moves[key]["accuracy"]) <= float(value[1]))}
            if name_convert(value[0]) == "pp":
                keys = {key for key in keys if (float(moves[key]["pp"]) <= float(value[1]))}
            if name_convert(value[0]) == "priority":
                keys = {key for key in keys if (float(moves[key]["priority"]) <= float(value[1]))}
        elif "=" in value:
            value = value.split("=")
            if name_convert(value[0]) == "bp":
                keys = {key for key in keys if (float(moves[key]["basePower"]) == float(value[1]))}
            if name_convert(value[0]) == "acc":
                keys = {key for key in keys if ((moves[key]["accuracy"]) == (value[1].strip()))}
            if name_convert(value[0]) == "pp":
                keys = {key for key in keys if (float(moves[key]["pp"]) == float(value[1]))}
            if name_convert(value[0]) == "priority":
                keys = {key for key in keys if (float(moves[key]["priority"]) == float(value[1]))}
        elif ">" in value:
            value = value.split(">")
            if name_convert(value[0]) == "bp":
                keys = {key for key in keys if (float(moves[key]["basePower"]) > float(value[1]))}
            if name_convert(value[0]) == "acc":
                keys = {key for key in keys if (moves[key]["accuracy"]=="true" or float(moves[key]["accuracy"]) > float(value[1]))}
            if name_convert(value[0]) == "pp":
                keys = {key for key in keys if (float(moves[key]["pp"]) > float(value[1]))}
            if name_convert(value[0]) == "priority":
                keys = {key for key in keys if (float(moves[key]["priority"]) > float(value[1]))}
        elif "<" in value:
            value = value.split("<")
            if name_convert(value[0]) == "bp":
                keys = {key for key in keys if (float(moves[key]["basePower"]) < float(value[1]))}
            if name_convert(value[0]) == "acc":
                keys = {key for key in keys if (moves[key]["accuracy"]!="true" and float(moves[key]["accuracy"]) < float(value[1]))}
            if name_convert(value[0]) == "pp":
                keys = {key for key in keys if (float(moves[key]["pp"]) < float(value[1]))}
            if name_convert(value[0]) == "priority":
                keys = {key for key in keys if (float(moves[key]["priority"]) < float(value[1]))}


    return sorted(list(keys))


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
    message = random.choice(["I'm the base 640 bot.", "Careful, I'm a bit of Klutz.", "Worst STABs since 2020.", "I wonder what I can't learn?"])
    await ctx.channel.send(f"{ctx.author.mention}"+message)

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
    try:
        args = (" ".join(args)).split(",")
        ret  = dsearch(list(pokemon.keys()),args)
        if len(ret) != 1486 and len(ret) != 0:
            ret = ", ".join([pokemon[key]["name"][1:-1]for key in ret])
            while len(ret)>2000:
                await ctx.channel.send(", ".join(ret.split(", ")[:100]))
                ret = ", ".join(ret.split(", ")[100:])
            await ctx.channel.send(ret)
        elif len(ret) == 0:
            await ctx.channel.send("Search resulted in no Pokemon.")
        else:
            await ctx.channel.send("Search resulted in all Pokemon.")
    except Exception as e:
        await ctx.channel.send(f"An Error has occurred, {e.__class__.__name__}: {e}")

@bot.command(name = 'ms', help = 'Searches for moves that match the criteria')
async def movesearch(ctx, *args):
    try:
        args = (" ".join(args)).split(",")
        ret = msearch(list(moves.keys()), args)
        if len(ret) != 1040 and len(ret) != 0:
            ret = ", ".join([moves[key]["name"][1:-1] for key in ret])
            while len(ret) > 2000:
                await ctx.channel.send(", ".join(ret.split(", ")[:100]))
                ret = ", ".join(ret.split(", ")[100:])
            await ctx.channel.send(ret)
        elif len(ret) == 0:
            await ctx.channel.send("Search resulted in no Moves.")
        else:
            await ctx.channel.send("Search resulted in all Moves.")
    except Exception as e:
        await ctx.channel.send(f"An Error has occurred, {e.__class__.__name__}: {e}")

@bot.command(name = 'learn', help = 'Tells if a pokemon can learn a move')
async def learn(ctx, *args):
    try:
        args = " ".join(args)
        args = args.split(",")
        args[0] = name_convert(args[0])
        if args[0] in learnsets.keys() and args[0] in pokemon.keys():
            args[1] = name_convert(args[1])
            if args[1] in moves.keys():
                if chainlearn(args[0], name_convert(args[1])):
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

@bot.command(name = 'weak', help = 'Shows a pokemon\'s or type\'s weaknesses(In Progress)')
async def weakness(ctx, *args):
    try:
        args = (" ".join(args)).split(",")
        ret = getweak(args)
        #print(ret)
        ret = [sorted([value[:1].upper() + value[1:] for value in s]) for s in ret]
        embed = discord.Embed(title = ",".join(args))
        embed.add_field(name = "Weak: ", value = ", ".join(ret[0]), inline = False)
        embed.add_field(name = "Neutral: ", value = ", ".join(ret[1]), inline = False)
        embed.add_field(name = "Resists: ", value = ", ".join(ret[2]), inline = False)
        if len(ret[3])!=0:
            embed.add_field(name = "Immune: ", value = ", ".join(ret[3]), inline = False)
        await ctx.channel.send(embed=embed)
    except Exception as e:
        await ctx.channel.send(f"An Error has occurred, {e.__class__.__name__}: {e}")

@bot.command(name = 'coverage', help = 'Shows the type coverage for a set of types(In Progress)')
async def coverage(ctx, *args):
    pass

@bot.command(name = 'randpoke', help = 'Returns a random pokemon that matches the criteria')
async def randompokemon(ctx, *args):
    try:
        args = (" ".join(args)).split(",")
        amount = args[0]
        args = args[1:]
        if int(amount) <= 24:
            ret = dsearch(list(pokemon.keys()), args)
            ret = random.choices(ret, k=int(amount))
            ret = ", ".join([pokemon[key]["name"][1:-1] for key in ret])
            await ctx.channel.send(ret)
        else:
            await ctx.channel.send("I will not generate that many random pokemon")
    except Exception as e:
        await ctx.channel.send(f"An Error has occurred, {e.__class__.__name__}: {e}")

bot.run(TOKEN)