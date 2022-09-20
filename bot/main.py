#bot.py

import os
import discord
from dotenv import load_dotenv
from gtts import gTTS
import asyncio


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = discord.Client()


async def load_blacklist(f: str = "test") -> list:
	with open(f) as bl:
		lis = []
		#return lis.append(bl.read.splitlines())
	return lis


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


@bot.command(name="dtts", pass_context=True,)
async def dtts(context):
	user = context.message.author
	out_channel = await user.voice.voice_channel.connect()

	txt = context.message.content
	conv = gTTS(text=txt, lang="en", slow=False)
	conv.save("conv.mp3")
	audio_out = out_channel.create_ffmep_player("conv.mp3")
	audio_out.start()
	while not audio_out.is_done():
		await asyncio.sleep(10)
	audio_out.stop()
	os.remove("conv.mp3")

bot.run(TOKEN)
