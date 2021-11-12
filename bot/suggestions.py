from discord.ext import commands
import unicodedata
import discord
from discord import RawReactionActionEvent
from collections.abc import Sequence
from bot import helpers


class suggestions(commands.Cog):
    def __init__(self, bot, GUILD_ID, logger):
        self.bot = bot
        self.GUILD_ID = GUILD_ID
        self.logger = logger
        self.SUGGEST_ID = 908640577640345631
        self.REQUEST_ID = 908652396786376734
        self.MESSAGE_ID = 908722060254138388
        self.reactions = ["LARGE GREEN CIRCLE", "LARGE RED CIRCLE"]

    @commands.command(
        name="update_suggestions",
        help="Updates the embed in the suggestions channel [new]",
    )
    @commands.has_role("Administrator")
    async def update_suggestions(self, ctx, arg):
        channel = self.bot.get_channel(self.SUGGEST_ID)

        suggest_title_embed = discord.Embed(
            color=0xB4E4F9,
        )
        suggest_title_embed.set_image(
            url="https://datasciencewithdaniel.com.au/images/Discord_Suggestions.png"
        )

        suggest_embed = discord.Embed(
            title="Open for suggestions and improvements",
            description=f"""
            Use this channel for your suggestion to improve Data Science with Daniel in some way!\n
            """,
            color=0xB4E4F9,
        )

        if arg == "new":
            await channel.send(embed=suggest_title_embed)
            message = await channel.send(embed=suggest_embed)
        else:
            message = await channel.fetch_message(self.MESSAGE_ID)
            await message.edit(embed=suggest_embed)

        self.MESSAGE_ID = message.id

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = self.bot.get_channel(self.SUGGEST_ID)

        if (
            message.author.name in ["Penguin", "BabyPenguin"]
            or message.channel.id != self.SUGGEST_ID
        ):
            return False

        new_suggest_embed = discord.Embed(
            title=f"New Suggestion from {message.author.name}!",
            description=f"""
            {message.content}\n
            {helpers.find_emoji(self.reactions[0])} - if you would like to accept this suggestion\n
            {helpers.find_emoji(self.reactions[1])} - if you would like to decline this suggestion\n
            """,
            color=0xB4E4F9,
        )
        new_suggest_embed.set_footer(text=message.author.id)

        channel = self.bot.get_channel(self.REQUEST_ID)
        new_message = await channel.send(embed=new_suggest_embed)

        await message.delete()
        await message.author.create_dm()
        await message.author.dm_channel.send(
            f"Hi {message.author.name}, your suggestion {message.content} has been received succesfully!"
        )

        for emoji in self.reactions:
            await new_message.add_reaction(emoji=helpers.find_emoji(emoji))

    async def reaction_edits(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        if channel != self.bot.get_channel(self.REQUEST_ID):
            return False

        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        emoji = unicodedata.name(payload.emoji.name)
        message = await channel.fetch_message(payload.message_id)
        author = guild.get_member(int(message.embeds[0].footer.text))

        if user.name in ["Penguin", "BabyPenguin"] or emoji not in self.reactions:
            return False
        if emoji == "LARGE GREEN CIRCLE":
            await author.create_dm()
            await author.dm_channel.send(
                f"Hi {message.author.name}, your suggestion {message.content} has been accepted!\nPlease follow up with {user.name} for more information"
            )
        elif emoji == "LARGE RED CIRCLE":
            await author.create_dm()
            await author.dm_channel.send(
                f"Hi {message.author.name}, sorry your suggestion {message.content} has been declined.\nPlease follow up with {user.name} for more information"
            )

        await message.clear_reactions()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        await self.reaction_edits(payload)
