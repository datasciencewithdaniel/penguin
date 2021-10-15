# from os import name
from discord.ext import commands
from bot import helpers


class responses(commands.Cog):
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger

    @commands.command(name="hi", help="Penguin is here to help")
    async def welcome(self, ctx):
        response = "Penguin is here, what can I help you with?"
        await ctx.send(response)
        helpers.command_log(
            ctx, logger=self.logger
        )  # What happens if you don't have a nickname?

    @commands.command(name="bye", help="Penguin is here to help")
    async def goodbye(self, ctx):
        response = "Until next time :)"
        await ctx.send(response)
        helpers.command_log(ctx, logger=self.logger)

    @commands.command(name="discord", help="Join us on Discord")
    async def discord(self, ctx):
        response = "Join us on Discord: https://discord.gg/D3KfXbdZgk"
        await ctx.send(response)
        helpers.command_log(ctx, logger=self.logger)

    @commands.command(name="projects", help="See our projects on GitHub")
    async def projects(self, ctx):
        response = "See our projects at: https://github.com/datasciencewithdaniel"
        await ctx.send(response)
        helpers.command_log(ctx, logger=self.logger)

    @commands.command(name="site", help="Check out our website")
    async def site(self, ctx):
        response = "Check out our website at: https://www.datasciencewithdaniel.com.au"
        await ctx.send(response)
        helpers.command_log(ctx, logger=self.logger)
