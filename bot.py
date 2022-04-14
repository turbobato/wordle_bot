#!/usr/bin/env python3
# Import the os module.
import asyncio
import os
# Import load_dotenv function from dotenv module.
from dotenv import load_dotenv
# Loads the .env file that resides on the same level as the script.
load_dotenv()
# Grab the API token from the .env file.
import discord
from discord.ext import tasks, commands
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()

phrase_list = ["Points", "Samuel <3", "h. <3<3", "road to top1", "#PandouEnSueur"]

async def my_background_task():
    await client.wait_until_ready()
    counter = 0
    channel = client.get_channel(id=835769646597668874) # replace with channel_id
    while not client.is_closed():
        counter = (counter + 1) % 5
        await channel.send(phrase_list[counter])
        await asyncio.sleep(60) # task runs every 60 seconds

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.loop.create_task(my_background_task())

client.run(os.getenv("DISCORD_TOKEN"), bot = False)