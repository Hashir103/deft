# bot.py
# type: ignore
import os
import discord
import scraper
import asyncio
from dotenv import load_dotenv
import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

async def get_data(l: dict):
    while True:
        for event in l:
            url = l[event]
            data = scraper.getTickets(url)  # Call your scraper function
            channel = client.get_channel(1166414794639822918)  # Replace with the actual channel ID
            if data[0]:
                await channel.send(f"{event} Tickets Available. Link: <{url}>. @everyone")
                await channel.send(scraper.printTicket(data[1]))
            else:
                print(str(datetime.datetime.now()) + " "  + str(data[1]))
        await asyncio.sleep(10)  # Sleep for 5 minutes (300 seconds)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    await get_data({"Finals":"https://www.globalinterpark.com/product/23010160?lang=en", "Semi-Finals":"https://www.globalinterpark.com/product/23009895?lang=en"})  # Start the background task

client.run(TOKEN)