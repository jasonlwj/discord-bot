#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import json
import requests

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

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

	if guild_emojis:
		response = str(random.choice(guild_emojis))
	else:
		response = ':thinking:'
		
	await ctx.send(response)

@bot.command(name='roll', help='Simulates a random number generator')
async def roll(ctx, *args: int):
	if len(args) == 0:
		roll_min, roll_max = 1, 100
	elif len(args) == 1:
		roll_min, roll_max = 1, args[0]
	elif len(args) == 2:
		roll_min, roll_max = args[0], args[1]
	else:
		raise commands.TooManyArguments

	response = str(random.randint(roll_min, roll_max))
	await ctx.send(response)

@roll.error
async def roll_error(ctx, error):
	if isinstance(error, commands.UserInputError):
		await ctx.send(
			'```'
			'Usage:\n'
			'- !roll\n'
			'- !roll [max]\n'
			'- !roll [min] [max]\n'
			'```'
		)

@bot.command(name='emote', help='Send an emote from the FFZ public library')
async def emote(ctx, name):
	api_url = 'https://api.frankerfacez.com/v1/emoticons'
	headers = {'Content-Type': 'application/json'}
	params = {'q': name, 'sort': 'count-desc', 'high_dpi': 'on', 'page': 1, 'per_page': 20}

	response = requests.get(api_url, params=params, headers=headers)

	if response.status_code == 200:
		if response.json()['_total'] > 0:
			emote = response.json()['emoticons'][0]
			emote_url = (emote['urls'].get('4', False) or emote['urls'].get('2', False) or emote['urls'].get('1', False))
			await ctx.send('https:' + emote_url)
	
	# TODO: Add exception handling
		
@bot.command(name='say')
async def say(ctx):
	pass

bot.run(TOKEN)
