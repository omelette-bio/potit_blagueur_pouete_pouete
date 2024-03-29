import os, discord, random, argparse, json
from blagues_api import BlaguesAPI, BlagueType
from discord.ext import commands
from dotenv import load_dotenv


# récupère le mode de lancement du bot
parser = argparse.ArgumentParser()
parser.add_argument('-m','--mode', type=int, default=0, help='Mode de lancement du bot, 1: dev, autre: public')
args = parser.parse_args()


# charge les variables d'environnement
load_dotenv()

# charge les données du fichier data.json
with open('data.json') as json_file:
   data = json.load(json_file)


# initialise le bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

# initialise l'API de blagues
blagues = BlaguesAPI(os.getenv('BLAGUES_API_TOKEN'))

# function to check if all characters in a string are punctuation
def all_char_punct(str):
   all = True
   for i in str:
      if i not in data['punct']:
         all = False
   return all

def cant_write_in_dev(ctx):
   return 'dev' not in [role.name.lower() for role in ctx.author.roles] and args.mode == 1


def keyword_in_msg(msg, keyword):
   assert type(msg) == list
   for i in data['possible_'+keyword]:
      if msg[-1] == i:
         return True
      elif len(msg)>1 and i in msg[-2] and all_char_punct(msg[-1]):
         return True

async def send_joke(ctx, type):
   if cant_write_in_dev(ctx):
      await ctx.send("le bot est en dev mode sorry :(")
   else:
      blague = await blagues.random_categorized(type)
      await ctx.send(blague.joke)
      await ctx.send(blague.answer + random.choice(data['emojis']))

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
   await send_joke(ctx, BlagueType.BEAUF)

# commande qui affiche une blague humour noir
@bot.command(name='humour_noir')
async def humour_noir(ctx):
   await send_joke(ctx, BlagueType.HUMOUR_NOIR)

# commande qui permet de changer le mode du bot, de dev à public et vice versa
@bot.command(name='toggle_dev')
async def toggle_dev(ctx):
   # si l'utilisateur a le role "dev", on change le mode du bot
   if 'dev' in [role.name.lower() for role in ctx.author.roles]:
      if args.mode == 1:
         args.mode = 2
         await ctx.send("le bot est maintenant en mode public")
      else:
         args.mode = 1
         await ctx.send("le bot est maintenant en mode dev")
   # sinon, on ne fait rien
   else:
      await ctx.send("tu n'as pas le droit de faire ça, t'es pas dev :joy_cat:")


# commande qui affiche la liste des commandes
@bot.command(name='help')
async def help(ctx):
   # si le dev mode est activé et que l'utilisateur n'a pas le role "dev", le bot ne répond pas
   if cant_write_in_dev(ctx):
      await ctx.send("le bot est en dev mode sorry :smiling_face_with_tear: ")
   # sinon, le bot répond
   else:
      # construit la liste des commandes avec leur description grâce à la variable cmds
      msg = "```bonjour, je suis un potit blagueur, voici la liste des commandes que je connais :\n"
      for cmd in data['cmds']:
         msg += cmd + " : " + data['cmds'][cmd] + "\n"
      msg += "je connais aussi d'autres choses mais je ne vais rien dévoiler ;)```"
      await ctx.send(msg)


# partie qui permet au bot de répondre à certains messages
@bot.event
async def on_message(message):
   # n'envoie pas de message si le message est envoyé par le bot (évite les boucles infinies)
   if message.author == bot.user:
         return
   
   msg = message.content.lower().split(" ")
   keywords = ['quoi', 'qui', 'hein']
   
   for keyword in keywords:
      if keyword_in_msg(msg, keyword):
         if cant_write_in_dev(message):
            return
         await message.reply(random.choice(data['answers_'+keyword]) + " :joy_cat:")
         return
         
   #check if a message contain "feur" and send a message
   for i in data['answers_quoi']:
      if i in message.content.lower():
         # si le dev mode est activé et que l'utilisateur n'a pas le role "dev", le bot ne répond pas
         if 'dev' not in [role.name.lower() for role in message.author.roles] and args.mode == 1:
            return
         # sinon, le bot répond
         await message.add_reaction('🙀')
         await message.reply("masterclass akhy :joy_cat:")
         return # on sort de la fonction pour éviter que le bot réponde deux fois

   for ans in data['formulations']:
      if ans in message.content.lower():
         await message.reply(data["formulations"][ans] + " :joy_cat:")
         return # on sort de la fonction pour éviter que le bot réponde deux fois
   
   # regarde si le message est une commande
   await bot.process_commands(message)

# lance le bot
bot.run(os.getenv('DISCORD_TOKEN'))
