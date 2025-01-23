import os, discord, random, argparse, json
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

# function to check if all characters in a string are punctuation
def all_char_punct(str):
	all = True
	for i in str:
		if i not in data['punct']:
			all = False
	return all

def keyword_in_msg(msg, keyword):
	assert type(msg) == list
	for i in data['possible_'+keyword]:
		if i in msg[-1]:
			return True
		elif len(msg)>1 and i in msg[-2] and all_char_punct(msg[-1]):
			return True

def msg_starts_with(msg, keyword):
	for i in data['possible_'+keyword]:
		if msg[-1].startswith(keyword):
			return (True, msg[-1][len(keyword):])
		elif len(msg)>1 and msg[-2].startswith(keyword) and all_char_punct(msg[-1]):
			return (True, msg[-1][len(keyword):])
	return (False, "")

def msg_ends_with(msg, keyword):
	for i in data['possible_'+keyword]:
		if msg[-1].endswith(keyword):
			return (True, msg[-1][:(len(msg[-1])-len(keyword))])
		elif len(msg)>1 and msg[-2].endswith(keyword) and all_char_punct(msg[-1]):
			return (True, msg[-2][:(len(msg[-2])-len(keyword))])
	return (False, "")

def stupid_message(msg):
	new_msg = ""
	new_msg += '"'
	for i in range(0,len(msg)):
		if i%2 == 0:
			new_msg+=msg[i].upper()
		else:
			new_msg+=msg[i]
	new_msg += '"'
	return new_msg

# display a message when the bot is ready and indicate the mode of the bot
@bot.event
async def on_ready():
	print(f'{bot.user.name} has connected to Discord in public mode !')


# commande qui affiche la liste des commandes
@bot.command(name='help')
async def help(ctx):
	msg = "```bonjour, je suis un potit blagueur, voici la liste des commandes que je connais :\n"
	for cmd in data['cmds']:
		msg += cmd + " : " + data['cmds'][cmd] + "\n"
	msg += "je connais aussi d'autres choses mais je ne vais rien dévoiler ;)```"
	await ctx.send(msg)

@bot.command(name='mock')
async def mock(ctx):
	if ctx.message.reference:
		original_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
		msg = stupid_message(original_message.content.lower())
		await ctx.message.reply(msg+" :index_pointing_at_the_viewer: :joy_cat:"+"\n\nhttps://i.kym-cdn.com/photos/images/original/001/268/278/b8c.gif")
		return
	else:
		return

# partie qui permet au bot de répondre à certains messages
@bot.event
async def on_message(message):
	# n'envoie pas de message si le message est envoyé par le bot (évite les boucles infinies)
	if message.author == bot.user:
		return
   
	msg = message.content.lower().split(" ")
	keywords = ['quoi', 'qui', 'hein', 'ouais']
   
	#if (message.author.id == 448181101932970016):
	#	msg = stupid_message(message.content.lower())
	#	await message.reply(msg+ ":index_pointing_at_the_viewer: :joy_cat:" + "\nhttps://i.kym-cdn.com/photos/images/original/001/268/278/b8c.gif"448181101932970016)
	#	return

	for keyword in keywords:
		(starts, end) = msg_starts_with(msg, keyword)
		if starts:
			await message.reply(random.choice(data['answers_'+keyword]) + end + " :joy_cat:")
			return
		(ends, start) = msg_ends_with(msg, keyword)
		if ends:
			await message.reply(start + random.choice(data['answers_'+keyword]) + " :joy_cat:")
			return
		if keyword_in_msg(msg, keyword):
			await message.reply(random.choice(data['answers_'+keyword]) + " :joy_cat:")
			return

         
	#check if a message contain "feur" and send a message
	for i in data['answers_quoi']:
		if i in message.content.lower():
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
