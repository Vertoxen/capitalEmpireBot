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
    "mongodb://vertoxen:omegamemes567@de1.centronodes.com:25930/?authMechanism=DEFAULT&authSource=economy&retryWrites=true&w=majority")
db = cluster['economy']
cursor = db["economy"]

FOOTERS = [f"Capital Empire v{json_file['version']}",
           f"Capital Empire v{json_file['version']}"]

cash_emoji = "<:cash:823714411444437053>"
gem_emoji = "<:gem:823716508395110401>"
tick_emoji = "<:tick_sign:800685194930552853>"

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        USER_ID = message.author.id

        resultCheck = await cursor.find_one({"user_id": USER_ID})

        if resultCheck is None:
            return

        else:
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

            else:
                return

    @commands.command(aliases=["bal"])
    async def balance(self, ctx):
        USER_ID = ctx.author.id
        FOOTER = random.choice(FOOTERS)

        results = await cursor.find_one({"user_id": USER_ID})

        if results is None:
            em = discord.Embed(
                title="Error!",
                description="You do not have an existing profile!\n\nTry doing `ce!create`!",
                color=discord.Colour.red()
            )

            em.set_footer(text=FOOTER)

            await ctx.send(embed=em)
            return

        else:
            em = discord.Embed(
                title = f"{ctx.author.name}'s Balance!",
                color = discord.Colour.random()
            )

            em.add_field(
                name = "Balance",
                value = f"{cash_emoji} {results['money']}",
                inline = False
            )

            em.add_field(
                name = "Gems",
                value = f"{gem_emoji} {results['gems']}",
                inline = False
            )

            em.set_thumbnail(url = ctx.author.avatar_url)
            em.set_footer(text = FOOTER)

            await ctx.send(embed=em)
            return

    @commands.command(aliases = ["prof", "pr", "p"])
    async def profile(self, ctx):
        USER_ID = ctx.author.id
        FOOTER = random.choice(FOOTERS)

        results = await cursor.find_one({"user_id": USER_ID})

        if results is None:
            em = discord.Embed(
                title="Error!",
                description="You do not have an existing profile!\n\nTry doing `ce!create`!",
                color=0xffffff
            )

            em.set_footer(text=FOOTER)

            await ctx.send(embed=em)
            return

        else:
            em = discord.Embed(
                title = f"Profile",
                color = discord.Colour.random()
            )

            em.add_field(
                name = "Username",
                value = f"{ctx.author}",
                inline = False
            )

            em.add_field(
                name = "Class",
                value = f"{results['class']}",
                inline = False
            )

            em.add_field(
                name = "Company Name",
                value = f"`{results['company-name']}`",
                inline = False
            )

            em.add_field(
                name = "Balance",
                value = f"{cash_emoji} {results['money']}",
                inline = False
            )

            em.add_field(
                name = "Gems",
                value = f"{gem_emoji} {results['gems']}",
                inline = False
            )

            em.add_field(
                name = "Level",
                value = f"{results['level']}",
                inline = False
            )

            em.add_field(
                name = "EXP",
                value = f"{results['exp']} / {results['exp-limit']}",
                inline  = False
            )

            em.add_field(
                name = "Rebirths",
                value = f"{results['rebirths']}",
                inline = False
            )

            em.add_field(
                name = "Multiplier",
                value = f"`{results['earn-multiplier']}x`",
                inline = False
            )

            em.set_thumbnail(url = ctx.author.avatar_url)
            em.set_footer(text = FOOTER)

            await ctx.send(embed=em)
            return

    @commands.command(aliases = ["up"])
    async def upgrade(self, ctx):
        USER_ID = ctx.author.id
        FOOTER = random.choice(FOOTERS)

        results = await cursor.find_one({"user_id": USER_ID})

        if results is None:
            em = discord.Embed(
                title="Error!",
                description="You do not have an existing profile!\n\nTry doing `ce!create`!",
                color=discord.Colour.red()
            )

            em.set_footer(text=FOOTER)

            await ctx.send(embed=em)
            return

        else:
            em = discord.Embed(
                title = "Upgrade",
                description = f"Current multiplier is `{results['earn-multiplier']}x`",
                color = discord.Colour.orange()
            )

            em.add_field(
                name = "Next Upgrade", value = f"**Costs** {gem_emoji} {results['earn-multiplier-price']}\n\nPlease react with {tick_emoji} to upgrade your multiplier!"
            )

            em.set_footer(text = FOOTER)

            message = await ctx.send(embed = em)
            await message.add_reaction(tick_emoji)

            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=lambda reaction, user: user == ctx.author and reaction.message.channel == ctx.channel)

            except Exception as e:
                print(e)

            else:
                if str(reaction.emoji) == tick_emoji:
                    getUserID = ctx.guild.get_member(USER_ID)
                    results = await cursor.find_one({"user_id": USER_ID})

                    await message.remove_reaction(tick_emoji, getUserID)

                    result_userGems = results["gems"]
                    result_userMultiPrice = results["earn-multiplier-price"]
                    result_userMulti = results["earn-multiplier"]

                    if result_userGems < result_userMultiPrice:
                        embError = discord.Embed(
                            title = "Error!",
                            description = "You don't have enough gems to upgrade your multiplier!",
                            color = discord.Colour.red()
                        )

                        embError.set_footer(text = FOOTER)

                        await ctx.send(embed=embError)

                    else:
                        addup = result_userGems - result_userMultiPrice
                        addupMulti = result_userMulti + 1
                        addupTimes = result_userMultiPrice * 5

                        await cursor.update_one({"user_id": USER_ID}, {"$set": {"gems": addup}})
                        await cursor.update_one({"user_id": USER_ID}, {"$set": {"earn-multiplier": addupMulti}})
                        await cursor.update_one({"user_id": USER_ID}, {"$set": {"earn-multiplier-price": addupTimes}})

                        resultsNew = await cursor.find_one({"user_id": USER_ID})

                        emb = discord.Embed(
                            title = "Successful!",
                            description = "You have upgraded your multiplier by `+1`!",
                            color = discord.Colour.green()
                        )

                        emb.add_field(
                            name = "Multiplier",
                            value = f"`{resultsNew['earn-multiplier']}x`",
                            inline = False
                        )

                        emb.add_field(
                            name = "Next Price",
                            value = f"{gem_emoji} {resultsNew['earn-multiplier-price']}",
                            inline = False
                        )

                        emb.set_footer(text = FOOTER)

                        await ctx.send(embed=em)


                else:
                    emError = discord.Embed(
                        title = "Error!",
                        description =" Operation cancelled due to **Invalid Reaction**! Please react with the emojis provided next time!",
                        color = discord.Colour.red()
                    )

                    emError.set_footer(text=FOOTER)

                    await ctx.send(embed=emError)

                    return

    @commands.command(aliases = ["give", "transfer"])
    async def pay(self, ctx, other: discord.Member = None, amount: int = None):
        FOOTER = random.choice(FOOTERS)

        if other is None:
            em = discord.Embed(
                title = "Error!",
                description = "Please mention the user you are going to pay!",
                color = discord.Colour.red()
            )

            em.set_footer(text = FOOTER)

            await ctx.send(embed=em)
            return

        if amount is None:
            em = discord.Embed(
                title = "Error!",
                description = "Please mention how much you are going to pay to the user!",
                color = discord.Colour.red()
            )

            em.set_footer(text = FOOTER)

            await ctx.send(embed=em)
            return

        else:
            USER_ID = ctx.author.id
            OTHER_ID = other.id

            levelCap = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]

            userResults = await cursor.find_one({"user_id": USER_ID})
            otherResults = await cursor.find_one({"user_id": OTHER_ID})

            userLevel = userResults['level']
            otherLevel = otherResults['level']

            levelGap = userLevel - otherLevel

            if userResults is None:
                em = discord.Embed(
                    title="Error!",
                    description="You do not have an existing profile!\n\nTry doing `ce!create`!",
                    color=discord.Colour.red()
                )

                em.set_footer(text=FOOTER)

                await ctx.send(embed=em)
                return

            if otherResults is None:
                em = discord.Embed(
                    title="Error!",
                    description="The user you are trying to pay does not have an existing profile!",
                    color=discord.Colour.red()
                )

                em.set_footer(text=FOOTER)

                await ctx.send(embed=em)
                return

            if levelGap not in levelCap:
                if levelGap < 0:
                    em = discord.Embed(
                        title = "Error!",
                        description = "The user you are trying to pay has a much higher level than you!",
                        color = discord.Colour.red()
                    )

                    em.set_footer(text = FOOTER)

                    await ctx.send(embed=em)
                    return

                else:
                    em = discord.Embed(
                        title = "Error!",
                        description = "The user you are trying to pay has a much lower level than you!",
                        color = discord.Colour.red()
                    )

                    em.set_footer(text = FOOTER)

                    await ctx.send(embed=em)
                    return

            else:
                userBal = userResults['balance']
                otherBal = otherResults['balance']

                if userBal < amount:
                    em = discord.Embed(
                        title = "Error!",
                        description = "You are trying to give more money than you already have!",
                        color = discord.Colour.red()
                    )

                    em.set_footer(text = FOOTER)

                    await ctx.send(embed=em)
                    return

                else:
                    remove = userBal - amount
                    addup = otherBal + amount

                    await cursor.update_one({"user_id": USER_ID}, {"$set": {"balance": remove}})
                    await cursor.update_one({"user_id": OTHER_ID}, {"$set": {"balance": addup}})

                    em = discord.Embed(
                        title = "Successful!",
                        description = f"You have paid **{other}** {cash_emoji} {amount} !",
                        color = discord.Colour.green()
                    )

                    em.set_footer(text = FOOTER)

                    await ctx.send(embed=em)
                    return\

def setup(bot):
    bot.add_cog(Economy(bot))
    print("( / ) -- Economy is ready! -- ( / )")
