import discord
import os
from dotenv import load_dotenv
import sqlite3
import re

con = sqlite3.connect('charlie.db')
cur = con.cursor()

if(not cur.execute('SELECT name from sqlite_master WHERE type = \'table\' AND name = \'{player_data}\'')):
    cur.execute('CREATE TABLE player_data (id, name, guild, balance, exp)') #create table
    con.commit()
    print("Table created")
else:
    print("Table player_data already exists")

#loads in our Token from our .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents = intents)

#Basic python function
def contains(arr, item):
    for i in range(len(arr)):
        if arr[i].lower() == item:
            return True

#Discord events must be started with @client.event
#Discord event commands and events are couruntine functions and must start with async
#on_ready() runs on bot startup (aka when you run this file)
@client.event
async def on_ready():
    for guild in client.guilds:
        print(f'Charlie is connected to {guild.name}')
        for member in guild.members:
            cur.execute(f'SELECT id FROM player_data WHERE id = "{member.id}" AND guild = "{guild}"')
            data = cur.fetchall()
            if(len(data) == 0):
                #add new member to the database with starting balance of 50
                print(f'Adding {member.name} to player_data')
                cur.execute(f'INSERT INTO player_data VALUES ("{member.id}", "{member.name}", "{guild}", {50}, {0})')
            else:
                print("user already in database")
    con.commit()

@client.event
async def on_guild_join(guild):
    for member in guild.members:
        print(f'Member: {member}')

#on_message will check every message sent and trigger when a condition is met
@client.event
async def on_message(message):
    if message.content.lower() == "How are you Charlie?".lower():
        #sending messages require you to include "await" to wait for the bot to be done with any existing processes before running your code
        await message.channel.send("I'm a happy dino!")

    msg_length = re.sub(":.:")
#running the bot using our unique bot Token
client.run(TOKEN)