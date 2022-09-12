#bot.py

import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = discord.Client(discord.Intents.default())


async def load_blacklist(f: str) -> list:
	with open(f) as bl:
		return bl.read.splitlines()


blacklist = await load_blacklist()


@bot.event
async def on_member_join(member):
	await member.create_dm()
	message = f"hi {member.name}, welcome to our server"
	await member.dm_channel.send(message)


@bot.event
async def on_message(message):
	if message.author is bot.user:
		return
	for x in blacklist:
		if x in message.content:
			hit = message
			message.author.create_dm()
			m = f"hi please refrain from using the word{hit} in the future"
			await message.author.dm_channel.send(m)

bot.run(TOKEN)