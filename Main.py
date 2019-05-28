import discord
from discord.ext import commands
import asyncio
import requests, bs4
import os
import time
import youtube_dl
import inspect
import datetime
from discord import opus

start_time = time.time()

bot = commands.Bot(command_prefix=("x"))

players = {}

@bot.event
async def on_ready():
  print("Logged in as")
  print("bot user Name:", bot.user.name)
  print("bot user ID:", bot.user.id)

@bot.command(name="join", pass_context=True, no_pm=True)
async def _join(ctx):
    user = ctx.message.author
    channel = ctx.message.author.voice.voice_channel
    await bot.join_voice_channel(channel)
    embed = discord.Embed(colour=user.colour)
    embed.add_field(name="Successfully connected to voice channel:", value=channel)
    await bot.say(embed=embed)

@bot.command(name="leave", pass_context=True, no_pm=True)
async def _leave(ctx):
    user = ctx.message.author
    server = ctx.message.server
    channel = ctx.message.author.voice.voice_channel
    voice_client = bot.voice_client_in(server)
    await voice_client.disconnect()
    embed = discord.Embed(colour=user.colour)
    embed.add_field(name="Successfully disconnected from:", value=channel)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def pause(ctx):
    user = ctx.message.author
    id = ctx.message.server.id
    players[id].pause()
    embed = discord.Embed(colour=user.colour)
    embed.add_field(name="Player Paused", value=f"Requested by {ctx.message.author.name}")
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def skip(ctx):
    user = ctx.message.author
    id = ctx.message.server.id
    players[id].stop()
    embed = discord.Embed(colour=user.colour)
    embed.add_field(name="Player Skipped", value=f"Requested by {ctx.message.author.name}")
    await bot.say(embed=embed)

@bot.command(name="play", pass_context=True)
async def _play(ctx, *, name):
	author = ctx.message.author
	name = ctx.message.content.replace("xplay ", '')
	fullcontent = ('http://www.youtube.com/results?search_query=' + name)
	text = requests.get(fullcontent).text
	soup = bs4.BeautifulSoup(text, 'html.parser')
	img = soup.find_all('img')
	div = [ d for d in soup.find_all('div') if d.has_attr('class') and 'yt-lockup-dismissable' in d['class']]
	a = [ x for x in div[0].find_all('a') if x.has_attr('title') ]
	title = (a[0]['title'])
	a0 = [ x for x in div[0].find_all('a') if x.has_attr('title') ][0]
	url = ('http://www.youtube.com'+a0['href'])
	server = ctx.message.server
	voice_client = bot.voice_client_in(server)
	player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
	players[server.id] = player
	print("User: {} From Server: {} is playing {}".format(author, server, title))
	player.start()
	embed = discord.Embed(description=" ")
	embed.add_field(name="Now Playing", value=title)
	await bot.say(embed=embed)

@bot.command(pass_context=True)
async def queue(ctx, *, name):
	name = ctx.message.content.replace("xqueue ", '')
	fullcontent = ('http://www.youtube.com/results?search_query=' + name)
	text = requests.get(fullcontent).text
	soup = bs4.BeautifulSoup(text, 'html.parser')
	img = soup.find_all('img')
	div = [ d for d in soup.find_all('div') if d.has_attr('class') and 'yt-lockup-dismissable' in d['class']]
	a = [ x for x in div[0].find_all('a') if x.has_attr('title') ]
	title = (a[0]['title'])
	a0 = [ x for x in div[0].find_all('a') if x.has_attr('title') ][0]
	url = ('http://www.youtube.com'+a0['href'])
	server = ctx.message.server
	voice_client = bot.voice_client_in(server)
	player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

	if server.id in queues:
		queues[server.id].append(player)
	else:
		queues[server.id] = [player]
	embed = discord.Embed(description=" ")
	embed.add_field(name="Video queued", value=title)
	await bot.say(embed=embed)
  
def user_is_me(ctx):
	return ctx.message.author.id == "277983178914922497"

@bot.command(name='eval', pass_context=True)
@commands.check(user_is_me)
async def _eval(ctx, *, command):
    res = eval(command)
    if inspect.isawaitable(res):
        await bot.say(await res)
    else:
    	await bot.delete_message(ctx.message)
    	await bot.say(res)
        
@_eval.error
async def eval_error(error, ctx):
	if isinstance(error, discord.ext.commands.errors.CheckFailure):
		text = "Sorry {}, You can't use this command only the bot owner can do this.".format(ctx.message.author.mention)
		await bot.send_message(ctx.message.channel, text)
  
bot.run(os.environ['BOT_TOKEN'])
