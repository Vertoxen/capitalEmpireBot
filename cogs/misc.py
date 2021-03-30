import discord
import asyncio
import json
import requests

from discord.ext import commands

reddit_icon = "<:reddit:808775167811256380>"

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ["meme"])
    async def memes(self, ctx):
        meme = requests.get("https://reddit-meme-api.herokuapp.com/memes/")
        memes = meme.json()

        em = discord.Embed(
            title = f'**{memes["title"]}**',
            url = f"{memes['post_link']}",
            color = discord.Colour.random()
        )

        em.set_image(url = memes['url'])
        em.set_footer(text = f"r/{memes['subreddit']} | Up-votes: {memes['ups']}")

        await ctx.send(embed=em)
        return

def setup(bot):
    bot.add_cog(Misc(bot))
    print("( / ) -- Misc is ready! -- ( / )")