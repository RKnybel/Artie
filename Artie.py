"""
Works with Python 3.6!

Artie.py, version 0.03
Authored by Nate Knybel
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

#VARIABLES--------------------------------------------

#This block of variables is populated by the values in the config file. Changes made here will not hold.
botToken = ''
botName = ''
botAuthor = ''
convowakeword = ''

#Global objects
client = discord.Client()
configFile = configparser.ConfigParser()

#Global variables
versionNumber = '0.03'
moodFloat = 0.8;

#FUNCTIONS--------------------------------------------

def adjust_mood(mod): #changes the moodFloat by a certain amount, enforcing the 0.0 minimum and 1.0 maximum
    global moodFloat #redefine moodFloat as global to keep it working
    moodFloat += mod #add the mod to moodFloat, whether it be positive or negative

    if moodFloat > 1.0: #if moodFloat is over the max...
        moodFloat = 1.0 #set moodFloat to max
    if moodFloat < 0.0: #if moodFloat is below the minimum...
        moodFloat = 0.0 # set moodFloat to the minimum

def initialize_configfile(): #creates a template config file
	configFile['BotAPI'] = {'BotToken' : 'Bot token goes here', #define bot parameters
                        'BotName' : 'Bot name goes here',
                        'BotAuthor' : 'Bot author\'s name goes here',
                        'convowakeword' : 'Artie'}

	configFile['Custom Responses'] = {'Hello' : 'Hi!'} #define one template custom response

	with open('config.txt', 'w+') as configfile: #set the config file name and permissions
		configFile.write(configfile); #write the config file

	print('Please edit the newly created config.txt file and run the script again.\n') #ask the user to edit the config file
	sys.exit() #close the application

def get_channel(channels, channel_name): #helper function to get a Discord channel object
    for channel in client.get_all_channels():
        print(channel)
        if channel.name == channel_name:
            return channel
    return None
            
async def type_message(destination_channel, message_text): #'types' and posts a message in a Discord channel, giving a more realistic response. Bases typing time on message length.

    await client.send_typing(destination_channel) #set the typing status in Discord client

    for characterIndex in range(len(message_text)): #for every character in message_text...
        await asyncio.sleep(0.03) #wait 0.03 seconds

    await client.send_message(destination_channel, message_text) #send the message in Discord client

#DISCORD CLIENT FUNCTIONS--------------------------------------------

@client.event
async def on_message(message): #when a message is sent in a channel Artie can see...

    if message.author == client.user: #if the message came from Artie...
        return #stop on_message here, do not attempt to respond

    if message.content.lower().startswith('~info'): #if the message starts with ~info...
        msg = ('**' + botName + ' v' + versionNumber + '**\nAuthor: ' + botAuthor).format(message) #form a string with bot information
        await client.send_message(message.channel, msg) #send the info string in the channel that the ~info message came from
        return #stop on_message here

    if configFile['BotAPI']['convowakeword'].lower() in message.content.lower(): #if the bot's name is in the message...
        for key in configFile['Custom Responses']: #iterate over the custom responses..
            if key in message.content.lower(): #if a response trigger is in the message..
                await type_message(message.channel, configFile['Custom Responses'][key]) #type and send the response using the type_response funtion
                return #stop on_message here
        if "you suck" in message.content.lower(): #if the message contains "you suck"...
            adjust_mood(-0.2) #reduce mood by 0.2
            await client.change_presence(game=discord.Game(name="Mood: " + str(round(moodFloat,2)), type=0)) #update playing status to see moodFloat under Artie's name
            await client.send_message(message.channel, "You hurt my feels! (Mood -0.2)") #let the user know that they are mean
            return #stop on_message here
        if "you rock" in message.content.lower(): #if the message contains "you rock"...
            adjust_mood(+0.2) #increase mood by 0.2
            await client.change_presence(game=discord.Game(name="Mood: " + str(round(moodFloat,2)), type=0))#update playing status to see moodFloat under Artie's name
            await client.send_message(message.channel, "Thanks! (Mood +0.2)") #express gratitude to the user
            return #stop on_message here
        
        #if all fails due to a respons not being recognized..
        suggestionTime = datetime.datetime.now() #create a time object
        suggestionTimeString = str(suggestionTime); #create a time string
        print("Unexpected message: ", suggestionTimeString, ', ', message.author, ', ', message.content); #print info about the unexpected message to the console
        with codecs.open('suggestions.csv', 'a+', encoding='utf8') as suggestionFile: #open the suggestions.csv file
            suggestionLine = suggestionTimeString + ", " + str(message.author) + ", " + str(message.content) + "\r\n" #create an entry string
            suggestionFile.write(suggestionLine) #write the entry string to the suggestionFile
            suggestionFile.close() #close the suggestion file
        

@client.event
async def on_ready(): #when the bot is connected and logged into Discord..
	#print information to the console
    print('Logged in as') 
    print(client.user.name) #prints the bot's username
    print(client.user.id) #prints the bot's user ID
    print('------')
    await client.change_presence(game=discord.Game(name="Mood: " + str(moodFloat), type=0)) #Set the playing status to display moodFloat's value

#ACTUAL CODE--------------------------------------------

#read/create the supporting data files
try:
	fileExists = open('config.txt', 'r') #Try to load the config file

	configFile.sections() #no idea what this does to be honest
	configFile.read('config.txt') #load the config file

	botToken = configFile['BotAPI']['BotToken'] #store the bot token in the variable
	botName = configFile['BotAPI']['BotName'] #store the bot name in the variable
	botAuthor = configFile['BotAPI']['BotAuthor'] #store the bot author in the variable
	convowakeword = configFile['BotAPI']['convowakeword'] #store the wake word in the variable
	with codecs.open('suggestions.csv', 'a+', encoding='utf8') as suggestionFile: #create the suggestions file if it doesn't already exist
		suggestionFile.close() #close the suggestion file
except: #if the config file cannot be loaded properly
    initialize_configfile() #run the initialize_configfile function
    with codecs.open('suggestions.csv', 'a+', encoding='utf8') as suggestionFile: #create the suggestions file if it doesn't already exist
    	suggestionFile.close() #close the suggestion file

client.run(botToken) #start the bot and its callback functions
