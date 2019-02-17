import discord
from discord.ext import commands
import inspect
import os

@bot.event
async def on_ready():
  print("Logged in as")
  print("bot user Name:", bot.user.name)
  print("bot user ID:", bot.user.id)
  
bot.run(os.environ['BOT_TOKEN'])
