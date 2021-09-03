from discord.ext import commands


class notifications(commands.Cog):
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f"Hi {member.name}, welcome to Data Science with Daniel!"
        )
        self.logger.info("{member} has joined Data Science with Daniel")
