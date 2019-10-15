"""
Works with Python 3.6!
Artie.py
Authored by Riley Knybel
Published under the Unlicense
----------------------------------------------------
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

import discord
import configparser
import sys
import datetime
import asyncio
import random
import numbers
import codecs
import os
import re
from discord.utils import get

#AI Chatbot Setup
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

#VARIABLES--------------------------------------------

#This block of variables is populated by the values in the config file. Changes made here will not hold.
botToken = ''
botName = ''
botAuthor = ''
convowakeword = ''

#Global objects
client = discord.Client()
configFile = configparser.ConfigParser()
serverRolesListFile = configparser.ConfigParser()

serverRolesListFile.optionxform = str

#Global variables
versionNumber = '0.07'


print('Reading config and role list files...')

#read/create the supporting data files
try:
    fileExists = open('config.txt', 'r') #Try to load the config file

    configFile.sections() #initialize config file sections
    configFile.read('config.txt') #load the config file

    fileExists = open('serverRolesList.txt', 'r')

    serverRolesListFile.sections()
    serverRolesListFile.read('serverRolesList.txt')
    

    botToken = configFile['BotAPI']['bottoken'] #store the bot token in the variable
    botName = configFile['BotAPI']['botname'] #store the bot name in the variable
    botAuthor = configFile['BotAPI']['botauthor'] #store the bot author in the variable
    convowakeword = configFile['BotAPI']['convowakeword'] #store the wake word in the variable
except: #if the config file cannot be loaded properly
    initialize_configfile() #run the initialize_configfile function


print(botName + ' is starting! (Version ' + versionNumber + ')\n-----------------')


print("Initializing AI Chatbot...")

#Check if intelligence database exists, make it if it doesn't
try:
    fileExists = open('Intelligence.sqlite3', 'r') #Try to load the config file#trainer = ChatterBotCorpusTrainer(bot) #set bot trainer to corpus
    print("Intelligence database found!")
    #INITIALIZE AND TRAIN AI CHATBOT
    bot = ChatBot( #define tha chatbot
        'Artie',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        logic_adapters=[
            'chatterbot.logic.MathematicalEvaluation',
        #    'chatterbot.logic.TimeLogicAdapter',
            'chatterbot.logic.BestMatch'
            ],
        database_uri='sqlite:///Intelligence.sqlite3'
    )
    bot.set_trainer(ListTrainer) #set bot training to ListTrainer

except:
    print("Intelligence database not found. AI must be trained.")

    bot = ChatBot( #define tha chatbot
        'Artie',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        logic_adapters=[
            'chatterbot.logic.MathematicalEvaluation',
        #    'chatterbot.logic.TimeLogicAdapter',
            'chatterbot.logic.BestMatch'
            ],
        database_uri='sqlite:///Intelligence.sqlite3'
    )

    bot.set_trainer(ListTrainer) #set bot training to ListTrainer

    print("Training AI from TrainingData.txt, this may take a while...")

    data = open('TrainingData.txt').read() #open the training file
    processedData = data.strip().split('\n') #convert the text data to a list data type

    bot.train(processedData) #train the bot with the processed training file

print('Chatbot initialized successfully!\n-----------------')

#FUNCTIONS--------------------------------------------

def initialize_configfile(): #creates a template config file
    configFile['BotAPI'] = {'BotToken' : 'Bot token goes here', #define bot parameters
                        'BotName' : 'Bot name goes here',
                        'BotAuthor' : 'Bot author\'s name goes here',
                        'convowakeword' : 'Artie'}

    with open('config.txt', 'w+') as configfile: #set the config file name and permissions
        configFile.write(configfile); #write the config file

    print('Please edit the newly created config.txt file and run the script again.\n') #ask the user to edit the config file
    sys.exit() #close the application

async def type_message(destination_channel, message_text): #'types' and posts a message in a Discord channel, giving a more realistic response. Bases typing time on message length.

    await client.send_typing(destination_channel) #set the typing status in Discord client

    await asyncio.sleep(0.03 * len(str(message_text))) #wait 0.03 seconds

    await client.send_message(destination_channel, message_text) #send the message in Discord client

def roll_dice(numDice, sides):
    dice = []
    numDice = int(numDice)
    sides = int(sides)
    diceString = ''
    total = 0
    
    for d in range(numDice):
        dice.append(random.randint(1, sides))
        total += dice[d]
        diceString += "Die " + str(d + 1) + ": " + str(dice[d]) + '\n'
    
    diceString += "Total: " + str(total)
    
    return diceString

#COMMAND FUNCTIONS--------------------------------------------

async def info(messageObject):#Information about the bot
    msg = '**' + botName + ' v' + versionNumber + '**\nAuthor: ' + botAuthor
    await client.send_message(messageObject.channel, msg) #send the info string in the channel that the ~info message came from
    return #stop on_message here

async def help(messageObject):#Help command for users
    msg = "**Owo here are the commands you can use:**\n\
        `~info`: Information about the bot\n\
        `~teach [keyword] = [response]`: Teach me what certain phrases mean.\n\t\t\t Example: `~teach lol = 🤣`\n\
        `~wolf`: Get a random cute wolfie picture owo\n\
        `~cat`: Get a random cute kitty picture owo\n\
        `~dice [number of dice] [number of sides]`: Roll dice, useful for RPGs!\n\
        `~listroles`: List the roles that you can add with `~addrole`\n\
        `~addrole [role]`: Add a role to yourself\n\
        `~remrole [role]`: Remove a role from yourself\n\
        `~customrole [Custom Role Name] #XXXXXX`. Color is in a 6-digit hex code. Add one custom role to yourself c:\n\
        `~fuwwy [text]`: Converts normal text to fuwwy text!\n"

    await client.send_message(messageObject.channel, msg);
    return

async def wolfpic(messageObject):#Sends a random wolf image in chat
    msg = ':wolf: Here\'s your wolfie:'
    wolfiefile = random.choice(os.listdir('images/wolves'))
    await client.send_file(messageObject.channel, 'images/wolves/' + wolfiefile, content=msg)

async def catpic(messageObject):#Sends a random cat image in chat
    msg = ':smiley_cat: Here\'s your kitty:'
    kittyfile = random.choice(os.listdir('images/cats'))
    await client.send_file(messageObject.channel, 'images/cats/' + kittyfile, content=msg)

async def dice(messageObject):#Rolls dice and sends the results in chat
    helpMsg = "**Usage:** ~dice [number of dice] [number of sides]\n **Example:** ~dice 2 6"
    msg = ''
    wordsInCommand = messageObject.content.lower().split(' ')
    numOfDice = 0;
    numOfSides = 0;

    if(len(wordsInCommand) != 3):
        await client.send_message(messageObject.channel, helpMsg)
        return
    
    try:
        numOfDice = int(wordsInCommand[1])
    except:
        await client.send_message(messageObject.channel, helpMsg)
        return

    try:
        numOfSides = int(wordsInCommand[2])
    except:
        await client.send_message(messageObject.channel, helpMsg)
        return

    if numOfSides == 0:
        await client.send_message(messageObject.channel, "Dice can't be zero-sided, dingus! That's physically impossible!");
        return

    if numOfSides < 0:
        await client.send_message(messageObject.channel, "I can't role a die that's inside-out.");
        return

    if numOfDice == 0:
        await client.send_message(messageObject.channel, "Come on buddy, there aren't any dice to roll!");
        return

    if numOfDice < 0:
        await client.send_message(messageObject.channel, "Wtf! You cannot role negative dice!");
        return

    if numOfDice > 10:
        await client.send_message(messageObject.channel, "That's too many dice, I'll lose count of them. 10 max please.");
        return
        
    msg = "**:game_die:Results:game_die:**\n" + roll_dice(numOfDice, numOfSides)
    await client.send_message(messageObject.channel, msg)
    return    

async def teach(messageObject):#Trains the AI with one definition/response
    definitionMessage = messageObject.content.split(' = ') #split the message by the equals sign
    trigger = definitionMessage[0].replace('~teach ', '')#remove ~teach from the trigger part of the command 
    response = definitionMessage[1] #store the response part of the comand

    if trigger == convowakeword:
        await type_message(messageObject.channel, "You can't define my name as a keyword, I'll get confused >w<") #type a confirmation in the channel the command was said in
        return #stop on_message here
        
    bot.train([trigger, response,])
    await type_message(messageObject.channel, "Thank you, sensei!") #type a confirmation in the channel the command was said in
    return #stop on_message here

async def deldef(messageObject):#Deletes a keyword in the case of a conflict
    trigger = messageObject.content.lower().replace('~deldef ', '')#remove ~deldef from the trigger part of the command and convert it to lower case

    try:
        learnedArtFile.remove_option('art::learned', trigger)
        with open('learned.art', 'w') as f: #open the learned file
            learnedArtFile.write(f) #update the file
        await type_message(messageObject.channel, "Removed custom response `" + trigger + "`")
    except:
        await type_message(messageObject.channel, "Couldn't remove response, probably because it doesn't exist.")

async def customRole(messageObject):#Creates a custom role and adds it to the user
    if messageObject.server.id == '515209981872570369':#If the command is used in Baxby's Ball...
            
        usageMsg = "Invalid command. Usage: `~customrole [Custom Role Name] #XXXXXX`. Color is in a 6-digit hex code."

        roleNameContent = re.search("~customrole (.*) #", messageObject.content)
            
        try:#try to get the name of the role from the command
            roleName = "✪" + roleNameContent.group(1)
        except:
            msg = usageMsg
            await client.send_message(messageObject.channel, msg)
            return

        try:#try to get the color of the role from the command
            roleColor = re.search("#(.*)", messageObject.content).group(1)
        except:
            msg = usageMsg
            await client.send_message(messageObject.channel, msg)
            return

        if len(roleColor) !=6:#check if the color is 6 digits long
            msg = usageMsg
            await client.send_message(messageObject.channel, msg)
            return

        if roleColor == "000000":#If the role color is pure black...
            roleColor = "010000"#Make it VERY slightly red cause discord api doesn't like that

        try:#try to convert the string color to an int
            roleColorInt = int(roleColor, 16)
        except:
            msg = usageMsg
            await client.send_message(messageObject.channel, msg)
            return
        
        role = discord.utils.get(messageObject.author.server.roles, name=roleName)

        if str(role) == roleName:
            msg="That role already exists. Please pick a different name and try again."
            await client.send_message(messageObject.channel, msg)
            return
                

        #Actual Role-Adding Part Now

        for roleObject in messageObject.author.roles:#Check every role the user has
            if str(roleObject.name).startswith("✪"):#if the role starts with a star, delete it.
                roleToDelete = discord.utils.get(messageObject.author.server.roles, name=roleObject.name)
                await client.remove_roles(messageObject.author, roleToDelete)
                await client.delete_role(messageObject.author.server, roleToDelete)


        await client.create_role(messageObject.author.server, name=roleName, colour=discord.Colour(roleColorInt))
        role = discord.utils.get(messageObject.author.server.roles, name=roleName)
        await client.add_roles(messageObject.author, role)
                
        msg = "Successfully added your role named \"" + roleName + "\" with the color #" + roleColor;
        await client.send_message(messageObject.channel, msg)
    return
            
async def listRoles(messageObject):#Lists the roles in the server that can be added
    msg = "**Add any of these roles with the command** `~addrole [role name]`**:**\n"
    serverId = messageObject.server.id
        
    for key in serverRolesListFile[serverId]:
        msg += key + "\n"

    await client.send_message(messageObject.channel, msg)
    return

async def regRole(messageObject):#Adds a role to the list of roles that can be added
    if str(messageObject.author.id) == "376088004135223297":#If Riley sent the command...
        
        roleName = messageObject.content[9:]
        
        
        user = messageObject.author
        role = discord.utils.get(user.server.roles, name=str(roleName))
        serverId = messageObject.server.id

        if str(role) == "None":
            await type_message(messageObject.channel, "That role doesn't exist. Please check case or add it in the server settings and try that command again. uwu.")
            return
            
        serverId = messageObject.server.id

        try:
            serverRolesListFile.add_section(str(serverId))
        except:
            print("oof")
            
        serverRolesListFile.set(serverId, roleName, serverId)

        with open('serverRolesList.txt', 'w') as f:
            serverRolesListFile.write(f)

        await type_message(messageObject.channel, "Registered the role **" + roleName + "**. It can now be added with the ~addrole command. owo.")
        
        return

async def unRegRole(messageObject):#Removes a role from the list of roles that can be added
    if str(messageObject.author.id) == "376088004135223297":
            
        roleName = messageObject.content[11:]

        user = messageObject.author
        role = discord.utils.get(user.server.roles, name=str(roleName))
        serverId = messageObject.server.id
            
        for key in serverRolesListFile[serverId]:
            if key == roleName:
                serverRolesListFile.remove_option(serverId, roleName)
                with open('serverRolesList.txt', 'w') as f:
                    serverRolesListFile.write(f)
                await type_message(messageObject.channel, 'Removed role definition: **' + roleName + "**. The role was not deleted. uwo.")
                return
            await type_message(messageObject.channel, "That role doesn't exist. Unregistry of role failed OnO!! Try checking case and spelling. uwo.")
            return

async def addRole(messageObject):#Adds a role to a user
    roleName = messageObject.content[9:]

    user = messageObject.author
    role = discord.utils.get(user.server.roles, name=str(roleName))
    serverId = messageObject.server.id

    for key in serverRolesListFile[serverId]:
        if key == roleName:
            await client.add_roles(user, role)
            await type_message(messageObject.channel, "Successfully added role **" + roleName + "**! uwo!!")
            return
        
    await type_message(messageObject.channel, "That role doesn't exist. Check the spelling and case. uwo.")

async def remRole(messageObject):#Removes a role from a user
    roleName = messageObject.content[9:]

    user = messageObject.author
    role = discord.utils.get(user.server.roles, name=str(roleName))
    serverId = messageObject.server.id

    for key in serverRolesListFile[serverId]:
        if key == roleName:
            await client.remove_roles(user, role)
            await type_message(messageObject.channel, "Successfully removed role **" + roleName + "**! uwo!!")
            return
    await type_message(messageObject.channel, "That role doesn't exist. Check the spelling and case. uwo.")

async def fuwwy(messageObject):
	messageContent = messageObject.content[7:]
	messageContent = messageContent.replace('r', 'w')
	messageContent = messageContent.replace('l', 'w')
	messageContent = messageContent.replace('R', 'W')
	messageContent = messageContent.replace('L', 'W')

	messageContent = messageContent.replace('na', 'nya')
	messageContent = messageContent.replace('ne', 'nye')
	messageContent = messageContent.replace('ni', 'nyi')
	messageContent = messageContent.replace('no', 'nyo')
	messageContent = messageContent.replace('nu', 'nyu')

	messageContent = messageContent.replace('Na', 'Nya')
	messageContent = messageContent.replace('Ne', 'Nye')
	messageContent = messageContent.replace('Ni', 'Nyi')
	messageContent = messageContent.replace('No', 'Nyo')
	messageContent = messageContent.replace('Nu', 'Nyu')

	messageContent = messageContent.replace('NA', 'NYA')
	messageContent = messageContent.replace('NE', 'NYE')
	messageContent = messageContent.replace('NI', 'NYI')
	messageContent = messageContent.replace('NO', 'NYO')
	messageContent = messageContent.replace('NU', 'NYU')

	await client.send_message(messageObject.channel, messageContent)

async def commandNotFoundAI(messageObject):#Tries to run the response thingy
    if messageObject.content.lower().startswith('a.'):
        print("AI INPUT: \"" + messageObject.content[2:] + "\"")
        await client.send_typing(messageObject.channel) #set the typing status in Discord client
        bot_output = bot.get_response(messageObject.content[2:]).text
        print("AI OUTPUT: \"" + bot_output + "\"")
        await client.send_message(messageObject.channel, bot_output)
        return
    if configFile['BotAPI']['convowakeword'].lower() in messageObject.content.lower(): #if the bot's name is in the message...
        print("AI INPUT: \"" + messageObject.content + "\"")
        await client.send_typing(messageObject.channel) #set the typing status in Discord client
        bot_output = bot.get_response(messageObject.content).text
        print("AI OUTPUT: \"" + bot_output + "\"")
        await client.send_message(messageObject.channel, bot_output)
        return
    print("Training: " + messageObject.content)
    #bot.train(messageObject.content)


#DISCORD CLIENT FUNCTIONS--------------------------------------------

@client.event

async def on_reaction_add(reaction, user): #add a reaction when a user reacts to a message
    await asyncio.sleep(2.0) #wait 2 seconds
    await client.add_reaction(reaction.message, reaction.emoji)

@client.event

async def on_message(message): #when a message is sent in a channel Artie can see...

    if message.author == client.user: #if the message came from Artie...
        return #stop on_message here, do not attempt to respond

    if message.content.lower().startswith('~dice'):
        await dice(message)
        return

    if message.content.lower().startswith('~wolf'): #if the message starts with ~wolf
        await wolfpic(message)
        return

    if message.content.lower().startswith('~cat'): #if the message starts with ~wolf
        await catpic(message)
        return

    if message.content.lower().startswith('~info'): #if the message starts with ~info...
        await info(message)
        return

    #if message.content.lower().startswith('~define'): #if the message starts with ~define
    #    await define(message)
    #    return
    
    if message.content.lower().startswith('~deldef'): #if the message starts with ~deldef
        await deldef(message)
        return

    if message.content.lower().startswith('~regrole'):
        await regRole(message)
        return

    if message.content.lower().startswith('~unregrole'):
        await unRegRole(message)
        return
                    
    if message.content.lower().startswith('~addrole'):
        await addRole(message)
        return

    if message.content.lower().startswith('~remrole'):
        await remRole(message)
        return

    if message.content.lower().startswith('~listroles'):
        await listRoles(message)
        return

    if message.content.lower().startswith('~help'):
        await help(message)
        return

    if message.content.lower().startswith('~customrole'):
        await customRole(message)
        return

    if message.content.lower().startswith('~teach'):
        await teach(message)
        return

    if message.content.lower().startswith('~fuwwy'):
    	await fuwwy(message)
    	return

    await commandNotFoundAI(message)


@client.event
async def on_ready(): #when the bot is connected and logged into Discord..
    #print information to the console
    print('Logged into Discord as ' + client.user.name + ' (User ID #' + client.user.id + ')\n-----------------') 
    await client.change_presence(game=discord.Game(name="type ~help")) #Set the playing status to help users
    print('Debug log:')
#ACTUAL CODE--------------------------------------------


print("Connecting to Discord...")
client.run(botToken) #start the bot and its callback functions
