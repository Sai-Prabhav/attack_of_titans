import os
import discord
import discord.ext.commands as commands
from dotenv import load_dotenv
import sql_lib
load_dotenv()
TOKEN = os.getenv('TOKEN')
client = commands.Bot(command_prefix=('!a',"!a "))


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    

@client.command()
async def ping(ctx):
    await ctx.send(f"the ping is " + str(round(client.latency * 1000)) + "ms")

client.run(TOKEN)