import asyncio
import datetime
import discord

#Set the intents to allow access to default intents as well as member related functions
intents = discord.Intents.default()
intents.members = True

GUILD = 0
TOKEN = ""

class BasedCounter(discord.Client):

    #Define class members
    memberList = 0
    memberScores = 0
    
    #Counts the number of times the word "based" appears in a message
    def count_the_based(self, mess):
        counterCounter = 0
        if(mess.content.lower().count("based") > 0):
            #Then, for each instance of "based", their parallel count will increment once
            for i in range(mess.content.lower().count("based")):
                counterCounter += 1
        return counterCounter

    #Events that happen upon connecting to the guild
    async def on_ready(self):
        #Get the guild associated with the testing ID
        guild = client.get_guild(GUILD)

        #Create lists corresponding to present members and a score to increment associated to each member
        self.memberList = guild.members
        self.memberList = list(self.memberList)
        self.memberScores = [0] * len(self.memberList)
        
        #To anyone who uses this code after me, I'm sorry.
        for mem in self.memberList:
            for chan in guild.text_channels:
                async for mess in chan.history():
                    self.memberScores[self.memberList.index(mem)] += self.count_the_based(mess)

        #Confirm connection and members present
        print('Logged on as {0}!'.format(self.user))
        print(self.memberList)

    #Events that happen when a new message is sent in chat.
    async def on_message(self, message):
        #Retrieves the message sent and the author to print to the console for debugging.
        print('Message from {0.author}: {0.content}'.format(message))

        #Get the guild associated with the testing ID
        guild = client.get_guild(GUILD)

        self.memberScores[self.memberList.index(message.author)] += self.count_the_based(message)

        #Prints how often the author has said  "based", regardless of case.
        print('{0.author} now has a Based Count of: '.format(message), end = '')
        print(self.memberScores[self.memberList.index(message.author)])

        #COMMAND: Sends a message saying how many times a specific user said "based"
        if(message.content.startswith("*mycount")):
            #Finds the channel the message was sent to, triggers the "typing" indicater,
            #waits 1 second, and then responds with the author's Based Count.
            channel = message.channel
            await channel.trigger_typing()
            await asyncio.sleep(1)
            await channel.send(message.author.display_name + ": " + str(self.memberScores[self.memberList.index(message.author)]))
        
        #COMMAND: Sends a message saying how many times everyone in a Guild said "based"
        if(message.content.startswith("*servercount")):
            #Finds the channel the message was sent to, triggers the "typing" indicator, and waits a second
            channel = message.channel
            await asyncio.sleep(1)
            await channel.trigger_typing()

            #Once the coroutines are run, assembles a string holding every guild member's Based Count
            outgoing = ""
            for person in guild.members:
                outgoing = outgoing + person.display_name + ": " + str(self.memberScores[self.memberList.index(person)]) + "\n"

            #Sends the collectiive based count to the channel in a message.
            await channel.send(outgoing)

client = BasedCounter(intents = intents)
client.run(TOKEN)