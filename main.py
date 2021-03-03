import discord
import os
import json
import requests
from keep_alive import keep_alive
from discord.ext import commands
import random
import matplotlib.pyplot as plt
import numpy as np
from time import sleep
import datetime
from replit import db
import re
from discord.utils import get

#configs
intents = discord.Intents.all()
prefix = os.getenv('PREFIX')
bot = commands.Bot(command_prefix=prefix, help_command=None, intents=intents)
owner = 575263293015588867




#functions
def verifyembed(arg):
  global embed
  embed = discord.Embed(title="", description=arg, color=0xe74c3c)
  embed.set_image(url="https://cdn.discordapp.com/attachments/815124760283185182/815284836113317958/4tCLSgYmgbLVEQCIgEegeAkETYv4q1vdw1BWiIgERjgCEgiHeAGIJsvEZAIdB8BSaTdx1CWIBGQCAxwBP4fkFAfPr0k2fsAAAAAS.png")
  return embed




#verification system commands
#--------------------
@bot.command()
async def verify(ctx,*,arg=None):
  if not arg:
    tok = f'Hello, {ctx.message.author.name}!\n**The correct way of doing this is:** \n`{prefix}verify "your name" "your breif introduction that can include your art style or any other information about you!"`'
    await ctx.send(embed = verifyembed(tok))
  else:
    check = arg.find('"')
    if check == -1:
      await ctx.send("See the format again!")
    else:  
      arg = re.split('"', arg)
      try:
        await ctx.send(f"Set Your details!\n**Name:** {arg[1]}\n**Personal Note:** {arg[3]}")
        db[ctx.message.author.id] = f"Name: {arg[1]} | Personal Note: {arg[3]}"
        
        role = get(ctx.guild.roles, name="Verified")
        role2 = get(ctx.guild.roles, id=815939799768367144)
        await ctx.author.add_roles(role)
        await ctx.author.add_roles(role2)
      except:
        await ctx.send("Something went wrong, try doing the command again with the proper format!")

@bot.event
async def on_member_join(member):
  channel = bot.get_channel(815207593169125406)
  general = bot.get_channel(815295318588522567)
  if member.id in db:
    await channel.send(f"{member} already has been verified before!\nAutomatically verified **{member}**.\n\nDetails: \n{db[member.id]}")
    await general.send(f"Hello, {member.mention}, you have been automatically verified because you had your information set up before. Thanks for rejoining!")
    role = get(member.guild.roles, name="Verified")
    role2 = get(member.guild.roles, id=815939799768367144)
    await member.add_roles(role)
    await member.add_roles(role2)
  elif(member.bot == True):
    role = get(member.guild.roles, id= 815436698846363668)
    await member.add_roles(role)
    await channel.send(f"{member} has entered, which is a bot. It has been given the **ServerBots** role.")
  else:
    await channel.send(member.mention,embed = verifyembed(f'Hello {member.name}!\n**Do the following to get verified:**\n`{prefix}verify "your name" "your breif introduction that can include your art style or any other information about you!"`'))

@bot.command()
async def info(ctx, arg=None):
  if not arg:
    await ctx.send(f"Hello, try doing `{prefix}info <user id>` to get information if the user is verified!")
  elif(arg == "f"):
    try:
      value = db[ctx.author.id]
      await ctx.send(value)
    except KeyError:
      await ctx.send("You have no info setup!")
  else:
    try:  
      value = db[arg]
      await ctx.send(value)
    except KeyError:
      await ctx.send("Couldnt find info with that user id.") 


@bot.command()
@commands.has_permissions(administrator=True)
async def deleteinfo(ctx, user:discord.Member=None):
  role = get(ctx.guild.roles, name="Verified")
  if user==None:
    await ctx.send(f"Delete user info and unverify them! `{prefix}deleteinfo <user id>`")
  else:
    id = user.id
    if id in db:
      del db[id]
      await ctx.send("Deleted user info from the database and unverified them!")
    else:
      await ctx.send("Cant find any info with that user id. Although the verified role will be removed if the user has it.")
    await user.remove_roles(role, reason="Unverifying")

#--------------------
#verification system commands




#commands
@bot.command()
async def echo(ctx,*,arg=None):
  if not arg:
    await ctx.send("Echo!")
  else:
    await ctx.send(f"The bot says: {arg}")

@bot.command()
async def varval(ctx, *, arg=None):
  if not arg:
    await ctx.send("No arguments given!")
  else:
    if(ctx.message.author.id == owner):
      await ctx.send(globals()[arg])
    else:
      await ctx.send("Owner only command!")

@bot.command()
async def ping(ctx):
  if round(bot.latency * 1000) <= 50:
        embed = discord.Embed(
            title="PING",
            description=
            f":ping_pong: Pong! The ping is **{round(bot.latency *1000)}** milliseconds!",
            color=0x44ff44)
  elif round(bot.latency * 1000) <= 100:
        embed = discord.Embed(
            title="PING",
            description=
            f":ping_pong: Pong! The ping is **{round(bot.latency *1000)}** milliseconds!",
            color=0xffd000)
  elif round(bot.latency * 1000) <= 200:
        embed = discord.Embed(
            title="PING",
            description=
            f":ping_pong: Pong! The ping is **{round(bot.latency *1000)}** milliseconds!",
            color=0xff6600)
  else:
        embed = discord.Embed(
            title="PING",
            description=
            f":ping_pong: Pong! The ping is **{round(bot.latency *1000)}** milliseconds!",
            color=0x990000)
  await ctx.send(embed=embed)

@bot.command()
async def say(ctx,*,arg):
  if(ctx.author.id == owner):
    embed = discord.Embed(title="", description=arg, color=0x3498db)
    embed.set_footer(text="#A&D")
    await ctx.send(embed=embed)
keep_alive()
bot.run(os.getenv('TOKEN'))