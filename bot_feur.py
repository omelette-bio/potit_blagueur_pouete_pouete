import os, discord, random, argparse
from blagues_api import BlaguesAPI, BlagueType
from discord.ext import commands
from dotenv import load_dotenv

# récupère le mode de lancement du bot
parser = argparse.ArgumentParser()
parser.add_argument('mode', type=int, help='Mode de lancement du bot, 1: dev, 2: public')
args = parser.parse_args()


# charge les variables d'environnement
load_dotenv()

# initialise le bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

# initialise l'API de blagues
blagues = BlaguesAPI(os.getenv('BLAGUES_API_TOKEN'))

# initialise les variables du bot qui vont lui permettre de répondre à certains messages
# on ira chercher les réponses dans une liste, pour pouvoir facilement en ajouter ou en supprimer
possible_quoi = ['quoi', 'quoi ?', 'quoi?', 'quoient', 'quoient ?', 'quoient?', 'Quoi', 'Quoi ?', 'Quoi?', 'Quoient', 'Quoient ?', 'Quoient?']
answers_quoi = ['feur','feuse','fure','drilatère','driceps','chi']

possible_qui = ['qui', 'qui ?', 'qui?', 'ki', 'ki ?', 'ki?', 'Qui', 'Qui ?', 'Qui?', 'Ki', 'Ki ?', 'Ki?']
emojis = [" :rofl:"," :sunglasses:", " :fire:", " :joy:"]
cmds = {"/blague_beauf": "renvoie une blague beauf", "/humour_noir": "renvoie une blague humour noir", "/help": "renvoie la liste des commandes"}


# display a message when the bot is ready and indicate the mode of the bot
@bot.event
async def on_ready():
   if args.mode == 1:
      print(f'{bot.user.name} has connected to Discord in dev mode !')
   else:
      print(f'{bot.user.name} has connected to Discord in public mode !')


# commande qui affiche une blague beauf
@bot.command(name='blague_beauf')
async def blague_beauf(ctx):
   # si le dev mode est activé et que l'utilisateur n'a pas le role "dev", le bot ne répond pas
   if 'dev' not in [role.name.lower() for role in ctx.author.roles] and args.mode == 1:
      await ctx.send("le bot est en dev mode sorry :(")
   # sinon, le bot répond
   else:
      blague = await blagues.random_categorized(BlagueType.BEAUF)
      await ctx.send(blague.joke)
      await ctx.send(blague.answer + random.choice(emojis))


# commande qui affiche une blague humour noir
@bot.command(name='humour_noir')
async def humour_noir(ctx):
   # si le dev mode est activé et que l'utilisateur n'a pas le role "dev", le bot ne répond pas
   if 'dev' not in [role.name.lower() for role in ctx.author.roles] and args.mode == 1:
      await ctx.send("le bot est en dev mode sorry :(")
   # sinon, le bot répond
   else:
      blague = await blagues.random_categorized(BlagueType.LIMIT)
      await ctx.send(blague.joke)
      await ctx.send(blague.answer + random.choice(emojis))


# commande qui affiche la liste des commandes
@bot.command(name='help')
async def help(ctx):
   # si le dev mode est activé et que l'utilisateur n'a pas le role "dev", le bot ne répond pas
   if 'dev' not in [role.name.lower() for role in ctx.author.roles] and args.mode == 1:
      await ctx.send("le bot est en dev mode sorry :smiling_face_with_tear: ")
   # sinon, le bot répond
   else:
      # construit la liste des commandes avec leur description grâce à la variable cmds
      msg = "```bonjour, je suis un potit blagueur, voici la liste des commandes que je connais :\n"
      for cmd in cmds:
         msg += cmd + " : " + cmds[cmd] + "\n"
      msg += "je connais aussi d'autres choses mais je ne vais rien dévoiler ;)```"
      await ctx.send(msg)


# partie qui permet au bot de répondre à certains messages
@bot.event
async def on_message(message):
   # n'envoie pas de message si le message est envoyé par le bot (évite les boucles infinies)
   if message.author == bot.user:
         return
   
   # regarde si le message fini par un des mots de la liste possible_quoi
   for i in possible_quoi:
      if message.content.endswith(i):
         # si le dev mode est activé et que l'utilisateur n'a pas le role "dev", le bot ne répond pas
         if 'dev' not in [role.name.lower() for role in message.author.roles] and args.mode == 1:
            return
         # sinon, le bot répond
         await message.channel.send(random.choice(answers_quoi))
   
   # regarde si le message fini par un des mots de la liste possible_qui
   for i in possible_qui:
      if message.content.endswith(i):
         # si le dev mode est activé et que l'utilisateur n'a pas le role "dev", le bot ne répond pas
         if 'dev' not in [role.name.lower() for role in message.author.roles] and args.mode == 1:
            return
         # sinon, le bot répond
         await message.channel.send('quette')

   # regarde si le message est une commande
   await bot.process_commands(message)

# lance le bot
bot.run(os.getenv('DISCORD_TOKEN'))