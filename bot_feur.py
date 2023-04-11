import os, discord, random
from blagues_api import BlaguesAPI, BlagueType
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
blagues = BlaguesAPI(os.getenv('BLAGUES_API_TOKEN'))

possible_quoi = ['quoi', 'quoi ?', 'quoi?', 'quoient', 'quoient ?', 'quoient?', 'Quoi', 'Quoi ?', 'Quoi?', 'Quoient', 'Quoient ?', 'Quoient?']
answers_quoi = ['feur','feuse','fure','drilatère','driceps','chi']

possible_qui = ['qui', 'qui ?', 'qui?', 'ki', 'ki ?', 'ki?', 'Qui', 'Qui ?', 'Qui?', 'Ki', 'Ki ?', 'Ki?']

emojis = [" :rofl:"," :sunglasses:", " :fire:", " :joy:"]



@bot.command(name='blague_beauf')
async def blague_beauf(ctx):
   blague = await blagues.random_categorized(BlagueType.BEAUF)
   await ctx.send(blague.joke)
   await ctx.send(blague.answer + random.choice(emojis))

@bot.command(name='humour_noir')
async def humour_noir(ctx):
   blague = await blagues.random_categorized(BlagueType.LIMIT)
   await ctx.send(blague.joke)
   await ctx.send(blague.answer + random.choice(emojis))

@bot.event
async def on_message(message):
   if message.author == bot.user:
      return
   
   for i in possible_quoi:
      if message.content.endswith(i):
         await message.channel.send(random.choice(answers_quoi))
   
   for i in possible_qui:
      if message.content.endswith(i):
         await message.channel.send('quette')
   

   await bot.process_commands(message)
   
   
bot.run(os.getenv('DISCORD_TOKEN'))