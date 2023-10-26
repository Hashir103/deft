# bot.py
# type: ignore
import discord
import os
import scraper
import asyncio
from dotenv import load_dotenv
import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

        channel = self.get_channel(1166414794639822918)  # channel ID goes here
        await channel.send("I'm alive")

    async def my_background_task(self):
        await self.wait_until_ready()
        l = {"Finals":"https://www.globalinterpark.com/product/23010160?lang=en", "Semi-Finals":"https://www.globalinterpark.com/product/23009895?lang=en"}
        channel = self.get_channel(1166414794639822918)  # channel ID goes here
        while not self.is_closed():
            for event in l:
                url = l[event]
                data = await scraper.getTickets(url)  # Call your scraper function

                if datetime.datetime.now().minute == 42:
                    await channel.send(f"Still alive, and Kelly is still a clown :clown:")
                if data[0]:
                    info = await scraper.printTicket(data[1])
                    message = f"{event} Tickets Available. Link: <{url}>. @everyone\n {info}"
                    await channel.send(message)
                else:
                    print(str(datetime.datetime.now()) + " "  + str(data[1]))
            await asyncio.sleep(10)  # task runs every 60 seconds

client = MyClient(intents=discord.Intents.default())
client.run(TOKEN)