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
            "|" + "-" * 104 + "|\n"
            f"| {str(self.bot.user):^102} |\n"
            f"| {guild.name:^102} |\n"
            f"| {guild.id:^102} |\n"
            "|" + "-" * 104 + "|\n"
            f"| {'User':^32} | {'Channel':^32} | {'Command':^32} |\n"
            "|" + "-" * 104 + "|"
        )
