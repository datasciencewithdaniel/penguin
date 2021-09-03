from discord.ext import commands
from discord.utils import get
import unicodedata
from discord import RawReactionActionEvent
from bot import helpers


class roles(commands.Cog):
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(851436058172194851)
        message = await channel.send("test reaction roles")
        await message.add_reaction(emoji=helpers.find_emoji("SNAKE"))
        await message.add_reaction(emoji=helpers.find_emoji("OCTOPUS"))
        await message.add_reaction(emoji=helpers.find_emoji("PENGUIN"))
        await message.add_reaction(emoji=helpers.find_emoji("SPOUTING WHALE"))

    async def reaction_edits(self, payload, action="remove"):
        channel = self.bot.get_channel(
            payload.channel_id
        )  # IMPORTANT - WELCOME CHANNEL ONLY

        # https://discord.com/channels/851059417562742854/851074616947769354/851452116799062026
        if channel != self.bot.get_channel(851074616947769354):
            return False

        reactions = [
            "SNAKE",  # DEVELOPER
            "OCTOPUS",  # OBSERVER
            "PENGUIN",
            "SPOUTING WHALE",
            "MAMMOTH",
        ]

        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        emoji = unicodedata.name(payload.emoji.name)

        if user.name == "Penguin" or emoji not in reactions:
            return False
        if emoji == "SNAKE":
            role = get(guild.roles, name="Developer")
        elif emoji == "OCTOPUS":
            role = get(guild.roles, name="Observer")
        elif emoji == "PENGUIN":
            role = get(guild.roles, name="bot-testing")

        helpers.role_log(
            user, payload.emoji, channel, role, payload.event_type, logger=self.logger
        )

        if action == "add":
            await user.add_roles(role)
        else:
            await user.remove_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        await self.reaction_edits(payload, "add")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        await self.reaction_edits(payload)
