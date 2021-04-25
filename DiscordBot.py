# imports
import asyncio
import discord
from discord.ext import commands, tasks
import youtube_dl
import os
import requests
from random import choice
import logging
import asyncio
import re
import time as timeModule
import random
from datetime import datetime
from pprint import pprint
import datetime
import json


client = commands.Bot(command_prefix=".")

# verifys the bot is online
@client.event
async def on_ready():
    print("The bot is online! (Echo.)")
    activity = discord.Game(name=".cmds", type=3)
    await client.change_presence(status=discord.Status.online, activity=activity)

# !clear command
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit = amount)


# unban script
@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
            return

# Kick script
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

# Ban script
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)

# .cmds script
@client.command()
async def cmds(ctx):
    embed = discord.Embed(title="Commands", description="Commands for the bot.", color=16719615)
    embed.add_field(name=".weather [city name]", value="Tells basic info about the city you asked about.")
    embed.add_field(name=".cmds", value="Displays full list of commands.")
    await ctx.send(embed=embed)

# .cmds mod view
@client.command()
@commands.has_permissions(manage_messages=True)
async def cmdsMod(ctx):
    embed = discord.Embed(title="Commands for mods", description="Advanced commands for mod's.", color=16719615)
    embed.add_field(name=".kick @person you want to kick", value="Kicks a member.")
    embed.add_field(name=".mute @person you want to mute", value="mutes a user.")
    embed.add_field(name=".unmute @person you want to umnute", value="Unmutes a user.")
    embed.add_field(name=".poll [question in the poll]", value="Starts a poll.")
    embed.add_field(name=".clear [message amount +1]", value="Clears messages.")
    embed.add_field(name=".cmdsAdmin", value="Advanced cmds for Admins")
    await ctx.send(embed=embed)

# !weather script
@client.command()
async def weather(ctx, *, city: str):
    api_key = "6d771618d6519fe680b9be90f6669391"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = city
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    channel = ctx.message.channel
    if x["cod"] != "404":
        async with channel.typing():
            y = x["main"]
            current_temperature = y["temp"]
            current_temperature_celsiuis = str(round(current_temperature - 273.15))
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            embed = discord.Embed(title=f"Weather in {city_name}", color=16719615, timestamp=ctx.message.created_at)
            embed.add_field(name="Descripition", value=f"**{weather_description}**", inline=False)
            embed.add_field(name="Temperature(C)", value=f"**{current_temperature_celsiuis}°C**", inline=False)
            embed.add_field(name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)
            embed.add_field(name="Atmospheric Pressure(hPa)", value=f"**{current_pressure}hPa**", inline=False)
            embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await channel.send(embed=embed)
    else:
        await channel.send('City you entered does not exist')

# Mute script
@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)
    embed = discord.Embed(title="muted", description=f"{member.mention} was muted ", colour=discord.Colour.red())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" you have been muted from: {guild.name} reason: {reason}")

# Unmute script
@client.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   await member.send(f" you have unmuted from: - {ctx.guild.name}")
   embed = discord.Embed(title="unmute", description=f" unmuted-{member.mention}",colour=discord.Colour.green())
   await ctx.send(embed=embed)

@commands.Cog.listener()
async def on_member_join(self, member):
    ment = member.mention
    await self.client.get_channel(834460714172940362).send(f"{ment} has joined the server.")
    print(f"{member} has joined the server.")

# poll script(needs and upgrade but works)
@client.command()
@commands.has_permissions(manage_messages=True)
async def poll(ctx,*,message):
    emb=discord.Embed(title=" POLL", description=f"{message}")
    msg=await ctx.channel.send(embed=emb)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')

# lockdown script
@client.command()
@commands.has_permissions(ban_members=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send( ctx.channel.mention + " ***is now in lockdown.***")

@client.command()
@commands.has_permissions(ban_members=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(ctx.channel.mention + " ***has been unlocked.***")

# .cmds Admin view
@client.command()
@commands.has_permissions(ban_members=True)
async def cmdsAdmin(ctx):
    embed = discord.Embed(title="Commands for Admins", description="Advanced commands for Admins.", color=16719615) #,color=Hex code
    embed.add_field(name=".ban @user you want to ban", value=" bans a user.")
    embed.add_field(name=".unban @user you want to ban", value=" Unbans a user.")
    embed.add_field(name=".lockdown", value="Locks a channel")
    embed.add_field(name=".unlock", value="unlocks the channel")
    await ctx.send(embed=embed)

# .suggest script
CHANNEL_ID = 834476925573398588

invite_link = 'https://discord.com/api/oauth2/authorize?client_id=814150166155231283&permissions=8&scope=bot'

@client.command()
async def suggest(ctx, command, *, description):
    ': Suggest a command. Provide the command name and description'
    embed = discord.Embed(title='Command Suggestion', description=f'Suggested by: {ctx.author.mention}\nCommand Name: *{command}*', color=discord.Color.green())
    embed.add_field(name='Description', value=description)
    channel = ctx.guild.get_channel(CHANNEL_ID)
    msg = await channel.send(embed=embed)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')
# DM people
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def pm(ctx, user: discord.User):
    await user.send('Hello, this is the bot Echo., im here to inform you that you have not migrated to the new Domediteisens Discord server. Join this server https://discord.gg/awMDGkUgKN. Thank you.')
    print("DM command executed")

client.run('ODE0MTUwMTY2MTU1MjMxMjgz.YDZqbQ.89k2DkLnja-K7HpcDla5JGD3NiY')