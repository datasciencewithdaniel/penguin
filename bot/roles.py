from discord.ext import commands
from discord.utils import get


class roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(851436058172194851)
        message = await channel.send("test reaction roles")
        await message.add_reaction(emoji="🏃")
        await message.add_reaction(emoji="👍")
        await message.add_reaction(emoji="😀")
        await message.add_reaction(emoji="\U0001F970")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        channel = self.bot.get_channel(851436058172194851)
        # print(reaction.message.author.name)
        # if reaction.message.channel.id != channel:
        #     return False
        if reaction.emoji == "🏃":
            role = get(user.guild.roles, name="bot-testing")
        await user.add_roles(role)
