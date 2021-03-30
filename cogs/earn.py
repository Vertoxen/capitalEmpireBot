import discord
import motor.motor_asyncio
import threading
import json
import random
import asyncio

from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient

with open('/home/yaminahmed/Python/Captial-Empire/config.json') as fe:
    json_file = json.load(fe)

cluster = AsyncIOMotorClient(
    "mongodb://vertoxen:omegamemes567@de1.centronodes.com:25930/?authMechanism=DEFAULT&authSource=economy&retryWrites=true&w=majority"
    )
db = cluster['economy']
cursor = db["economy"]

FOOTERS = [f"Capital Empire v{json_file['version']}",
           f"Capital Empire v{json_file['version']}"]

class Earn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def earn(self, ctx):
        USER_ID = ctx.author.id

        resultCheck = await cursor.find_one({"user_id": USER_ID})

        if resultCheck is None:
            FOOTER = random.choice(FOOTERS)

            em = discord.Embed(
                title="Error!",
                description="You do not have an existing profile!\n\nTry doing `ce!create`!",
                color=discord.Colour.red()
            )

            em.set_footer(text=FOOTER)

            await ctx.send(embed=em)
            return

        else:
            results = await cursor.find_one({"user_id": USER_ID})

            isEarn = results["isEarn"]

            FOOTER = random.choice(FOOTERS)

            if isEarn == "True":
                em = discord.Embed(
                    title="Error!",
                    description="You are already earning coins!",
                    color=discord.Colour.red()
                )

                em.set_footer(text=FOOTER)

                await ctx.send(embed=em)
                await asyncio.sleep(5)
                await cursor.update_one({"user_id": USER_ID}, {"$set": {"isEarn": "False"}})
                return

            if isEarn == "False":
                em = discord.Embed(
                    title="Successful!",
                    description="You are now earning money!\n\n`You can now AFK if you need to!`",
                    color=discord.Colour.green()
                )

                em.set_footer(text=FOOTER)

                await ctx.send(embed=em)

                while True:
                    results = await cursor.find_one({"user_id": USER_ID})

                    exp = results["exp"]
                    exp_limit = results["exp-limit"]

                    if exp >= exp_limit:
                        results = await cursor.find_one({"user_id": USER_ID})

                        newLevel = results["level"] + 1

                        await cursor.update_one({"user_id": USER_ID}, {"$set": {"level": newLevel}})
                        await cursor.update_one({"user_id": USER_ID}, {"$set": {"exp": 0}})

                        newExpLimit = round(exp_limit * 2.5)
                        newGems = results["gems"] + 10

                        await cursor.update_one({"user_id": USER_ID}, {"$set": {"exp-limit": newExpLimit}})
                        await cursor.update_one({"user_id": USER_ID}, {"$set": {"gems": newGems}})
                        pass

                    newMoney = results["money"] + results["earn"]
                    newExp = results["exp"] + results["exp-rate"]

                    await cursor.update_one({"user_id": USER_ID}, {"$set": {"money": newMoney}})
                    await cursor.update_one({"user_id": USER_ID}, {"$set": {"exp": newExp}})

                    seconds = results["earn-second"]

                    await asyncio.sleep(seconds)
                    await cursor.update_one({"user_id": USER_ID}, {"$set": {"isEarn": "True"}})

def setup(bot):
    bot.add_cog(Earn(bot))
    print("( / ) -- Earn is ready! -- ( / )")