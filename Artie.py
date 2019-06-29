"""
Works with Python 3.6!
Artie.py, version 0.1
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

coreArtFile = configparser.ConfigParser()
learnedArtFile = configparser.ConfigParser()

#Global variables
versionNumber = '0.03'
moodFloat = 0.8;

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

    for characterIndex in range(len(message_text)): #for every character in message_text...
        await asyncio.sleep(0.03) #wait 0.03 seconds

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
    msg = ('**' + botName + ' v' + versionNumber + '**\nAuthor: ' + botAuthor + "\n\n Type `~define` to add keywords/responses that I can use! For example:\n`~define owo = uwu!`").format(messageObject) #form a string with bot information
    await client.send_message(messageObject.channel, msg) #send the info string in the channel that the ~info message came from
    return #stop on_message here

async def help(messageObject):#Help command for users
    msg = "**Owo here are the commands you can use:**\n\
        `~info`: Information about the bot\n\
        `~define [keyword] = [response]`: Add keywords and responses that I can use.\n\t\t\t Example: `~define owo = uwu!`\n\
        `~wolf`: Get a random cute wolfie picture owo\n\
        `~cat`: Get a random cute kitty picture owo\n\
        `~dice [number of dice] [number of sides]`: Roll dice, useful for RPGs!\n\
        `~listroles`: List the roles that you can add with `~addrole`\n\
        `~addrole [role]`: Add a role to yourself\n\
        `~remrole [role]`: Remove a role from yourself\n\
        `~customrole [Custom Role Name] #XXXXXX`. Color is in a 6-digit hex code. Add one custom role to yourself c:\n"

    await client.send_message(messageObject.channel, msg);
    return

async def wolfpic(messageObject):#Sends a random wolf image in chat
    msg = ':wolf: Here\'s your wolfie:'
    wolfiefile = random.choice(os.listdir('images/wolves'))
    await client.send_file(message.channel, 'images/wolves/' + wolfiefile, content=msg)

async def catpic(messageObject):#Sends a random cat image in chat
    msg = ':smiley_cat: Here\'s your kitty:'
    kittyfile = random.choice(os.listdir('images/cats'))
    await client.send_file(message.channel, 'images/cats/' + kittyfile, content=msg)

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

async def define(messageObject):#Adds a new keyword definition to the learned.art file
    definitionMessage = messageObject.content.split(' = ') #split the message by the equals sign
    trigger = definitionMessage[0].lower().replace('~define ', '')#remove ~define from the trigger part of the command and convert it to lower case
    response = definitionMessage[1] #store the response part of the comand

    if trigger == convowakeword:
        await type_message(messageObject.channel, "You can't define my name as a keyword, I'll get confused >w<") #type a confirmation in the channel the command was said in
        return #stop on_message here
        
    learnedArtFile.set('art::learned', trigger, response) #create a new key in the learnedArtFile config object

    with open('learned.art', 'w') as f: #open the learned file
        learnedArtFile.write(f) #write the new entry to the file
            
    await type_message(messageObject.channel, "Added entry\nTrigger: " + trigger + "\nResponse: " + response) #type a confirmation in the channel the command was said in
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

async def commandNotFound(messageObject):#Tries to run the response thingy
    if configFile['BotAPI']['convowakeword'].lower() in messageObject.content.lower(): #if the bot's name is in the message...
    
        if "knight me" in messageObject.content.lower(): #if the message contains "knight me"...
            user = messageObject.author #get the author of the message
            role = discord.utils.get(user.server.roles, name="Knight") #get the Knight role
            await client.add_roles(user, role) #add the knight role to the user who said knight me
            await type_message(messageObject.channel, "*Produces sword and taps your left shoulder, then your right, then boops your snoot with it* I dub thee Sir Knight.")
            return #stop on_message here
        for key in coreArtFile['art::core']: #iterate over the custom responses..
            if " " + key in messageObject.content.lower() or key + " " in messageObject.content.lower(): #if a response trigger is in the message..
                await type_message(messageObject.channel, coreArtFile['art::core'][key]) #type and send the response using the type_response funtion
                return #stop on_message here
        for key in learnedArtFile['art::learned']: #iterate over the custom responses..
            if " " + key in messageObject.content.lower() or key + " " in messageObject.content.lower(): #if a response trigger is in the message..
                await type_message(messageObject.channel, learnedArtFile['art::learned'][key]) #type and send the response using the type_response funtion
                return #stop on_message here
        await client.add_reaction(messageObject, '🤔')

    if messageObject.author.name.startswith("Zippy#0143"):
        await type_message(messageObject.channel, "ZIPPY IS GAY")
        print("ZIPPY IS GAY")
        
    #if all fails due to a response not being recognized..
    suggestionTime = datetime.datetime.now() #create a time object
    suggestionTimeString = str(suggestionTime); #create a time string
    print("Unexpected message: ", suggestionTimeString, ', ', messageObject.author, ', ', messageObject.content); #print info about the unexpected message to the console

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

    if message.content.lower().startswith('~define'): #if the message starts with ~define
        await define(message)
        return
    
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

    await commandNotFound(message)


@client.event
async def on_ready(): #when the bot is connected and logged into Discord..
    #print information to the console
    print('Logged in as') 
    print(client.user.name) #prints the bot's username
    print(client.user.id) #prints the bot's user ID
    print('------')
    await client.change_presence(game=discord.Game(name="type ~help")) #Set the playing status to help users

#ACTUAL CODE--------------------------------------------

#read/create the supporting data files
try:
    fileExists = open('config.txt', 'r') #Try to load the config file

    configFile.sections() #initialize config file sections
    configFile.read('config.txt') #load the config file

    fileExists = open('core.art', 'r') #Try to load the core art file

    coreArtFile.sections() #initialize core art file sections
    coreArtFile.read('core.art') #load the core art file

    fileExists = open('learned.art', 'r') #Try to load the learned art file

    learnedArtFile.sections() #initialize learned art file sections
    learnedArtFile.read('learned.art') #load the learned art file

    fileExists = open('serverRolesList.txt', 'r')

    serverRolesListFile.sections()
    serverRolesListFile.read('serverRolesList.txt')
    

    botToken = configFile['BotAPI']['bottoken'] #store the bot token in the variable
    botName = configFile['BotAPI']['botname'] #store the bot name in the variable
    botAuthor = configFile['BotAPI']['botauthor'] #store the bot author in the variable
    convowakeword = configFile['BotAPI']['convowakeword'] #store the wake word in the variable
except: #if the config file cannot be loaded properly
    initialize_configfile() #run the initialize_configfile function

client.run(botToken) #start the bot and its callback functions
