from discord.ext import commands
import discord
import subprocess
import json
from bot import helpers


class github(commands.Cog):
    def __init__(self, bot, GUILD_ID, logger):
        self.bot = bot
        self.GUILD_ID = GUILD_ID
        self.logger = logger
        self.CHANNEL_ID = {
            908383304397512784: "beluga",
            908383378007547924: "penguin",
            908390460840624178: "datasciencewithdaniel",  # web
            # 908634903896272936: "space",
        }
        self.reactions = [
            "LARGE BLUE CIRCLE",
            "LARGE GREEN CIRCLE",
            "LARGE RED CIRCLE",
        ]

    @commands.command(
        name="issues",
        help="Checks the open issues for the given repo [*args]",
    )
    async def issues(self, ctx, args):
        channel = self.bot.get_channel(ctx.channel.id)
        if ctx.channel.id not in list(self.CHANNEL_ID.keys()):
            return False
        await ctx.message.delete()

        repo = self.CHANNEL_ID[ctx.channel.id] if not args else args
        command = f"""curl \
            -H "Accept: application/vnd.github.v3+json" \
            https://api.github.com/repos/datasciencewithdaniel/{repo}/issues
            """
        raw_issues = subprocess.run(
            command, shell=True, text=True, check=True, capture_output=True
        )
        raw_issues = json.loads(raw_issues.stdout)

        for ele in raw_issues[::-1]:
            if ele["state"] == "open":
                issue_embed = discord.Embed(
                    title=f"Open Issue #{ele['number']} - {ele['title']} [{ele['repository_url'].split('/')[-1]}]",
                    description=f"{ele['body']}",
                    color=0xB4E4F9,
                )
                await channel.send(embed=issue_embed)

        helpers.command_log(ctx, logger=self.logger)
