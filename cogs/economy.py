import discord
import motor.motor_asyncio
import threading
import json
import random
import asyncio

from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient

with open('/home/yaminahmed/Python/Captial-Empire/config.json') as f:
    json_file = json.load(f)

cluster = AsyncIOMotorClient(
    "mongodb+srv://test:omegamemes567@testcluster.tme6j.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster['test']
cursor = db["test"]

FOOTERS = [f"Rebirths will make you more money! | Capital Empire v{json_file['version']}",
           f"Don't forget to advertise the bot! | Capital Empire v{json_file['version']}",
           f"Use ce!help for the list of commands! | Capital Empire v{json_file['version']}"]


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # thread = threading.Thread(target=await self.start)
        # thread.start()

        print("Placeholder...")

def setup(bot):
    bot.add_cog(Economy(bot))
    print("( / ) -- Economy is ready! -- ( / )")
