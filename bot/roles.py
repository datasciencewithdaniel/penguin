from discord.ext import commands
from discord.utils import get
import unicodedata
import discord
from discord import RawReactionActionEvent
from bot import helpers

REACT_ID = 883340591742726194
WELCOME = 851074616947769354
BOT_ADMIN = 883346863326117888


class roles(commands.Cog):
    def __init__(self, bot, GUILD_ID, logger):
        self.bot = bot
        self.GUILD_ID = GUILD_ID
        self.logger = logger

    @commands.Cog.listener()
    async def on_ready(self):
        guild = discord.utils.get(self.bot.guilds, name=self.GUILD_ID)
        channel = self.bot.get_channel(WELCOME)

        message = await channel.fetch_message(channel.last_message_id)
        if message.id == REACT_ID:
            return False

        embed = discord.Embed(
            title="Reaction Roles",
            url="https://www.datasciencewithdaniel.com.au",
            description=f"""
                React to this messgage to get your roles!\n
                {helpers.find_emoji("SNAKE")} {get(guild.roles, name="Developer").mention} - if you want to write code and contribute to projects\n
                {helpers.find_emoji("OCTOPUS")} {get(guild.roles, name="Observer").mention} - if you are happy to watch and attend events to learn\n
                {helpers.find_emoji("PENGUIN")} {get(guild.roles, name="Bot-Admin").mention} - if you want to be part of managing the Penguin Bot\n
                """,
            color=0xB4E4F9,
        )
        message = await channel.send(embed=embed)

        await message.add_reaction(emoji=helpers.find_emoji("SNAKE"))
        await message.add_reaction(emoji=helpers.find_emoji("OCTOPUS"))
        await message.add_reaction(emoji=helpers.find_emoji("PENGUIN"))

    async def reaction_edits(self, payload, action="remove"):
        channel = self.bot.get_channel(payload.channel_id)
        if channel == self.bot.get_channel(BOT_ADMIN):
            pass  # CHECK IF STREAM IS HAPPENING
        if channel != self.bot.get_channel(WELCOME):
            return False

        if payload.message_id != REACT_ID:
            return False

        reactions = [
            "SNAKE",  # DEVELOPER
            "OCTOPUS",  # OBSERVER
            "PENGUIN",  # BOT-ADMIN
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
            role = get(guild.roles, name="Bot-Admin")

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
