import discord
from discord.ext import commands
import inspect
import os
import asyncio
import requests, bs4
import youtube_dl
import datetime
from discord import opus

start_time = time.time()

@bot.event
async def on_ready():
  print("Logged in as")
  print("bot user Name:", bot.user.name)
  print("bot user ID:", bot.user.id)
  
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
