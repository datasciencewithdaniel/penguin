from discord.ext import commands
import unicodedata
import discord
from discord import RawReactionActionEvent
from bot import helpers


class todo(commands.Cog):
    def __init__(self, bot, GUILD_ID, logger):
        self.bot = bot
        self.GUILD_ID = GUILD_ID
        self.logger = logger
        self.TASK_ID = 908645656950894593
        self.TASK_LOG_ID = 908910662246359040
        self.reactions = {
            "LARGE BLUE CIRCLE": "In Progress",
            "LARGE GREEN CIRCLE": "Complete",
            "LARGE RED CIRCLE": "Cancelled",
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = self.bot.get_channel(self.TASK_ID)

        if (
            message.author.name in ["Penguin", "BabyPenguin"]
            or message.channel.id != self.TASK_ID
        ):
            return False

        challenge_embed = discord.Embed(
            title=f"New Task!",
            description=f"""
            {message.content}\n
            {helpers.find_emoji(list(self.reactions.keys())[0])} - {self.reactions[list(self.reactions.keys())[0]]}
            {helpers.find_emoji(list(self.reactions.keys())[1])} - {self.reactions[list(self.reactions.keys())[1]]}
            {helpers.find_emoji(list(self.reactions.keys())[2])} - {self.reactions[list(self.reactions.keys())[2]]}\n
            """,
            color=0xB4E4F9,
        )

        new_message = await channel.send(embed=challenge_embed)

        await message.delete()

        for emoji in self.reactions:
            await new_message.add_reaction(emoji=helpers.find_emoji(emoji))

    async def reaction_edits(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        if channel != self.bot.get_channel(self.TASK_ID):
            return False

        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        emoji = unicodedata.name(payload.emoji.name)
        message = await channel.fetch_message(payload.message_id)
        embed = message.embeds[0]
        embed.set_footer(text=f"{user.name}: {self.reactions[emoji]}")

        if user.name in ["Penguin", "BabyPenguin"] or emoji not in self.reactions:
            return False
        if emoji in list(self.reactions.keys())[1:]:
            log_channel = self.bot.get_channel(self.TASK_LOG_ID)
            await log_channel.send(embed=embed)
            await message.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        await self.reaction_edits(payload)
