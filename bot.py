import os, discord, random, argparse, json
# from blagues_api import BlaguesAPI, BlagueType
from discord.ext import commands
from dotenv import load_dotenv
import re

# charge les variables d'environnement
load_dotenv()

# charge les données du fichier data.json
with open('data.json') as json_file:
    data = json.load(json_file)

# initialise le bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)
reactions_id = {1 : "quoi", 2 : "qui", 3 : "hein"}

# initialise l'API de blagues
# blagues = BlaguesAPI(os.getenv('BLAGUES_API_TOKEN'))

# async def send_joke(ctx, type):
#    if cant_write_in_dev(ctx):
#       await ctx.send("le bot est en dev mode sorry :(")
#    else:
#       blague = await blagues.random_categorized(type)
#       await ctx.send(blague.joke)
#       await ctx.send(blague.answer + random.choice(data['emojis']))

# display a message when the bot is ready and indicate the mode of the bot
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord !')


# commande qui affiche une blague beauf
# @bot.command(name='blague_beauf')
# async def blague_beauf(ctx):
#    await send_joke(ctx, BlagueType.BEAUF)

# commande qui affiche une blague humour noir
# @bot.command(name='humour_noir')
# async def humour_noir(ctx):
#    await send_joke(ctx, BlagueType.HUMOUR_NOIR)

# commande qui affiche la liste des commandes
# @bot.command(name='help')
# async def help(ctx):
#    # si le dev mode est activé et que l'utilisateur n'a pas le role "dev", le bot ne répond pas
#    if cant_write_in_dev(ctx):
#       await ctx.send("le bot est en dev mode sorry :smiling_face_with_tear: ")
#    # sinon, le bot répond
#    else:
#       # construit la liste des commandes avec leur description grâce à la variable cmds
#       msg = "```bonjour, je suis un potit blagueur, voici la liste des commandes que je connais :\n"
#       for cmd in data['cmds']:
#          msg += cmd + " : " + data['cmds'][cmd] + "\n"
#       msg += "je connais aussi d'autres choses mais je ne vais rien dévoiler ;)```"
#       await ctx.send(msg)

def keyword_in_msg(msg, keyword):
    assert type(msg) == list
    for i in data['possible_' + keyword]:
        if msg[-1] == i:
            return True

# va renvoyer tout un tas d'informations, sous la forme d'un tuple, avec un booleen pour le cas ou feur est dans le mot
# et un id pour le message a renvoyer (0 pour rien, 1 pour quoi, 2 pour qui, 3 pour hein) (idrep)
def get_message_data(msg: list):
    assert type(msg) is list
    match msg[-1]:
        case 'quoi':
            idrep = 1
        case 'qui':
            idrep = 2
        case 'hein':
            idrep = 3
        case _:
            idrep = 0
    joined_msg = " ".join(msg)
    i = 0
    hasfeur = False
    while i < len(data['answers_quoi']) and hasfeur == False:
        hasfeur = re.search(data['answers_quoi'][i], joined_msg) is not None
        i = i + 1

    return (hasfeur, idrep)

# partie qui permet au bot de répondre à certains messages
@bot.event
async def on_message(message):
    # n'envoie pas de message si le message est envoyé par le bot (évite les boucles infinies)
    if message.author == bot.user:
        return

    # msg = message.content.lower().split(" ")
    msg = [s for s in re.split("\W", message.content.lower()) if len(s) > 1]
    keywords = ['quoi', 'qui', 'hein']

    (feur, id_rep) = get_message_data(msg);

    if feur :
        await message.add_reaction('🙀')
        await message.reply("masterclass akhy :joy_cat:")
        return

    if id_rep > 0:
        await message.reply(random.choice(data['answers_' + reactions_id[id_rep]]) + " :joy_cat:")
        return
    # for keyword in keywords:
    #     if keyword_in_msg(msg, keyword):
    #         await message.reply(random.choice(data['answers_' + keyword]) + " :joy_cat:")
    #         return
    #
    # # check if a message contain "feur" and send a message
    # for i in data['answers_quoi']:
    #     if i in message.content.lower():
    #         await message.add_reaction('🙀')
    #         await message.reply("masterclass akhy :joy_cat:")
    #         return  # on sort de la fonction pour éviter que le bot réponde deux fois
    #
    # for ans in data['formulations']:
    #     if ans in message.content.lower():
    #         await message.reply(data["formulations"][ans] + " :joy_cat:")
    #         return  # on sort de la fonction pour éviter que le bot réponde deux fois

    # regarde si le message est une commande
    await bot.process_commands(message)


# lance le bot
bot.run(os.getenv('DISCORD_TOKEN'))
