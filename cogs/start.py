import discord
import motor.motor_asyncio
import threading
import json
import random
import asyncio

from discord.ext import commands

with open('/home/yaminahmed/Python/Captial-Empire/config.json') as fe:
    json_file = json.load(fe)

cluster = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb://")
db = cluster['economy']
cursor = db.economy

FOOTERS = [f"Capital Empire v{json_file['version']}",
           f"Capital Empire v{json_file['version']}"]


class Start(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create(self, ctx):
        USER_ID = ctx.author.id
        USER_NAME = str(ctx.author.name)
        USER_DISCRIMINATOR = str(ctx.author.discriminator)

        results = await cursor.find_one({"user_id": USER_ID})

        if results is None:
            FOOTER = random.choice(FOOTERS)

            ins = {"user_id": USER_ID, "user_name": USER_NAME, "user_discriminator": USER_DISCRIMINATOR, "money": json_file["money"],
                   "company-name": json_file["company-name"], "class": json_file["class"],
                   "earn": json_file["earn"], "earn-second": json_file["earn-second"],
                   "earn-multiplier": json_file["earn-multiplier"], "gems": json_file["gems"],
                   "rebirths": json_file["rebirths"], "exp": json_file["exp"],
                   "level": json_file["level"], "exp-limit": json_file["exp-limit"],
                   "exp-rate": json_file["exp-rate"], "isEarn": json_file["isEarn"],
                   "isVote": json_file["isVote"], "lemon-stand": json_file["lemon-stand"],
                   "lemon-stand-manager": json_file["lemon-stand-manager"], "lemon-stand-manager-price": json_file["lemon-stand-manager-price"],
                   "thrift-shop": json_file["thrift-shop"], "thrift-shop-price": json_file["thrift-shop-price"],
                   "thrift-shop-earn": json_file["thrift-shop-earn"], "thrift-shop-manager": json_file["thrift-shop-manager"],
                   "thrift-shop-manager-price": json_file["thrift-shop-manager-price"], "newspaper-company": json_file["newspaper-company"],
                   "newspaper-company-earn": json_file["newspaper-company-earn"], "newspaper-company-price": json_file["newspaper-company-price"],
                   "newspaper-company-manager": json_file["newspaper-company-manager"], "newspaper-company-manager-price": json_file["newspaper-company-manager-price"],
                   "donut-shop": json_file["donut-shop"], "donut-shop-price": json_file["donut-shop-price"], "donut-shop-earn": json_file["donut-shop-earn"],
                   "donut-shop-manager": json_file["donut-shop-manager"], "donut-shop-manager-price": json_file["donut-shop-manager-price"],
                   "retail-store": json_file["retail-store"], "retail-store-price": json_file["retail-store-price"], "retail-store-earn": json_file["retail-store-earn"],
                   "retail-store-manager": json_file["retail-store-manager"], "retail-store-manager-price": json_file["retail-store-manager-price"],
                   "fast-food-chain": json_file["fast-food-chain"], "fast-food-chain-price": json_file["fast-food-chain-price"], "fast-food-chain-earn": json_file["fast-food-chain-earn"],
                   "fast-food-chain-manager": json_file["fast-food-chain-manager"], "fast-food-chain-manager-price": json_file["fast-food-chain-manager-price"],
                   "earn-multiplier-price": json_file["earn-multiplier-price"]
                   }

            await cursor.insert_one(ins)

            emMain = discord.Embed(
                title="Company Name!",
                description="Please input in your company name!\n(Min. 2 Char) (Max. 12 Char)",
                color=discord.Color.orange()
            )

            emMain.set_footer(text=FOOTER)

            await ctx.send(embed=emMain)

            try:
                message = await self.bot.wait_for('message', check=lambda
                    message: message.author == ctx.author and message.channel == ctx.message.channel, timeout=15.0)

            except asyncio.TimeoutError:
                em = discord.Embed(
                    title="Error!",
                    description="Operation cancelled due to **Timeout**! Please be quicker next time!",
                    color=discord.Color.red()
                )

                em.set_footer(text=FOOTER)

                await ctx.send(embed=em)

                await cursor.delete_one({"user_id": USER_ID})
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

                    await cursor.delete_one({"user_id": USER_ID})
                    return

                if len(message.content) > 12:
                    em = discord.Embed(
                        title="Under 12 Characters please!",
                        description="Operation cancelled due to **Input Error**! Please follow the minimum requirements!",
                        color=discord.Colour.red()
                    )

                    em.set_footer(text=FOOTER)

                    await ctx.send(embed=em)

                    await cursor.delete_one({"user_id": USER_ID})
                    return

                else:
                    await cursor.update_one({"user_id": USER_ID}, {"$set": {"company-name": message.content}})

                    entrepreneur_emoji = "<:entrepreneur:823290572121833572>"
                    bargain_hunter_emoji = "<:bargain_hunter:823290705614733322>"
                    athlete_emoji = "<:athlete:823291947200413817>"

                    em = discord.Embed(
                        title="Class!",
                        description="Choose your class!\n`You cannot change this later on!`",
                        color=discord.Colour.orange()
                    )

                    em.add_field(
                        name=f"{entrepreneur_emoji} Entrepreneur",
                        value="Choose this class and you will start with 50% more earnings!",
                        inline=False
                    )

                    em.add_field(
                        name=f"{bargain_hunter_emoji} Bargain Hunter",
                        value="Choose this class and everything will be 10% off (Upgrades & Shop)",
                        inline=False
                    )

                    em.add_field(
                        name=f"{athlete_emoji} Athlete",
                        value="Choose this class and 50% of the time will be taken off in waiting for earnings!",
                        inline=False
                    )

                    em.set_footer(text=FOOTER)

                    sent = await ctx.send(embed=em)

                    await sent.add_reaction(entrepreneur_emoji)
                    await sent.add_reaction(bargain_hunter_emoji)
                    await sent.add_reaction(athlete_emoji)

                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=10, check=lambda reaction,
                                                                                                          user: user == ctx.author and reaction.message.channel == ctx.channel)

                    except asyncio.TimeoutError:
                        emError = discord.Embed(
                            title="Error!",
                            description="Operation cancelled due to **Timeout**! Please be quicker next time!",
                            color=discord.Colour.red()
                        )

                        emError.set_footer(text=FOOTER)

                        await ctx.send(embed=emError)

                        await cursor.delete_one({"user_id": USER_ID})
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

                            await cursor.delete_one({"user_id": USER_ID})
                            return

                        if str(reaction.emoji) == entrepreneur_emoji:
                            await cursor.update_one({"user_id": USER_ID}, {"$set": {"class": "Entrepreneur"}})
                            await cursor.update_one({"user_id": USER_ID}, {"$set": {"earn": 375}})

                            emb = discord.Embed(
                                title="Profile Created!",
                                description="Your profile has successfully been created!\n\nPlease do `ce!earn` to start earning money in the background!",
                                color=discord.Colour.green()
                            )

                            emb.set_footer(text=FOOTER)

                            await ctx.send(embed=emb)
                            return

                        if str(reaction.emoji) == bargain_hunter_emoji:
                            await cursor.update_one({"user_id": USER_ID}, {"$set": {"class": "Bargain-Hunter"}})

                            emb = discord.Embed(
                                title="Profile Created!",
                                description="Your profile has successfully been created!\n\nPlease do `ce!earn` to start earning money in the background!",
                                color=discord.Colour.green()
                            )

                            emb.set_footer(text=FOOTER)

                            await ctx.send(embed=emb)
                            return

                        if str(reaction.emoji) == athlete_emoji:
                            await cursor.update_one({"user_id": USER_ID}, {"$set": {"class": "Athlete"}})
                            await cursor.update_one({"user_id": USER_ID}, {"$set": {"earn-second": 5}})

                            emb = discord.Embed(
                                title="Profile Created!",
                                description="Your profile has successfully been created!\n\nPlease do `ce!earn` to start earning money in the background!",
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
