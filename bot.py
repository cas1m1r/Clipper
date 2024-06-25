from discord.ext import commands
from dotenv import load_dotenv
from discord.utils import get
from utils import *
import discord
import asyncio
import json
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')

intents = discord.Intents.default()
intents.message_content=True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
	guild = get(bot.guilds, name=GUILD)
	print(f'{bot.user} in online')



@bot.command(name='yt-format')
async def get_format(ctx, *arg):
	url = arg[-1]
	print(url)
	await ctx.send(f'Getting format options')
	forms = '\n'.join(get_formats(url))
	await ctx.send("```\n"+forms+"\n```")

@bot.command(name='yt-sample')
async def get_sample(ctx, *arg):
	url = arg[-1]
	# clean url to avoid extra stuff ?pp= etc.
	await ctx.send(f'Downloading and sampling. Just a second...')
	c1 = f'/usr/sbin/yt-dlp -f 251 {url} -o tmp.webm'
	c2 = f'ffmpeg -i tmp.webm sample.wav'
	if os.path.isfile('tmp.webm'):
		os.remove('tmp.webm')
	if os.path.isfile('sample.wav'):
		os.remove('sample.wav')
	try:
		os.system(c1)
		os.system(c2)
		# get file size, attachment limits.... 
		fstat = os.stat('sample.wav')
		fsize = fstat.st_size/1e6
		await ctx.send(f'Converted file is **{fsize} MB**')	
		with open('sample.wav','rb') as f:
			wav = discord.File(f)
			msg = f'Downloaded and converted to wav file:'
			await ctx.send(msg, file=wav)
		f.close()
	except:
		await ctx.send(f':cry: Something went wrong... Sorry about that')	
		pass
	
	
	
	os.remove('tmp.webm')
	os.remove('sample.wav')
		

@bot.command(name='yt-vid')
async def get_video(ctx, *arg):
	url = arg[-1]
	default = '614'
	if len(arg) > 1:
		format = arg[0]
	
	# TODO: clean urls?
	await ctx.send(f'Downloading video. Just a second...')
	c1 = f'/usr/sbin/yt-dlp -f {format} {url} -o clip.mp4'
	if os.path.isfile('tmp.webm'):
		os.remove('tmp.webm')
	if os.path.isfile('sample.wav'):
		os.remove('sample.wav')
	try:
		os.system(c1)
		# get file size, attachment limits.... 
		fstat = os.stat('clip.mp4')
		fsize = fstat.st_size/1e6
		await ctx.send(f'File is **{fsize} MB**')	
		with open('clip.mp4','rb') as f:
			wav = discord.File(f)
			msg = f'Downloaded mp4 file:'
			await ctx.send(msg, file=wav)
		f.close()
	except:
		await ctx.send(f':cry: Something went wrong... Sorry about that')	
		pass
	
	os.remove('clip.mp4')


@bot.command(name='ping')
async def ping(ctx):
	await ctx.send('AYOOOOO :wave:')


def main():
	bot.run(TOKEN)


if __name__ == '__main__':
	main()

