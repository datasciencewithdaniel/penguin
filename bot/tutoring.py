import asyncio
import boto3
from boto3.dynamodb.conditions import Attr
import unicodedata
import discord
from discord.ext import commands
from discord import RawReactionActionEvent
from discord.utils import get
from bot import helpers

YES = "LARGE GREEN CIRCLE"
NO = "LARGE RED CIRCLE"


class tutoring(commands.Cog):
    def __init__(self, bot, GUILD, logger):
        self.bot = bot
        self.GUILD = GUILD
        self.logger = logger
        self.session = boto3.session.Session(profile_name="dswd")
        self.resource = self.session.resource("dynamodb")
        self.tablename = "tutoring-dev"
        self.table = self.resource.Table(self.tablename)
        self.languages = ["Python", "SQL", "Java", "JavaScript"]
        self.tutoring_channel_raw = 890976909054320681
        self.tutor_admin_channel_raw = 895262367112384522

    @commands.Cog.listener()
    async def on_ready(self):
        self.tutoring_channel = self.bot.get_channel(self.tutoring_channel_raw)
        self.tutor_admin_channel = self.bot.get_channel(self.tutor_admin_channel_raw)
        self.bot.loop.create_task(self.scan_table())
        self.members = {
            member.name: member.id
            for guild in self.bot.guilds
            for member in guild.members
            if guild.name == "Data Science with Daniel"
        }

    async def scan_table(self, tutees=True, tutors=True):
        while True:
            if tutees:
                await self.validate_tutees()
            if tutors:
                await self.validate_tutors()
            await asyncio.sleep(1800)

    async def validate_tutees(self):
        tutee_response = self.table.scan(
            TableName=self.tablename,
            FilterExpression=Attr("tuteeValidation").eq(False) & Attr("tutee").eq(True),
        )["Items"]
        if len(tutee_response) == 0:
            return False
        for tutee in tutee_response:
            tags = self.find_tutors(tutee)
            message = await self.post_new_tutoring(tutee, tags)
            self.complete_validation(tutee, message, field="tuteeValidation")
        return True

    async def post_new_tutoring(self, tutee, tags):
        try:
            price = f"Asking Price: {tutee['tuteePrice']}\n"
        except KeyError:
            price = ""
        req_languages = f"Requested Langauge/s: {' - '.join([lang for lang in self.languages if tutee[lang]])}"
        embed = discord.Embed(
            title="Tutoring Request",
            url="https://www.datasciencewithdaniel.com.au/tutoring.html",
            description=f"""
                React to this message to accept or decline a tutoring request from {tutee['username']}! Please only accept the request if no one else already has.\n
                {req_languages}\n{price}
                {helpers.find_emoji(YES)} - if you would like to accept this tutoring request\n
                {helpers.find_emoji(NO)} - if you would like to decline this tutoring request\n
                Please send {tutee['username']} a message if you accept their tutoring request to arrange the details.\n
                Tutoring Reason:\n{tutee['reason']}\n
                """,
            color=0xB4E4F9,
        )
        message = await self.tutoring_channel.send(tags, embed=embed)
        await message.add_reaction(emoji=helpers.find_emoji(YES))
        await message.add_reaction(emoji=helpers.find_emoji(NO))
        return message

    def complete_validation(self, tut, message, field):
        tut[field] = True
        tut[field[:5] + "_message_id"] = message.id
        try:
            tut["userID"] = self.members[tut["username"]]
        except KeyError:
            pass
        self.table.put_item(Item=tut)
        return True

    def find_tutors(self, tutee):
        avail_tutors = self.table.scan(
            TableName=self.tablename, FilterExpression=Attr("tutorComplete").eq(True)
        )["Items"]
        tutors = []
        for tutor in avail_tutors:
            for lang in self.languages:
                if tutee[lang] and tutor[lang] and tutor["username"] not in tutors:
                    tutors.append(tutor["username"])
        tutor_mentioned = []
        for tutor in tutors:
            if tutor in list(self.members.keys()):
                tutor_mentioned.append(f"<@{self.members[tutor]}>")
        tutor_mentioned = " ".join(tutor_mentioned)
        tags = f"Matching Tutors: {tutor_mentioned}"
        return tags

    async def validate_tutors(self):
        tutor_response = self.table.scan(
            TableName=self.tablename,
            FilterExpression=Attr("tutorValidation").eq(False) & Attr("tutor").eq(True),
        )["Items"]
        if len(tutor_response) == 0:
            return False
        for tutor in tutor_response:
            message = await self.post_new_tutor(tutor)
            self.complete_validation(tutor, message, field="tutorValidation")
        return True

    async def post_new_tutor(self, tutor):
        embed = discord.Embed(
            title="Tutor Request",
            url="https://www.datasciencewithdaniel.com.au/tutoring.html",
            description=f"""
                React to this message to accept or decline a tutor request from {tutor['username']}!\n
                {helpers.find_emoji(YES)} - if you would like to accept this tutor request\n
                {helpers.find_emoji(NO)} - if you would like to decline this tutor request\n
                Tutor Justification:\n{tutor['justification']}\n
                """,
            color=0xB4E4F9,
        )
        message = await self.tutor_admin_channel.send(embed=embed)
        await message.add_reaction(emoji=helpers.find_emoji(YES))
        await message.add_reaction(emoji=helpers.find_emoji(NO))
        return message

    async def reaction_edits(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        if channel == self.tutor_admin_channel:
            embed_field = "tutorComplete"
            tutor = "N/A"
        elif channel == self.tutoring_channel:
            embed_field = "tuteeComplete"
            tutor = payload.member.name
        else:
            return False

        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        emoji = unicodedata.name(payload.emoji.name)

        reactions = [
            YES,
            NO,
        ]
        if user.name == "Penguin" or emoji not in reactions:
            return False

        entry = self.table.scan(
            TableName=self.tablename,
            FilterExpression=Attr(embed_field[:5] + "_message_id").eq(
                payload.message_id
            )
            & Attr(embed_field).eq(False),
        )["Items"]
        if len(entry) != 1:
            return False

        if emoji == YES:
            self.table.update_item(
                Key={"email": entry[0]["email"]},
                AttributeUpdates={
                    embed_field: {"Value": True},
                    "tutorName": {"Value": tutor},
                },
            )
            if embed_field == "tutorComplete":
                tutor_user = guild.get_member(entry[0]["userID"])
                role = get(guild.roles, name="Tutor")
                await tutor_user.add_roles(role)
                helpers.role_log(
                    user,
                    payload.emoji,
                    channel,
                    role,
                    payload.event_type,
                    logger=self.logger,
                )
            elif embed_field == "tuteeComplete":
                await self.send_tutee_dm(payload, entry)

    async def send_tutee_dm(self, user, entry):
        tutee = self.bot.get_user(entry[0]["userID"])
        author = user.member.nick if user.member.nick is not None else user.member.name
        await tutee.create_dm()
        await tutee.dm_channel.send(
            f"{author} has accepted your tutoring request and will be reaching out to you!"
        )

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        await self.reaction_edits(payload)
