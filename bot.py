# bot.py
# type: ignore
import os
import discord
import scraper
from dotenv import load_dotenv
import datetime
from discord.ext import tasks, commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    check_alive.start()
    get_data.start()

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    if message.content == 'ping':
        await message.channel.send('pong')

@tasks.loop(seconds=15)
async def get_data():
    data = {"Finals": "https://www.globalinterpark.com/product/23010160?lang=en", "Semi-Finals": "https://www.globalinterpark.com/product/23009895?lang=en"}

    for event, url in data.items():
        channel = bot.get_channel(1166414794639822918)  # Replace with the actual channel ID
        ticket_data = scraper.getTickets(url)  # Call your scraper function

        if ticket_data[0]:
            await channel.send(f"{event} Tickets Available. Link: <{url}>. @everyone")
            await channel.send(scraper.printTicket(ticket_data[1]))
        else:
            print(f"{datetime.datetime.now()} {ticket_data[1]}")

@tasks.loop(hours=1)
async def check_alive():
    channel = bot.get_channel(1166414794639822918)
    await channel.send("I'm alive. Kelly is still a clown :clown:")

@check_alive.before_loop
async def before_check_alive():
    await bot.wait_until_ready()

@get_data.before_loop
async def before_get_data():
    await bot.wait_until_ready()

bot.run(TOKEN)
