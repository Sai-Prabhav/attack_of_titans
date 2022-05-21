import os
import discord
import discord.ext.commands as commands
from dotenv import load_dotenv
import sql_lib
from random import randint
load_dotenv()
TOKEN = os.getenv('TOKEN')
client = commands.Bot(command_prefix=('!a', "!a "))


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
    print(inventory)
    ans = ""
    for item, qnt in inventory:
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


@client.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def fish(ctx):
    if not sql_lib.isUser(ctx.message.author.id):
        await ctx.send("you are not registered you can register with `!ajoin`")
        return
    if randint(0, 10) < 7:
        print("fished")
        inv = sql_lib.get_inventory(ctx.message.author.id)
        inv_dict = {}
        for i in inv:
            inv_dict[i[0]] = i[1]
        num_fish = round(randint(1*(sql_lib.get_strength(ctx.message.author.id)/10),
                                 4*(sql_lib.get_strength(ctx.message.author.id)/10)))
        if inv_dict.get(4):
            inv_dict[4] += num_fish
        else:
            inv_dict[4] = num_fish
        sql_lib.set_inventory(ctx.message.author.id, inv_dict)
        await ctx.send(f"you caught {num_fish} fish")
    if randint(0, 10) > 7:
        result = sql_lib.monster(ctx.message.author)
        if len(result)==3:
            await ctx.send(f'you encountered a level {result[0]} and won the battle you earned {result[1]} xp and {result[2]} money')


client.run(TOKEN)
