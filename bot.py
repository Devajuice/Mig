from ast import alias
from http import client
from tokenize import Token
import os
import discord
import random
from dotenv import load_dotenv

load_dotenv(dotenv_path= "D:\Coding\DiscordBot/Token.env")
os.path.abspath(os.path.dirname(__file__))



from discord.ext import commands

client = commands.Bot(command_prefix='>')
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(help_command=None)

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_member_join(member):
        channel = client.get_channel(66445656564456565)
        await channel.send(f'{member} has joined the server.')

@client.event
async def on_member_remove(member):
        channel = client.get_channel(66445656564456565)
        await channel.send(f'{member} has left the server.')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, question):
    responses = ['It is certain.',
                'It is decidedly so.',
                'Without a doubt.',
                'Yes - definitely.',
                'You may rely on it.',
                'As I see it, yes.',
                'Most likely.',
                'Outlook good.',
                'Yes.',
                'Signs point to yes.',
                'Reply hazy, try again.',
                'Ask again later.',]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


#create a coin flip command
@client.command(aliases=['flip'])
async def coin(ctx):
    responses = ['Heads',
                'Tails']
    await ctx.send(f'Flipping a coin... {random.choice(responses)}')

#create a clear command with permission if the user does not have the permission, it will not work
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command.")   

#create a mute command with permission if the user does not have the permission, print out You do not have permission
@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
        if not discord.utils.get(ctx.guild.roles, name="Muted"):
            mute_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(mute_role, send_messages=False)
        await member.add_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
        await ctx.send(f'{member} has been muted')
@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command.")

@client.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member, *, reason=None):
    await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
    await ctx.send(f'{member} has been unmuted')

@client.command()
async def info(ctx):
    embed = discord.Embed(title="Info", description="Here are the commands you can use: Prefix is >", color=0xeee657)
    embed.add_field(name="8ball", value="Ask the magic 8ball a question.", inline=False)
    embed.add_field(name="flip", value="Flip a coin.", inline=False)
    embed.add_field(name="clear", value="Clear a certain amount of messages.", inline=False)
    embed.add_field(name="ping", value="Ping the bot.", inline=False)
    embed.add_field(name="say", value="Make the bot say something.", inline=False)
    embed.add_field(name="mute", value="Get someone muted.", inline=False)
    embed.add_field(name="unmute", value="Unmute someone.", inline=False)

    await ctx.send(embed=embed)

# create a say command
@client.command()
async def say(ctx, *, content):
    await ctx.send(content)

#run the bot with the token
client.run(os.getenv('DISCORD_TOKEN'))

