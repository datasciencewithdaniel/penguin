from discord.ext import commands
import discord
from bot import helpers


class coder(commands.Cog):
    def __init__(self, bot, GUILD_ID, logger):
        self.bot = bot
        self.GUILD_ID = GUILD_ID
        self.logger = logger
        self.CODER_ID = 908749766995902504
        self.reactions = [
            "LARGE GREEN CIRCLE",
            "LARGE ORANGE CIRCLE",
            "LARGE RED CIRCLE",
        ]

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = self.bot.get_channel(self.CODER_ID)

        if (
            message.author.name in ["Penguin", "BabyPenguin"]
            or message.channel.id != self.CODER_ID
        ):
            return False

        content = "<@&908749408777158678>"

        challenge_embed = discord.Embed(
            title=f"New Challenge!",
            description=f"""
            {message.content}\n
            {helpers.find_emoji(self.reactions[0])} - I found this easy => Lets move on to the next one
            {helpers.find_emoji(self.reactions[1])} - I found this medium => I would like to discuss it
            {helpers.find_emoji(self.reactions[2])} - I found this hard => I need some more help to solve\n
            """,
            color=0xB4E4F9,
        )

        new_message = await channel.send(content=content, embed=challenge_embed)

        await message.delete()

        for emoji in self.reactions:
            await new_message.add_reaction(emoji=helpers.find_emoji(emoji))
