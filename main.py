import os
import discord
import discord.ext.commands as commands
from dotenv import load_dotenv
import sql_lib
load_dotenv()
TOKEN = os.getenv('TOKEN')
client = commands.Bot(command_prefix=('!a', "!a "))


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


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
client.run(TOKEN)
