import os
import discord
import discord.ext.commands as commands
from dotenv import load_dotenv
import sql_lib
from random import randint
load_dotenv()
TOKEN = os.getenv('TOKEN')
client = commands.Bot(command_prefix=('!a', "!a "))


async def monster(ctx):

    result = sql_lib.monster_battle(ctx.message.author)
    if len(result) == 3:
        await ctx.send(f'you encountered {result[0].name} of level {result[0].level} and won the battle you earned {result[1]} xp and {result[2]} money')
    else:
        await ctx.send(f'you encountered {result[0].name} of level {result[0].level} and lost the battle better luck next time')


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("That command does not exist.")
    if isinstance(error, commands.errors.CommandOnCooldown):
        await ctx.send(f"That command is on cooldown,please try again after {round(error.retry_after*100)/100} seconds.")


@client.command()
async def ping(ctx):
    await ctx.send(f"the ping is " + str(round(client.latency * 1000)) + "ms")


@client.command()
async def profile(ctx):
    user = sql_lib.user(ctx.message.author)
    x = str(user)
    await ctx.send(str(user))


@client.command()
async def join(ctx):
    if not sql_lib.isUser(ctx.message.author.id):
        sql_lib.join(ctx.message.author)
        await ctx.send(f"<@{ctx.message.author.id}> has joined the game")
    else:
        await ctx.send("you are already a member")


@client.command()
async def inv(ctx):
    inventory = sql_lib.get_inventory(ctx.message.author.id)

    ans = ""
    for item, qnt in inventory.items():
        ans += (f"{sql_lib.item(item).name[-1]} : {str(qnt)}\n")
    await ctx.send(ans)


@client.command()
async def pay(ctx, to: discord.Member, amount: int):
    if not(sql_lib.isUser(ctx.message.author.id) and sql_lib.isUser(to.id)):
        await ctx.send("One or both of you are not registered")
        return

    if ctx.message.author.id == to.id:
        await ctx.send("you can't pay yourself")
        return
    if amount <= 0 or amount > sql_lib.get_money(ctx.message.author.id):
        await ctx.send("you can only pay what you have")
        return
    sql_lib.set_money(ctx.message.author.id, sql_lib.get_money(
        ctx.message.author.id)-amount)
    sql_lib.set_money(to.id, sql_lib.get_money(to.id)+amount)
    await ctx.send(f"you have paid <@{to.id}> {amount}")


@client.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def fish(ctx):
    if not sql_lib.isUser(ctx.message.author.id):
        await ctx.send("you are not registered you can register with `!ajoin`")
        return
    if randint(0, 10) < 7:
        inv_dict = sql_lib.get_inventory(ctx.message.author.id)

        num_fish = round(randint(1*(sql_lib.get_strength(ctx.message.author.id)/10),
                                 4*(sql_lib.get_strength(ctx.message.author.id)/10)))
        if inv_dict.get(4):
            inv_dict[4] += num_fish
        else:
            inv_dict[4] = num_fish
        sql_lib.set_inventory(ctx.message.author.id, inv_dict)
        await ctx.send(f"you caught {num_fish} fish")
    if randint(0, 10) > 7:
        await monster(ctx)


@client.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def mine(ctx):
    if not sql_lib.isUser(ctx.message.author.id):
        await ctx.send("you are not registered you can register with `!ajoin`")
        return
    if randint(0, 10) < 7:
        inv_dict = sql_lib.get_inventory(ctx.message.author.id)
        num_stone = round(randint(2*(sql_lib.get_strength(ctx.message.author.id)/10),
                                  5*(sql_lib.get_strength(ctx.message.author.id)/10)))
        if inv_dict.get(2):
            inv_dict[2] += num_stone
        else:
            inv_dict[2] = num_stone
        sql_lib.set_inventory(ctx.message.author.id, inv_dict)
        await ctx.send(f"you mined {num_stone} ore")
    if randint(0, 10) > 7:
        await monster(ctx)


@client.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def chop(ctx):
    if not sql_lib.isUser(ctx.message.author.id):
        await ctx.send("you are not registered you can register with `!ajoin`")
        return
    if randint(0, 10) < 7:
        inv_dict = sql_lib.get_inventory(ctx.message.author.id)
        num_wood = round(randint(2.5*(sql_lib.get_strength(ctx.message.author.id)/10),
                                 7.5*(sql_lib.get_strength(ctx.message.author.id)/10)))
        if inv_dict.get(0):
            inv_dict[0] += num_wood
        else:
            inv_dict[0] = num_wood
        sql_lib.set_inventory(ctx.message.author.id, inv_dict)
        await ctx.send(f"you chopped {num_wood} wood")
    if randint(0, 10) > 7:
        await monster(ctx)

@client.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def hunt(ctx):
    await monster(ctx)

@client.command()   
async def levelup(ctx):
    if not sql_lib.isUser(ctx.message.author.id):
        await ctx.send("you are not registered you can register with `!ajoin`")
        return
    level=sql_lib.get_level(ctx.message.author.id)
    xp=sql_lib.get_xp(ctx.message.author.id)
    if xp>=(required_xp:=1.5**level*100):
        sql_lib.set_xp(ctx.message.author.id,xp-required_xp)
        sql_lib.set_level(ctx.message.author.id,level+1)
        await ctx.send(f"you have leveled up to level {level+1}")
    else:
        await ctx.send(f"you need {required_xp-xp} more xp to level up")

client.run(TOKEN)
