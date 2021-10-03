import os
import discord
import pandas as pd

#Parses a specific channel and creates a table for a poker leaderboard

my_secret = os.environ['TOKEN']

client = discord.Client()
guild = discord.Guild


@client.event
async def on_message(message):

    chat = client.get_channel(840607256189861898)

    data = pd.DataFrame(columns=['Name', 'Chips'])
    data = data.append({'Name': "name", 'Chips': 10000.00}, ignore_index=True)

    #makes sure the command is not called by this bot
    if message.author == client.user:
        return
    #checks if the messages starts with _
    elif message.content.startswith('_'):

        #gets rid of the _
        cmd = message.content.split()[0].replace("_", "")

        #checks for command call
        if cmd == 'ldb':

            #reads all messages in history
            async for msg in chat.history(
                    limit=None) :  

                        #parses the string with " " as the delimitter
                        split = msg.content.split()

                        #makes sure split only splits into two
                        if (len(split) <= 1 or len(split) > 2):
                            temp = 0
                        else:
                            
                            #gets rid of asterisks if there in case message is bolded
                            name = msg.content.split()[0].replace("*", "")
                            temp = msg.content.split()[1].replace("*", "")

                        if (temp == 0):
                            #exits
                            temp = 0
                        #checks if we're adding or subtracting
                        elif (temp[0] == '+' or temp[0] == '-'):

                            i = 1
                            count = 0

                            while (i < len(temp)):

                                if (temp[i] < '0' or temp[i] > '9'):
                                    #checks for decimals
                                    if (temp[i] == '.' and count < 1):
                                        count = count + 1
                                    else:
                                        #exits
                                        temp = 0
                                        break

                                i = i + 1

                        else:
                            #exits
                            temp = 0

                        if (temp != 0):
                            if (temp[0] == '-'):
                                chips = float(temp)
                                #await message.channel.send(chips)

                            else:
                                chips = float(temp[1:])
                                #await message.channel.send(chips)

                            i = 0

                            #decides if the name already exists if it does aadds the chip value to said name in the dataframe
                            while (i < len(data)):
                                if (name == data.loc[i, "Name"]):
                                    data.loc[
                                        i,
                                        "Chips"] = data.loc[i, "Chips"] + chips
                                    break

                                i = i + 1

                            #creates a new name in the pandaframe and adds its chip count
                            if (i >= len(data)):
                                data = data.append(
                                    {
                                        'Name': name,
                                        'Chips': chips
                                    },
                                    ignore_index=True)

            #sort the pandaframe
            data.sort_values(by=['Chips'],
                             ignore_index=True,
                             inplace=True,
                             ascending=False)

            #print the dataframe
            await message.channel.send(data[1:])


client.run(os.getenv('TOKEN'))
