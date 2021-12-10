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
    def __init__(self, bot, GUILD_ID, table, logger):
        self.bot = bot
        self.GUILD_ID = GUILD_ID
        self.logger = logger
        self.session = boto3.session.Session(profile_name="dswd")
        self.resource = self.session.resource("dynamodb")
        self.tablename = table
        self.table = self.resource.Table(self.tablename)
        self.languages = ["Python", "SQL", "Java", "JavaScript"]
        self.tutoring_channel_raw = 890976909054320681
        self.tutor_admin_channel_raw = 895262367112384522

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = discord.utils.get(self.bot.guilds, name=self.GUILD_ID)
        self.tutoring_channel = self.bot.get_channel(self.tutoring_channel_raw)
        self.tutor_admin_channel = self.bot.get_channel(self.tutor_admin_channel_raw)
        self.bot.loop.create_task(self.scan_table())

    async def scan_table(self, tutees=True, tutors=True):
        while True:
            if tutees:
                await self.validate_tutees()
            if tutors:
                await self.validate_tutors()
            await asyncio.sleep(28800)

    async def validate_tutees(self):
        tutee_response = self.table.scan(
            TableName=self.tablename,
            FilterExpression=Attr("tuteeValidation").eq(False) & Attr("tutee").eq(True),
        )["Items"]
        if len(tutee_response) == 0:
            return False
        for tutee in tutee_response:
            tags, tags_list = self.find_tutors(tutee)
            message = await self.post_new_tutoring(tutee, tags)
            await self.complete_validation(tutee, message, field="tuteeValidation")
            await self.message_member(tutee, tags_list, "tutee")
        return True

    async def post_new_tutoring(self, tutee, tags):
        user = self.guild.get_member_named(tutee["username"])
        try:
            price = f"Asking Price: {tutee['tuteePrice']}\n"
        except KeyError:
            price = ""
        req_languages = f"Requested Langauge/s: {' - '.join([lang for lang in self.languages if tutee[lang]])}"
        embed = discord.Embed(
            title="Tutoring Request",
            url="https://www.datasciencewithdaniel.com.au/tutoring.html",
            description=f"""
                React to this message to accept or decline a tutoring request from {user.display_name}! Please only accept the request if no one else already has.\n
                {req_languages}\n{price}
                {helpers.find_emoji(YES)} - if you would like to accept this tutoring request\n
                {helpers.find_emoji(NO)} - if you would like to decline this tutoring request\n
                Please send {user.display_name} a message if you accept their tutoring request to arrange the details.\n
                Tutoring Reason:\n{tutee['reason']}\n
                """,
            color=0xB4E4F9,
        )
        message = await self.tutoring_channel.send(tags, embed=embed)
        await message.add_reaction(emoji=helpers.find_emoji(YES))
        await message.add_reaction(emoji=helpers.find_emoji(NO))
        return message

    async def complete_validation(self, tut, message, field):
        tut[field] = True
        tut[field[:5] + "_message_id"] = message.id
        try:
            tut["userID"] = self.guild.get_member_named(tut["username"]).id
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
            tutor_check = self.guild.get_member_named(tutor)
            if tutor_check:
                tutor_mentioned.append(f"<@{tutor_check.id}>")
        tutor_mentioned_s = " ".join(tutor_mentioned)
        tags = f"Matching Tutors: {tutor_mentioned_s}"
        return tags, tutor_mentioned

    async def message_member(self, member, tags_list, member_type):
        user = self.guild.get_member_named(member["username"])

        if member_type == "tutee":
            template1 = "Your tutoring request has been posted to the Data Science with Daniel tutoring channel! "
            template2 = (
                f"There is currently {len(tags_list)} tutor that matches your request. "
            )
            template3 = (
                f"There are currently {len(tags_list)} tutors that match your request. "
            )
            if len(tags_list) == 0:
                template3 = (
                    template3
                    + "Your request will still be reviewed to see if there is anyone that can help out"
                )
        elif member_type == "tutor":
            template1 = "Your tutor request has been posted to the Data Science with Daniel tutoring admin channel! "
            template2 = ""
            template3 = "Look out for a message from the team to verify you as a tutor."

        if user and len(tags_list) == 1:
            await user.create_dm()
            await user.dm_channel.send(template1 + template2)
        elif user and len(tags_list) != 1:
            await user.create_dm()
            await user.dm_channel.send(template1 + template3)

        return True

    async def validate_tutors(self):
        tutor_response = self.table.scan(
            TableName=self.tablename,
            FilterExpression=Attr("tutorValidation").eq(False) & Attr("tutor").eq(True),
        )["Items"]
        if len(tutor_response) == 0:
            return False
        for tutor in tutor_response:
            message = await self.post_new_tutor(tutor)
            await self.complete_validation(tutor, message, field="tutorValidation")
            await self.message_member(tutor, [], "tutor")
        return True

    async def post_new_tutor(self, tutor):
        user = self.guild.get_member_named(tutor["username"])
        embed = discord.Embed(
            title="Tutor Request",
            url="https://www.datasciencewithdaniel.com.au/tutoring.html",
            description=f"""
                React to this message to accept or decline a tutor request from {user.display_name}!\n
                {helpers.find_emoji(YES)} - if you would like to accept this tutor request\n
                {helpers.find_emoji(NO)} - if you would like to decline this tutor request\n
                Tutor Justification:\n{tutor['justification']}\n
                Python:     {tutor['Python']:^10}{tutor['PythonExp']:^20}
                SQL:        {tutor['SQL']:^10}{tutor['SQLExp']:^20}
                Java:       {tutor['Java']:^10}{tutor['JavaExp']:^20}
                JavaScript: {tutor['JavaScript']:^10}{tutor['JavaScriptExp']:^20}\n
                """,
            color=0xB4E4F9,
        )
        embed.set_footer(text=user.id)

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
