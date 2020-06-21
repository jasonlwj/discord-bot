#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random

from dotenv import load_dotenv
from discord.ext.commands import Bot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = Bot(command_prefix='!')

@bot.event
async def on_ready():
	connected_guilds = '\n - '.join([f'{g.name} ({len(g.members)} members)' for g in bot.guilds])
	print(
		f'{bot.user.name} has connected to Discord!\n'
		f'{bot.user.name} is currently connected to the following servers: \n - {connected_guilds}'
	)

@bot.command(name='react', help='Sends a reaction emoji to the channel')
async def react_message(ctx):
	guild_emojis = ctx.guild.emojis
	response = str(random.choice(guild_emojis))
	await ctx.send(response)

@bot.command(name='roll', help='Simulates a random number generator')
async def roll(ctx, *args: int):
	if len(args) == 0:
		response = str(random.randint(1, 100))
	elif len(args) == 1:
		response = str(random.randint(1, args[0]))
	elif len(args) == 2:
		response = str(random.randint(args[0], args[1]))
	else:
		response = 'Invalid number of arguments'

	await ctx.send(response)

	# TODO: add exception handling

@bot.command(name='say')
async def say(ctx):
	pass

bot.run(TOKEN)
