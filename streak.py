import discord
from discord.ext import commands
from discord.ext.commands import Bot
import collections
import os

BOT_PREFIX = os.environ['prefix']  # -Prfix is need to declare a Command in discord ex: !pizza "!" being the Prefix
TOKEN = os.environ['token']  # The token is also substituted for security reasons

bot = Bot(command_prefix=BOT_PREFIX)

streaks = {}

pots = collections.defaultdict(list)
total_pot = collections.defaultdict(list)


@bot.command()
@commands.has_role("Host")
async def b(ctx, member: discord.Member, bet: float):
    global total_pot
    payout = round(bet*1.8, 2)
    new_pot = round(bet*2, 2)
    temp_str = pots[ctx.author.id]
    formatted_string = f'<@{member.id}>'
    count = 0
    bets_exist = False
    for bets in temp_str:
        if formatted_string in bets:
            bets_exist = True
            new_payout = float(pots[ctx.author.id][count].split()[4]) + float(payout)
            new_bet = float(pots[ctx.author.id][count].split()[2]) + float(bet)
            pots[ctx.author.id][count] = f'<@{member.id}> **Bet**: {new_bet} **Payout**: {new_payout}'
        count += 1
    if not bets_exist:
        pots[ctx.author.id].append(f'<@{member.id}> **Bet**: {bet} **Payout**: {payout}')
    total_pot[ctx.author.id].append(f'{new_pot}')
    await ctx.send(embed=discord.Embed(
        title='Confirmation',
        description='```Added to the pot```'
    ))


@bot.command(name="potreset")
@commands.has_role("Host")
async def pot_reset(ctx):
    global total_pot
    user = ctx.author.id
    total_pot.pop(user, None)
    pots.pop(user, None)
    await ctx.send(embed=discord.Embed(
        title='Pot Reset',
        description='Pot has been reset'
    ))


@bot.command(name="pot")
async def pot(ctx, member: discord.Member = None):
    user_pot = 0.0
    if member is None:
        user = ctx.author.id
    else:
        user = member.id

    msg = ""

    if user in pots:
        for bets in pots[user]:
            msg += bets + "\n"
    else:
        msg = "User has no pot"

    if msg == "":
        msg = "User has no pot"
    for numbers in total_pot[user]:
        user_pot += float(numbers)
    await ctx.send(embed=discord.Embed(
        title='Pot',
        description=f'{msg} \n ```Total pot: {user_pot}```'
    ))


@bot.command(name="win")
@commands.has_role("Host")
async def win(ctx):

    if str(ctx.message.author.id) in streaks:

        streaks[str(ctx.message.author.id)].insert(0, "<:win:489151982918172723>")
    else:
        streaks[str(ctx.message.author.id)] = []
        streaks[str(ctx.message.author.id)].append("<:win:489151982918172723>")

    user_pot = 0.0
    user = ctx.message.author.id
    msg = ""
    global total_pot

    if user in pots:
        for bets in pots[user]:
            msg += bets + "\n"
    else:
        msg = "User has no pot"

    if msg == "":
        msg = "User has no pot"
    for numbers in total_pot[user]:
        user_pot += float(numbers)
    await ctx.send(embed=discord.Embed(
        title='Pot',
        description=f'{msg} \n ```Total pot: {user_pot}```'
    ))

    pots.pop(user, None)
    total_pot.pop(user, None)

    user = ctx.message.author
    embed = discord.Embed()
    wins = 0
    lossed = 0
    total = "0"
    message_to_send = ""
    if str(user.id) in streaks:
        for streakEmote in streaks[str(user.id)]:
            if not message_to_send == "":
                message_to_send = message_to_send + "," + streakEmote
            else:
                message_to_send = streakEmote
            if streakEmote == "<:loss:489151983018704896>":
                lossed = lossed + 1
            elif streakEmote == "<:win:489151982918172723>":
                wins = wins + 1

        total = wins + lossed
    embed.set_author(name=user.name, icon_url=user.avatar_url)
        
    embed.set_footer(text="WINS: "+str(wins)+"		LOSS: "+str(lossed)+"		TOTAL DUELS: "+str(total))
    if message_to_send == "":
        message_to_send = "Nothing"
        
    embed.add_field(name="All Streaks", value=message_to_send)
        
    await ctx.message.channel.send(embed=embed)


@bot.command(name="loss")
@commands.has_role("Host")
async def loss(ctx):
    
    if str(ctx.message.author.id) in streaks:
    
        streaks[str(ctx.message.author.id)].insert(0, "<:loss:489151983018704896>")
    else:
        streaks[str(ctx.message.author.id)] = []
        streaks[str(ctx.message.author.id)].append("<:loss:489151983018704896>")

    user = ctx.message.author.id
    msg = ""
    user_pot = 0.0
    global total_pot

    if user in pots:
        for bets in pots[user]:
            msg += bets + "\n"
    else:
        msg = "User has no pot"

    if msg == "":
        msg = "User has no pot"
    for numbers in total_pot[user]:
        user_pot += float(numbers)
    await ctx.send(embed=discord.Embed(
        title='Pot',
        description=f'{msg} \n ```Total pot: {user_pot}```'
    ))

    pots.pop(user, None)
    total_pot.pop(user, None)

    user = ctx.message.author
    embed = discord.Embed()
    wins = 0
    lossed = 0
    total = "0"
    message_to_send = ""
    if str(user.id) in streaks:
        for streakEmote in streaks[str(user.id)]:
            if not message_to_send == "":
                message_to_send = message_to_send + "," + streakEmote
            else:
                message_to_send = streakEmote
            if streakEmote == "<:loss:489151983018704896>":
                lossed = lossed + 1
            elif streakEmote == "<:win:489151982918172723>":
                wins = wins + 1

        total = wins + lossed
    embed.set_author(name=user.name, icon_url=user.avatar_url)
        
    embed.set_footer(text="WINS: "+str(wins)+"		LOSS: "+str(lossed)+"		TOTAL DUELS: "+str(total))
    if message_to_send == "":
        message_to_send = "Nothing"
        
    embed.add_field(name="All Streaks", value=message_to_send)
        
    await ctx.message.channel.send(embed=embed)


@bot.command(name="fresh")
@commands.has_role("Host")
async def fresh(ctx):
    
    if str(ctx.message.author.id) in streaks:
    
        streaks[str(ctx.message.author.id)].insert(0, "<:fresh:489151981789904917>")
    else:
        streaks[str(ctx.message.author.id)] = []
        streaks[str(ctx.message.author.id)].append("<:fresh:489151981789904917>")

    user = ctx.message.author
    embed = discord.Embed()
    wins = 0
    lossed = 0
    total = "0"
    message_to_send = ""
    if str(user.id) in streaks:
        for streakEmote in streaks[str(user.id)]:
            if not message_to_send == "":
                message_to_send = message_to_send + "," + streakEmote
            else:
                message_to_send = streakEmote
            if streakEmote == "<:loss:489151983018704896>":
                lossed = lossed + 1
            elif streakEmote == "<:win:489151982918172723>":
                wins = wins + 1

        total = wins + lossed
    embed.set_author(name=user.name, icon_url=user.avatar_url)
        
    embed.set_footer(text="WINS: "+str(wins)+"		LOSS: "+str(lossed)+"		TOTAL DUELS: "+str(total))
    if message_to_send == "":
        message_to_send = "Nothing"
        
    embed.add_field(name="All Streaks", value=message_to_send)
        
    await ctx.message.channel.send(embed=embed)
    

@bot.command(name="streakreset")
@commands.has_role("Host")
async def streakreset(ctx):
    
    streaks[str(ctx.message.author.id)] = []
    total_pot[ctx.message.author.id] = []


async def is_zach(ctx):
    return ctx.author.id == 209081432956600320


@bot.command(name="zach")
@commands.check(is_zach)
async def zach(ctx):
    await ctx.send("Zach is the best cashier in StakeLand")


@bot.command(name="slowbarry")
@commands.has_role("Super Nerdy")
async def slowbarry(ctx):
    await ctx.send("```Deep Breaths Barry, Slow down```")


@bot.command(name="stop")
@commands.has_role("Super Nerdy")
async def stop(ctx):
    await ctx.send("```I think it would be a good idea for you to stop now. ```")


@bot.command(name="streak")
async def streak(ctx, member: discord.Member = None):

    if member is None: 
        user = ctx.message.author
    else:
        user = member

    valid_host = False
    roles = user.roles
    for role in roles:
        if str(role) == "Host":
            valid_host = True

    if valid_host:
        embed = discord.Embed()
        wins = 0
        lossed = 0
        total = "0"
        message_to_send = ""
        if str(user.id) in streaks:
            for streakEmote in streaks[str(user.id)]:
                if not message_to_send == "":
                    message_to_send = message_to_send + "," + streakEmote
                else:
                    message_to_send = streakEmote
                if streakEmote == "<:loss:489151983018704896>":
                    lossed = lossed + 1
                elif streakEmote == "<:win:489151982918172723>":
                    wins = wins + 1

            total = wins + lossed
        embed.set_author(name=user.name, icon_url=user.avatar_url)

        embed.set_footer(text="WINS: "+str(wins)+"		LOSS: "+str(lossed)+"		TOTAL DUELS: "+str(total))
        if message_to_send == "":
            message_to_send = "Nothing"

        embed.add_field(name="All Streaks", value=message_to_send)

        await ctx.message.channel.send(embed=embed)

bot.run(TOKEN)