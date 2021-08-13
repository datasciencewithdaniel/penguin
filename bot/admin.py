import discord
from discord.ext import commands


class admin(commands.Cog):
    def __init__(self, bot, GUILD):
        self.bot = bot
        self.GUILD = GUILD

    @commands.Cog.listener()
    async def on_ready(self):
        guild = discord.utils.get(self.bot.guilds, name=self.GUILD)
        print(
            f"{self.bot.user} is connected to the following guild:\n"
            f"{guild.name} (id: {guild.id})"
        )
