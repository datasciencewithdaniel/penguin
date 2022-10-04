import asyncio
import boto3
from boto3.dynamodb.conditions import Attr
# import unicodedata
import discord
from discord.ext import commands
# from discord import RawReactionActionEvent
# from discord.utils import get
from bot import helpers


class contact(commands.Cog):
    def __init__(self, bot, GUILD_ID, table, credentials, logger):
        self.bot = bot
        self.GUILD_ID = GUILD_ID
        self.logger = logger
        # self.session = boto3.session.Session(profile_name="dswd")
        # self.resource = self.session.resource("dynamodb")
        self.resource = boto3.resource(
            "dynamodb", region_name="ap-southeast-2",
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )
        self.tablename = table
        self.table = self.resource.Table(self.tablename)
        self.channel_raw = 918845689285447681
        self.reactions = ["LARGE GREEN CIRCLE", "LARGE RED CIRCLE"]

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = discord.utils.get(self.bot.guilds, name=self.GUILD_ID)
        self.contact_channel = self.bot.get_channel(self.channel_raw)
        self.bot.loop.create_task(self.scan_table())

    async def scan_table(self):
        while True:
            await self.find_message()
            await asyncio.sleep(28800)

    async def find_message(self):
        messages = self.table.scan(
            TableName=self.tablename,
            FilterExpression=Attr("posted").eq(False),
        )["Items"]
        if len(messages) == 0:
            return False
        for message in messages:
            await self.post_message(message)
            await self.complete_validation(message)

    async def post_message(self, message):
        user = self.guild.get_member_named(message["username"])
        user_embed = f"\nUsername: \n{user}\n" if user else ""
        embed = discord.Embed(
            title="New Contact Form Message!",
            description=f"""
                Name: \n{message['firstName']} {message['lastName']}\n
                Email: \n{message['email']}\n{user_embed}
                Message: \n{message['message']}\n
                """,
            color=0xB4E4F9,
        )
        new_message = await self.contact_channel.send(embed=embed)
        for emoji in self.reactions:
            await new_message.add_reaction(emoji=helpers.find_emoji(emoji))

        return True

    async def complete_validation(self, message):
        message['posted'] = True
        self.table.put_item(Item=message)
        return True
