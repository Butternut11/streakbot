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
totalpot = collections.defaultdict(list)


@bot.command()
@commands.has_role("Host")
async def b(ctx, member: discord.Member, bet: float):
    global totalpot
    payout = round(bet*1.8, 2)
    newpot = round(bet*2, 2)
    tmpstr = pots[ctx.author.id]
    formattedString = f'<@{member.id}>'
    count = 0
    betsExist = False
    for bets in tmpstr:
        if formattedString in bets:
            betsExist = True
            newpayout = float(pots[ctx.author.id][count].split()[4]) + float(payout)
            newbet = float(pots[ctx.author.id][count].split()[2]) + float(bet)
            pots[ctx.author.id][count] = f'<@{member.id}> **Bet**: {newbet} **Payout**: {newpayout}'
        count += 1
    if not betsExist:
        pots[ctx.author.id].append(f'<@{member.id}> **Bet**: {bet} **Payout**: {payout}')
    totalpot[ctx.author.id].append(f'{newpot}')
    await ctx.send(embed=discord.Embed(
        title='Confirmation',
        description='```Added to the pot```'
    ))


@bot.command(name="potreset")
@commands.has_role("Host")
async def potreset(ctx):
    global totalpot
    user = ctx.author.id
    totalpot.pop(user, None)
    pots.pop(user, None)
    await ctx.send(embed=discord.Embed(
        title='Pot Reset',
        description='Pot has been reset'
    ))


@bot.command(name="pot")
async def pot(ctx, member: discord.Member = None):
    userpot = 0.0
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
    for numbers in totalpot[user]:
        userpot += float(numbers)
    await ctx.send(embed=discord.Embed(
        title='Pot',
        description=(f'{msg} \n ```Total pot: {userpot}```')
    ))


@bot.command(name="win")
@commands.has_role("Host")
async def win(ctx):
    
    if str(ctx.message.author.id) in streaks:
    
        streaks[str(ctx.message.author.id)].insert(0, "<:win:489151982918172723>")
    else:
        streaks[str(ctx.message.author.id)] = []
        streaks[str(ctx.message.author.id)].append("<:win:489151982918172723>")

    userpot = 0.0
    user = ctx.message.author.id
    msg = ""
    global totalpot

    if user in pots:
        for bets in pots[user]:
            msg += bets + "\n"
    else:
        msg = "User has no pot"

    if msg == "":
        msg = "User has no pot"
    for numbers in totalpot[user]:
        userpot += float(numbers)
    await ctx.send(embed=discord.Embed(
        title='Pot',
        description=f'{msg} \n ```Total pot: {userpot}```'
    ))

    pots.pop(user, None)
    totalpot.pop(user, None)

    user = ctx.message.author
    embed = discord.Embed()
    wins = 0
    lossed = 0
    total = "0"
    messageToSend = ""
    if str(user.id) in streaks:
        for streakEmote in streaks[str(user.id)]:
            if not messageToSend == "":
                messageToSend = messageToSend +","+ streakEmote
            else:
                messageToSend = streakEmote
            if streakEmote == "<:loss:489151983018704896>":
                lossed = lossed +1
            elif streakEmote == "<:win:489151982918172723>":
                wins = wins +1
        
            
        total = wins + lossed
    embed.set_author(name=user.name, icon_url=user.avatar_url)
        
    embed.set_footer(text="WINS: "+str(wins)+"		LOSS: "+str(lossed)+"		TOTAL DUELS: "+str(total))
    if messageToSend == "":
        messageToSend = "Nothing"
        
    embed.add_field(name="All Streaks", value=messageToSend)
        
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
    userpot = 0.0
    global totalpot

    if user in pots:
        for bets in pots[user]:
            msg += bets + "\n"
    else:
        msg = "User has no pot"

    if msg == "":
        msg = "User has no pot"
    for numbers in totalpot[user]:
        userpot += float(numbers)
    await ctx.send(embed=discord.Embed(
        title='Pot',
        description=(f'{msg} \n ```Total pot: {userpot}```')
    ))

    pots.pop(user, None)
    totalpot.pop(user, None)

    user = ctx.message.author
    embed = discord.Embed()
    wins = 0
    lossed = 0
    total = "0"
    messageToSend = ""
    if str(user.id) in streaks:
        for streakEmote in streaks[str(user.id)]:
            if not messageToSend == "":
                messageToSend = messageToSend +","+ streakEmote
            else:
                messageToSend = streakEmote
            if streakEmote == "<:loss:489151983018704896>":
                lossed = lossed +1
            elif streakEmote == "<:win:489151982918172723>":
                wins = wins +1
        
            
        total = wins + lossed
    embed.set_author(name=user.name, icon_url=user.avatar_url)
        
    embed.set_footer(text="WINS: "+str(wins)+"		LOSS: "+str(lossed)+"		TOTAL DUELS: "+str(total))
    if messageToSend == "":
        messageToSend = "Nothing"
        
    embed.add_field(name="All Streaks", value=messageToSend)
        
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
    messageToSend = ""
    if str(user.id) in streaks:
        for streakEmote in streaks[str(user.id)]:
            if not messageToSend == "":
                messageToSend = messageToSend +","+ streakEmote
            else:
                messageToSend = streakEmote
            if streakEmote == "<:loss:489151983018704896>":
                lossed = lossed +1
            elif streakEmote == "<:win:489151982918172723>":
                wins = wins +1
        
            
        total = wins + lossed
    embed.set_author(name=user.name, icon_url=user.avatar_url)
        
    embed.set_footer(text="WINS: "+str(wins)+"		LOSS: "+str(lossed)+"		TOTAL DUELS: "+str(total))
    if messageToSend == "":
        messageToSend = "Nothing"
        
    embed.add_field(name="All Streaks", value=messageToSend)
        
    await ctx.message.channel.send(embed=embed)
    

@bot.command(name="streakreset")
@commands.has_role("Host")
async def streakreset(ctx):
    
    streaks[str(ctx.message.author.id)] = []
    totalpot[ctx.message.author.id] = ""

async def is_zach(ctx):
    return ctx.author.id == 209081432956600320

@bot.command(name="zach")
@commands.check(is_zach)
async def zach(ctx):
    await ctx.send("Zach is the best cashier in StakeLand")

@bot.command(name="fuckbarry")
async def fuckbarry(ctx):
    await ctx.send("Barry has a small peepee")

@bot.command(name="slowbarry")
@commands.has_role("Super Nerdy")
async def slowbarry(ctx):
    await ctx.send("```Deep Breaths Barry, Slow down```")

@bot.command(name="stop")
@commands.has_role("Super Nerdy")
async def stop(ctx):
    await ctx.send("```I think it would be a good idea for you to stop now. ```")

@bot.command(name="streak")
async def streak(ctx, member : discord.Member = None):
    user = None
    
    if member is None: 
        user = ctx.message.author
    else:
        user = member
    
    if not user is None:
        validHost = False
        roles = user.roles
        for role in roles:
            if str(role) == "Host":
                validHost = True
        
        if validHost:
            embed = discord.Embed()
            wins = 0
            lossed = 0
            total = "0"
            messageToSend = ""
            if str(user.id) in streaks:
                for streakEmote in streaks[str(user.id)]:
                    if not messageToSend == "":
                        messageToSend = messageToSend +","+ streakEmote
                    else:
                        messageToSend = streakEmote
                    if streakEmote == "<:loss:489151983018704896>":
                        lossed = lossed +1
                    elif streakEmote == "<:win:489151982918172723>":
                        wins = wins +1
                
                    
                total = wins + lossed
            embed.set_author(name=user.name, icon_url=user.avatar_url)
                
            embed.set_footer(text="WINS: "+str(wins)+"		LOSS: "+str(lossed)+"		TOTAL DUELS: "+str(total))
            if messageToSend == "":
                messageToSend = "Nothing"
                
            embed.add_field(name="All Streaks", value=messageToSend)
                
            await ctx.message.channel.send(embed=embed)

# bot.run('NDc5MDkwODg1OTk3NjI1MzY0.Dn67Fg.iRWIgTNP7f1mF0zu5uLHnVrpPwc')
# bot.run('NDg5MzczODU1OTQxNTI1NTA1.Dnp0eA.3IBn8bvOZJ5ZJu2O2EAGAQJRXb0')
bot.run(TOKEN)