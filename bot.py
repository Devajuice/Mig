from ast import alias
from distutils import command
from http import client
from tokenize import Token
import os
import discord
import random
import aiohttp 
import asyncio
import datetime
import time
from dotenv import load_dotenv
import pyjokes

load_dotenv('Token.env')
TOKEN = os.getenv('DISCORD_TOKEN')


from discord.ext import commands

client = commands.Bot(command_prefix='>', help_command=None)
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(help_command=None)

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=">help | golo.tk"))
    print('Bot is ready!')

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

@client.command(aliases=['flip'])
async def coin(ctx):
    responses = ['Heads',
                'Tails']
    await ctx.send(f'Flipping a coin... {random.choice(responses)}')

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command.")   

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
@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command.")

@client.command()
async def say(ctx, *, content):
    await ctx.send(content)

@client.command()
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, *, nickname):
    await member.edit(nick=nickname)
    await ctx.send(f'{member} has been nicknamed')
@nick.error
async def nick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command.")

@client.command()
async def avatar(ctx, member: discord.Member):
    await ctx.send(f'{member.avatar_url}')

@client.command()
async def joke(ctx):
    await ctx.send(pyjokes.get_joke())

#create a command not found error message when the user sends a command that is not found in the bot 
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command not found. Please use >help for a list of commands.')

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member} has been kicked')
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command.")

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member} has been banned')
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command.")

@client.command()
async def whois(ctx, member: discord.Member):
    embed = discord.Embed(title=f'{member}', description=f'{member.id}', color=member.color)
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name='Highest Role', value=member.top_role)
    embed.add_field(name='Joined Server', value=member.joined_at)
    embed.add_field(name='Account Created', value=member.created_at)
    embed.add_field(name='Roles', value=' '.join([role.mention for role in member.roles if role != ctx.guild.default_role]))
    await ctx.send(embed=embed)

@client.command()
async def info(ctx):
    embed = discord.Embed(title='Bot Info', description='This is a bot made by @Bloop#7070', color=0x00ff00)
    embed.add_field(name='Bot Name', value='Mig')
    embed.add_field(name='Bot Creator', value='Bloop#7070')
    embed.add_field(name='Bot Invite', value='https://discord.com/api/oauth2/authorize?client_id=898457693415686144&permissions=8&scope=bot')
    embed.add_field(name='Bot Source Code', value='https://github.com/Realxxmonkey/Mig')
    embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/ZFsnZ5W1xalBiv9_GlzcQk-MQhptIxawsafxOKr9B8A/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/898457693415686144/44f65e0ab8d728ece08d74691e9a4564.webp")
    await ctx.send(embed=embed)
 
@client.command()
async def invite(ctx):
    await ctx.send('https://discord.com/api/oauth2/authorize?client_id=898457693415686144&permissions=8&scope=bot')

@client.command()
async def meme(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://meme-api.herokuapp.com/gimme/dankmemes') as r:
            meme = await r.json()
    embed = discord.Embed(title=meme['title'], url=meme['postLink'], color=0x00ff00)
    embed.set_image(url=meme['url'])
    await ctx.send(embed=embed)

@client.command()
async def kill(ctx, member: discord.Member):
    await ctx.send(f'{member} has been killed by {ctx.author}')

@client.command()
async def help(ctx):
    embed = discord.Embed(title="Help", description="Here are the commands you can use: Prefix is > for more information of commands visit https://realxxmonkey.github.io/Mig/", color=0xeee657)
    embed.add_field(name="Moderation", value="kick,mute,unmute,ban,clear,nick")
    embed.add_field(name="Fun", value="8ball,flip,say,joke,whois,avatar,meme, kill")
    embed.add_field(name="General", value="help,info,ping,invite")
    embed.set_footer(text="Made by: @Bloop#7070")
    embed.set_thumbnail(url="https://images-na.ssl-images-amazon.com/images/I/51oxgH9Kl-L.png")
    await ctx.send(embed=embed)


client.run(os.getenv('DISCORD_TOKEN'))

