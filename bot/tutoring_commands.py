from discord.ext import commands
import boto3
from boto3.dynamodb.conditions import Attr
from bot import helpers


class tutoring_commands(commands.Cog):
    def __init__(self, bot, table, logger):
        self.bot = bot
        self.logger = logger
        self.session = boto3.session.Session(profile_name="dswd")
        self.resource = self.session.resource("dynamodb")
        self.tablename = table
        self.table = self.resource.Table(self.tablename)

    @commands.command(name="recommend", help="Give your tutor a recommendation")
    async def recommend(self, ctx, *args):
        tutor_name = args[0]
        message = " ".join(args[1:])
        tutor, tutor_id = False, False
        for member in ctx.guild.members:
            if member.nick == tutor_name or member.name == tutor_name:
                tutor = member
                tutor_id = member.id
                break
        print(tutor_id)
        if tutor:
            author = ctx.author.nick if ctx.author.nick is not None else ctx.author
            await tutor.create_dm()
            await tutor.dm_channel.send(
                f"You have received a new recommendation from {author}!\nRecommendation is as follows:\n{message}"
            )

        entry = self.bot.table.scan(
            TableName=self.bot.tablename, FilterExpression=Attr("userID").eq(tutor_id)
        )["Items"]
        if len(entry) != 1:
            return False

        self.table.update_item(
            Key={"email": entry[0]["email"]},
            AttributeUpdates={
                "recommendations": {"Value": entry["recommendations"] + [message]},
            },
        )

    # @commands.command(name="rating", help="Give your tutor a rating")
    # async def rating(self, ctx):
    #     response = "How many stars would you rate your tutor out of 5?"
    #     await ctx.author.create_dm()
    #     message = await ctx.author.dm_channel.send(response)
    #     await message.add_reaction(emoji=helpers.find_emoji("DIGIT_ONE*")) # EMOJI NOT WORKING
    #     helpers.command_log(
    #         ctx, logger=self.logger
    #     )
