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


class Start(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # thread = threading.Thread(target=await self.start)
        # thread.start()

        print("Placeholder...")

    @commands.command()
    async def create(self, ctx):
        USER_ID = ctx.author.id
        USER_NAME = str(ctx.author)

        results = cursor.find_one({"user_id": USER_ID})

        if USER_ID not in results:
            FOOTER = random.choice(FOOTERS)

            ins = {"user_id": USER_ID, "user_name": USER_NAME, "balance": json_file["balance"],
                   "company-name": json_file["company-name"], "class": json_file["class"],
                   "earn": json_file["earn"], "earn-second": json_file["earn-second"],
                   "earn-multiplier": json_file["earn-multiplier"], "gems": json_file["gems"],
                   "rebirths": json_file["rebirths"]}

            cursor.insert_one(ins)

            emMain = discord.Embed(
                title="Company Name!",
                description="Please input in your company name! (Min. 2 Char) (Max. 12 Char)",
                color=discord.Color.orange()
            )

            emMain.set_footer(text=FOOTER)

            await ctx.send(embed=emMain)

            try:
                message = None
                message = await self.bot.wait_for('message', check=lambda
                    m: m.author == ctx.author and m.channel == ctx.author.dm_channel, timeout=15.0)

            except asyncio.TimeoutError:
                em = discord.Embed(
                    title="Error!",
                    description="Operation cancelled due to **Timeout**! Please be quicker next time!",
                    color=discord.Color.red()
                )

                em.set_footer(text=FOOTER)

                await ctx.send(embed=em)

                cursor.delete_one({"user_id": USER_ID})
                return

            else:
                if len(message.content) < 2:
                    em = discord.Embed(
                        title="Over 2 Characters please!",
                        description="Operation cancelled due to **Input Error**! Please follow the minimum requirements!",
                        color=discord.Colour.red()
                    )

                    em.set_footer(text=FOOTER)

                    await ctx.send(embed=em)

                    cursor.delete_one({"user_id": USER_ID})
                    return

                if len(message.content) > 12:
                    em = discord.Embed(
                        title="Under 12 Characters please!",
                        description="Operation cancelled due to **Input Error**! Please follow the minimum requirements!",
                        color=discord.Colour.red()
                    )

                    em.set_footer(text=FOOTER)

                    await ctx.send(embed=em)

                    cursor.delete_one({"user_id": USER_ID})
                    return

                else:
                    cursor.update_one({"user_id": USER_ID}, {"$set": {"company-name": message.content}})

                    entrepreneur_emoji = "<:entrepreneur:823290572121833572>"
                    bargain_hunter_emoji = "<:bargain_hunter:823290705614733322>"
                    athlete_emoji = "<:athlete:823291947200413817>"

                    em = discord.Embed(
                        title="Class!",
                        description="Choose your class! (You cannot change this later on!)",
                        color=discord.Colour.orange()
                    )

                    em.add_field(
                        name=f"{entrepreneur_emoji} Entrepreneur",
                        value="Choose this class and you will get 50% more earnings!",
                        inline=True
                    )

                    em.add_field(
                        name=f"{bargain_hunter_emoji} Bargain Hunter",
                        value="Choose this class and everything will be 50% off (Upgrades & Shop)",
                        inline=True
                    )

                    em.add_field(
                        name=f"{athlete_emoji} Athlete",
                        value="Choose this class and 50% of the time will be taken off in waiting for earnings!",
                        inline=True
                    )

                    em.set_footer(text=FOOTER)

                    sent = await ctx.send(embed=em)

                    sent.add_reaction(entrepreneur_emoji)
                    sent.add_reaction(bargain_hunter_emoji)
                    sent.add_reaction(athlete_emoji)

                    try:
                        reaction, member = None
                        reaction, member = await self.bot.wait_for('reaction_add', timeout=10.0, check=lambda reaction,
                                                                                                              user: user == member and reaction.message.channel == ctx.channel)

                    except asyncio.TimeoutError:
                        emError = discord.Embed(
                            title="Error!",
                            description="Operation cancelled due to **Timeout**! Please be quicker next time!",
                            color=discord.Colour.red()
                        )

                        emError.set_footer(text=FOOTER)

                        await ctx.send(embed=emError)

                        cursor.delete({"user_id": USER_ID})
                        return

                    else:
                        if str(reaction.emoji) not in [entrepreneur_emoji, bargain_hunter_emoji, athlete_emoji]:
                            emError = discord.Embed(
                                title="Error!",
                                description="Operation cancelled due to **Invalid Reaction**! Please react with the emojis provided next time!",
                                color=discord.colour.red()
                            )

                            emError.set_footer(text=FOOTER)

                            await ctx.send(embed=emError)

                            cursor.delete({"user_id": USER_ID})
                            return

                        if str(reaction.emoji) == entrepreneur_emoji:
                            cursor.update_one({"user_id": USER_ID}, {"$set": {"class": "Entrepreneur"}})

                            emb = discord.Embed(
                                title="Profile Created!",
                                description="Your profile has successfully been created!",
                                color=discord.Colour.green()
                            )

                            emb.set_footer(text=FOOTER)

                            await ctx.send(embed=emb)
                            return

                        if str(reaction.emoji) == bargain_hunter_emoji:
                            cursor.update_one({"user_id": USER_ID}, {"$set": {"class": "Bargain-Hunter"}})

                            emb = discord.Embed(
                                title="Profile Created!",
                                description="Your profile has successfully been created!",
                                color=discord.Colour.green()
                            )

                            emb.set_footer(text=FOOTER)

                            await ctx.send(embed=emb)
                            return

                        if str(reaction.emoji) == athlete_emoji:
                            cursor.update_one({"user_id": USER_ID}, {"$set": {"class": "Athlete"}})

                            emb = discord.Embed(
                                title="Profile Created!",
                                description="Your profile has successfully been created!",
                                color=discord.Colour.green()
                            )

                            emb.set_footer(text=FOOTER)

                            await ctx.send(embed=emb)
                            return

                        else:
                            emError = discord.Embed(
                                title="Error!",
                                description="An unknown error has occured! Please try again!",
                                color=discord.Colour.red()
                            )

                            emError.set_footer(text=FOOTER)

                            await ctx.send(embed=emError)
                            return

        else:
            FOOTER = random.choice(FOOTERS)

            em = discord.Embed(
                title="Error!",
                description="You already have an existing profile!",
                color=discord.Colour.red()
            )

            em.set_footer(text=FOOTER)

            await ctx.send(embed=em)
            return


def setup(bot):
    bot.add_cog(Start(bot))
    print("( / ) -- Start is ready! -- ( / )")