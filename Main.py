import discord
from discord.ext import commands
import asyncio
import inspect
import requests, bs4
from itertools import cycle
import os
import time
import youtube_dl
from discord import opus

client = commands.Bot(command_prefix=("x"))
client.remove_command("help")

players = {}	

@client.event 
async def on_ready():
	print('Logged in as')
	print("User name:", client.user.name)
	print("User id:", client.user.id)
	print('---------------')

@client.event
async def on_message(message):
  if message.content.startswith('xplay '):
	if song = ("playing").print("Sorry, You can't do that right now, Please wait for the song to finish")
      author = message.author
      name = message.content.replace("xplay ", '')                 
      fullcontent = ('http://www.youtube.com/results?search_query=' + name)
      text = requests.get(fullcontent).text
      soup = bs4.BeautifulSoup(text, 'html.parser')
      img = soup.find_all('img')
      div = [ d for d in soup.find_all('div') if d.has_attr('class') and 'yt-lockup-dismissable' in d['class']]
      a = [ x for x in div[0].find_all('a') if x.has_attr('title') ]
      title = (a[0]['title'])
      a0 = [ x for x in div[0].find_all('a') if x.has_attr('title') ][0]
      url = ('http://www.youtube.com'+a0['href'])
      delmsg = await client.send_message(message.channel, 'Now Playing ** >> ' + title + '**')
      server = message.server
      voice_client = client.voice_client_in(server)
      player = await voice_client.create_ytdl_player(url)
      players[server.id] = player
      print("User: {} From Server: {} is playing {}".format(author, server, title))
      player.start()
  await client.process_commands(message)

def user_is_me(ctx):
	return ctx.message.author.id == "381562121865003009"

@client.command(pass_context=True, no_pm=True)
async def ping(ctx):
    pingtime = time.time()
    pingms = await client.say("Pinging...")
    ping = (time.time() - pingtime) * 1000
    await client.edit_message(pingms, "Pong! :ping_pong: ping time is `%dms`" % ping)
	
@client.command(name='eval', pass_context=True)
@commands.check(user_is_me)
async def _eval(ctx, *, command):
    res = eval(command)
    if inspect.isawaitable(res):
        await client.say(await res)
    else:
        await client.delete_message(ctx.message)
        await client.say(res)

@_eval.error
async def eval_error(error, ctx):
	if isinstance(error, discord.ext.commands.errors.CheckFailure):
		text = "Sorry {} You can't use this command only the bot owner can do this.".format(ctx.message.author.mention)
		await client.send_message(ctx.message.channel, text)
    
@client.command(pass_context=True, no_pm=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    await client.say('Connected to voice channel: **[' + str(channel) + ']**')

@client.command(pass_context=True, no_pm=True)
async def leave(ctx):
    server = ctx.message.server
    channel = ctx.message.author.voice.voice_channel
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()
    await client.say("Successfully disconnected from ***[{}]***".format(channel))

@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()
    await client.say("Player Paused")

@client.command(pass_context=True)
async def stop(ctx):
    author = ctx.message.author
    id = ctx.message.server.id
    players[id].stop()
    embed = discord.Embed(description=" ")
    embed.add_field(name="Player Stopped", value=f"Requested by {ctx.message.author.name}")
    await client.say(embed=embed)

@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()
    await client.say("player resumed")

@client.command(pass_context=True, no_pm=True)
async def help(ctx):
	embed = discord.Embed(title="Help section", description=" ", color=0xFFFF)
	embed.add_field(name="xjoin", value="make the bot join voice channel")
	embed.add_field(name="xleave", value="make the bot leave the voice channel")
	embed.add_field(name="xplay", value="please be careful when using this command it will break if theres music playing.")
	embed.add_field(name="xstop", value="to stop the music from playing")
	embed.add_field(name="xping", value="get bot's ping time")
	embed.add_filed(name="Comming Soon", value="New Loop Command & Queue Commands Comming Soon")
	await client.say(embed=embed)

client.run(os.environ['BOT_TOKEN'])
