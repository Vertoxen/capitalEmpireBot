import discord
import motor.motor_asyncio
import threading
import json
import random
import asyncio
import DiscordUtils

from discord.ext import commands
from discord.ext.commands import BucketType
from motor.motor_asyncio import AsyncIOMotorClient

with open('/home/yaminahmed/Python/Captial-Empire/config.json') as fe:
    json_file = json.load(fe)

cluster = AsyncIOMotorClient(
    "mongodb://")
db = cluster['economy']
cursor = db["economy"]

FOOTERS = [f"Capital Empire v{json_file['version']}",
           f"Capital Empire v{json_file['version']}"]

cash_emoji = "<:cash:823714411444437053>"
gem_emoji = "<:gem:823716508395110401>"
tick_emoji = "<:tick_sign:800685194930552853>"
shop_emoji = "<:shop:827590803718144091>"
manager_emoji = "<:manager:827590850808774736>"

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        USER_ID = message.author.id

        resultCheck = await cursor.find_one({"user_id": USER_ID})

        if resultCheck is None:
            pass

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
                        description ="Operation cancelled due to **Invalid Reaction**! Please react with the emojis provided next time!",
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
                    return

    @commands.command(aliases = ["steal"])
    @commands.cooldown(1, 60, BucketType.user)
    async def rob(self, ctx, other: discord.Member = None):
        FOOTER = random.choice(FOOTERS)

        if other is None:
            em = discord.Embed(
                title="Error!",
                description="Please mention the user you are going to rob!",
                color=discord.Colour.red()
            )

            em.set_footer(text=FOOTER)

            await ctx.send(embed=em)
            return

        else:
            USER_ID = ctx.author.id
            OTHER_ID = other.id

            userResults = await cursor.find_one({"user_id": USER_ID})
            otherResults = await cursor.find_one({"user_id": OTHER_ID})

            userLevel = userResults['level']
            otherLevel = otherResults['level']

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

            if userLevel < 25:
                em = discord.Embed(
                    title = "Error!",
                    description = "You must be at-least in **Level 25** to be able to use this command!",
                    color = discord.Colour.red()
                )

                em.set_footer(text = FOOTER)

                await ctx.send(embed=em)
                return

            if otherLevel < 25:
                em = discord.Embed(
                    title = "Error!",
                    description = "Stop picking on weak prey and rob someone that is in **Level 25** or above!",
                    color = discord.Colour.red()
                )

                em.set_footer(text = FOOTER)

                await ctx.send(embed=em)
                return

            else:
                probability = random.randint(1, 10)

                if probability == 5:
                    userBal = userResults['balance']
                    otherBal = otherResults['balance']

                    addup = round(otherBal / 4.5)

                    userChange = userBal + addup
                    otherChange = otherBal - addup

                    await cursor.update_one({"user_id": USER_ID}, {"$set": {"balance": userChange}})
                    await cursor.update_one({"user_id": OTHER_ID}, {"$set": {"balance": otherChange}})

                    em = discord.Embed(
                        title = "Successful!",
                        description = f"You stole {cash_emoji} {addup} from **{other}**!",
                        color = discord.Colour.green()
                    )

                    em.set_footer(text = FOOTER)

                    await ctx.send(embed=em)
                    return

                else:
                    userBal = userResults['balance']
                    otherBal = otherResults['balance']

                    addup = round(otherBal / 15.5)

                    userChange = userBal - addup
                    otherChange = otherBal + addup

                    await cursor.update_one({"user_id": USER_ID}, {"$set": {"balance": userChange}})
                    await cursor.update_one({"user_id": OTHER_ID}, {"$set": {"balance": otherChange}})

                    em = discord.Embed(
                        title="Failed!",
                        description=f"You failed and had to pay **{other}** {cash_emoji} {addup} !",
                        color=discord.Colour.red()
                    )

                    em.set_footer(text=FOOTER)

                    await ctx.send(embed=em)
                    return

    @rob.error
    async def rob_error(self, ctx, error):
        FOOTER = random.choice(FOOTERS)

        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Error!",
                               description=f"Please wait `{error.retry_after:.2f}s` before executing this command again!",
                               color=0xff0040)

            em.set_footer(text=f"{FOOTER}")
            await ctx.send(embed=em)
            return

    @commands.command(aliases = ["store"])
    async def shop(self, ctx):
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
            emStart = discord.Embed(
                title = "Shop",
                color = discord.Colour.orange()
            )

            emStart.add_field(
                name = "Stores",
                value = f"React with {shop_emoji} to get the **Store** list!",
                inline = False
            )

            emStart.add_field(
                name = "Managers",
                value = f"React with {manager_emoji} to get the **Manager** list!",
                inline = False
            )

            emStart.set_footer(text = FOOTER)

            message = await ctx.send(embed=emStart)

            await message.add_reaction(shop_emoji)
            await message.add_reaction(manager_emoji)

            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=lambda reaction, user: user == ctx.author and reaction.message.channel == ctx.channel)

            except:
                pass

            else:
                if str(reaction.emoji) == shop_emoji:
                    em = discord.Embed(
                        title = "Store Shop!",
                        color = discord.Colour.green()
                    )

                    em.add_field(
                        name = "Lemon Stand",
                        value = f"`N/A`\n**Bought:** `{results['lemon-stand']}`\n**Earn:** `N/A`\n**Price:** `N/A`",
                        inline = False
                    )

                    em.add_field(
                        name = "Thrift Shop",
                        value = f"`ce!buy store thrift-shop`\n**Bought:** `{results['thrift-shop']}`\n**Earn:** {cash_emoji} `+{results['thrift-shop-earn']}`\n**Price:** {cash_emoji} `{results['thrift-shop-price']}`",
                        inline = False
                    )

                    em.add_field(
                        name = "Newspaper Company",
                        value = f"`ce!buy store newspaper-company`\n**Bought:** `{results['newspaper-company']}`\n**Earn:** {cash_emoji} `+{results['newspaper-company-earn']}`\n**Price:** {cash_emoji} `{results['newspaper-company-price']}`",
                        inline = False
                    )

                    em.add_field(
                        name = "Donut Shop",
                        value = f"`ce!buy store donut-shop`\n**Bought:** `{results['donut-shop']}`\n**Earn:** {cash_emoji} `+{results['donut-shop-earn']}`\n**Price:** {cash_emoji} `{results['donut-shop-price']}`",
                        inline = False
                    )

                    em.add_field(
                        name = "Retail Store",
                        value = f"`ce!buy store retail-store`\n**Bought:** `{results['retail-store']}`\n**Earn:** {cash_emoji} `+{results['retail-store-earn']}`\n**Price:** {cash_emoji} `{results['retail-store-price']}`",
                        inline = False
                    )

                    em.set_footer(text = FOOTER)

                    em2 = discord.Embed(
                        title = "Store Shop!",
                        color = discord.Colour.green()
                    )

                    em2.add_field(
                        name = "Fast Food Chain",
                        value = f"`ce!buy store fast-food-chain`\n**Bought:** `{results['fast-food-chain']}`\n**Earn:** {cash_emoji} `+{results['fast-food-chain-earn']}`\n**Price:** {cash_emoji} `{results['fast-food-chain-price']}`",
                        inline = False
                    )

                    em2.set_footer(text = FOOTER)

                    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx)

                    paginator.add_reaction('⏪', "back")
                    paginator.add_reaction('⏩', "next")

                    embeds = [em, em2]

                    await paginator.run(embeds)

                if str(reaction.emoji) == manager_emoji:
                    pass

                if str(reaction.emoji) == "⏪":
                    pass

                if str(reaction.emoji) == "⏩":
                    pass

                else:
                    em = discord.Embed(
                        title = "Error!",
                        description = "Operation cancelled due to **Invalid Reaction**! Please react with the emojis provided next time!",
                        color = discord.Colour.red()
                    )

                    em.set_footer(text = FOOTER)

                    await ctx.send(embed=em)
                    return

def setup(bot):
    bot.add_cog(Economy(bot))
    print("( / ) -- Economy is ready! -- ( / )")
