import os, discord, random
from blagues_api import BlaguesAPI, BlagueType
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
blagues = BlaguesAPI(os.getenv('BLAGUES_API_TOKEN'))

@bot.command(name='blague_beauf')
async def blague_beauf(ctx):
   blague = await blagues.random_categorized(BlagueType.BEAUF)
   await ctx.send(blague.joke)
   await ctx.send(blague.answer + " :rofl:")

@bot.event
async def on_message(message):
   if message.author == bot.user:
      return

   if message.content.endswith('quoi') or message.content.endswith('quoi ?') or message.content.endswith('quoient') or message.content.endswith('quoient ?') or message.content.endswith('quoi?'):
      answers=['feur','feuse','fure','drilatère','driceps']
      await message.channel.send(random.choice(answers))

   if message.content.endswith('qui') or message.content.endswith('qui ?') or message.content.endswith('qui?') or message.content.endswith('ki') or message.content.endswith('ki ?') or message.content.endswith('ki?'):
      await message.channel.send('quette')

   await bot.process_commands(message)
   
   
bot.run(os.getenv('DISCORD_TOKEN'))