# initialise les variables du bot qui vont lui permettre de répondre à certains messages
# on ira chercher les réponses dans une liste, pour pouvoir facilement en ajouter ou en supprimer
possible_quoi = ['quoi', 'quoi ?', 'quoi?', 'quoient', 'quoient ?', 'quoient?', 'Quoi', 'Quoi ?', 'Quoi?', 'Quoient', 'Quoient ?', 'Quoient?']
answers_quoi = ['feur','feuse','fure','drilatère','driceps','chi']

possible_qui = ['qui', 'qui ?', 'qui?', 'ki', 'ki ?', 'ki?', 'Qui', 'Qui ?', 'Qui?', 'Ki', 'Ki ?', 'Ki?']
emojis = [" :rofl:"," :sunglasses:", " :fire:", " :joy:"]
cmds = {"/blague_beauf": "renvoie une blague beauf", "/humour_noir": "renvoie une blague humour noir", "/help": "renvoie la liste des commandes"}