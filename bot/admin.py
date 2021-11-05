import discord
from discord.ext import commands


class admin(commands.Cog):
    def __init__(self, bot, GUILD_ID, logger):
        self.bot = bot
        self.GUILD_ID = GUILD_ID
        self.logger = logger

    @commands.Cog.listener()
    async def on_ready(self):
        guild = discord.utils.get(self.bot.guilds, name=self.GUILD_ID)
        text_list = [
            "|" + "-" * 104 + "|",
            f"| {str(self.bot.user):^102} |",
            f"| {guild.name:^102} |",
            f"| {guild.id:^102} |",
            "|" + "-" * 104 + "|",
            f"| {'User':^32} | {'Channel':^32} | {'Command':^32} |",
            "|" + "-" * 104 + "|",
        ]
        [print(t) for t in text_list]
        [self.logger.info(t) for t in text_list]
