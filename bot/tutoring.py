import asyncio
import boto3
from boto3.dynamodb.conditions import Attr
import unicodedata
import discord
from discord.ext import commands
from discord import RawReactionActionEvent
from bot import helpers


class tutoring(commands.Cog):
    def __init__(self, bot, GUILD, logger):
        self.bot = bot
        self.GUILD = GUILD
        self.logger = logger
        self.bot.loop.create_task(self.scan_table())
        self.session = boto3.session.Session(profile_name="dswd")
        self.resource = self.session.resource("dynamodb")
        self.table = self.resource.Table("tutoring-base")
        self.languages = ["Python", "SQL", "Java", "JavaScript", "Bash", "R"]
        self.tutoring_channel = self.bot.get_channel(890976909054320681)
        self.tutor_admin_channel = self.bot.get_channel(895262367112384522)

    async def scan_table(self, tutees=True, tutors=True):
        while True:
            if tutees:
                self.validate_tutees()
            if tutors:
                self.validate_tutors()
            await asyncio.sleep(1800)

    def validate_tutees(self):
        tutee_response = self.table.scan(
            TableName="tutoring-base",
            FilterExpression=Attr("tuteeValidation").eq(False) & Attr("tutee").eq(True),
        )["Items"]
        if len(tutee_response) == 0:
            return False
        for tutee in tutee_response:
            tutors = tutors.append(self.find_tutors(tutee))
            self.post_new_tutoring(tutee, tutors)
            self.complete_validation(tutee, field="tuteeValidation")

    async def post_new_tutoring(self, tutee, tutors):
        tutor_mentioned = " @".join(tutors)  # CHANGE TO ACTUAL MENTIONS
        embed = discord.Embed(
            title="Tutoring Request",
            url="https://www.datasciencewithdaniel.com.au/tutoring.html",
            description=f"""
                React to this message to accept or decline a tutoring request from {tutee['username']}! Please only accept the request if no one else already has.\n
                {tutor_mentioned}\n
                {helpers.find_emoji("CHECK_MARK_BUTTON")} - if you would like to accept this tutoring request\n
                {helpers.find_emoji("CROSS_MARK")} - if you would like to decline this tutoring request\n
                Please send {tutee['username']} a message if you accept their tutoring request to arrange the details.\n
                Tutoring Reason:\n
                {tutee['justification']}\n
                """,
            color=0xB4E4F9,
        )
        embed.add_field(name="tuteeComplete", value=tutee["email"])
        message = await self.tutoring_channel.send(embed=embed)
        await message.add_reaction(emoji=helpers.find_emoji("CHECK_MARK_BUTTON"))
        await message.add_reaction(emoji=helpers.find_emoji("CROSS_MARK"))
        # IF TICK - UPDATE TABLE WITH TUTOR

    def complete_validation(self, tutee, field):
        tutee[field] = True
        self.table.put_item(Item=tutee)

    def find_tutors(self, tutee):
        tutee_lang = None
        for lang in self.languages:
            if tutee[lang] is True:
                tutee_lang = lang
        avail_tutors = self.table.scan(
            TableName="tutoring-base",
            ProjectionExpression="username",
            FilterExpression=Attr("tutorComplete").eq(True) & Attr(tutee_lang).eq(True),
        )["Items"]
        return [tutor["username"] for tutor in avail_tutors]

    def validate_tutors(self):
        tutor_response = self.table.scan(
            TableName="tutoring-base",
            FilterExpression=Attr("tutorValidation").eq(False) & Attr("tutor").eq(True),
        )["Items"]
        if len(tutor_response) == 0:
            return False
        for tutor in tutor_response:
            self.post_new_tutor(tutor)
            self.complete_validation(tutor, field="tutorValidation")

    async def post_new_tutor(self, tutor):
        embed = discord.Embed(
            title="Tutor Request",
            url="https://www.datasciencewithdaniel.com.au/tutoring.html",
            description=f"""
                React to this message to accept or decline a tutor request from {tutor['username']}!\n
                {helpers.find_emoji("CHECK_MARK_BUTTON")} - if you would like to accept this tutor request\n
                {helpers.find_emoji("CROSS_MARK")} - if you would like to decline this tutor request\n
                Tutor Justification:\n
                {tutor['justification']}\n
                """,
            color=0xB4E4F9,
        )
        embed.add_field(name="tutorComplete", value=tutor["email"])
        message = await self.tutoring_channel.send(embed=embed)
        await message.add_reaction(emoji=helpers.find_emoji("CHECK_MARK_BUTTON"))
        await message.add_reaction(emoji=helpers.find_emoji("CROSS_MARK"))

    async def reaction_edits(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        if channel != self.tutor_admin_channel or channel != self.tutoring_channel:
            return False
        elif channel == self.tutor_admin_channel:
            embed_field = "tutorComplete"
        elif channel == self.tutoring_channel:
            emebd_field = "tuteeComplete"

        user = self.GUILD.get_member(payload.user_id)
        emoji = unicodedata.name(payload.emoji.name)

        reactions = [
            "CHECK_MARK_BUTTON",
            "CROSS_MARK",
        ]

        user_key = None
        msg = await channel.fetch_message(payload.message_id)
        embed = msg.embeds[0]
        for field in embed.fields:
            if field.name == embed_field:
                user_key = field.value

        if user.name == "Penguin" or emoji not in reactions:
            return False
        if emoji == "CHECK_MARK_BUTTON":
            self.table.update_item(
                Key={"email": user_key},
                AttributeUpdates={
                    emebd_field: True,
                },
            )
        # ADD TUTOR ROLE IF FOR TUTOR
        # LOGGING?

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        await self.reaction_edits(payload)
