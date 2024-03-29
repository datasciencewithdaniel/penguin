import argparse
import discord
from discord.ext import commands
import logging
import boto3

from bot import (
    admin,
    notifications,
    responses,
    roles,
    tutoring,
    suggestions,
    coder,
    todo,
    bn_interviews,
    github,
    contact,
    testing
)  # , tutoring_commands

my_parser = argparse.ArgumentParser(description='Bot Selection')
my_parser.add_argument('--bot', metavar='bot', type=str, choices=['0','1'], default='1', help='the bot selection to use')
my_parser.add_argument('--discord', metavar='discord', type=str, help='the discord token')
my_parser.add_argument('--guild', metavar='guild', type=str, help='the discord guild name')
my_parser.add_argument('--account', metavar='account', type=str, help='the dswd AWS account')

args = my_parser.parse_args()

MYBOTS = ["Penguin", "BabyPenguin"]
if args.bot == '0':
    BOT = MYBOTS[0]
    tutor_table = "tutoring-base"
else:
    BOT = MYBOTS[1]
    tutor_table = "tutoring-dev"

TOKEN = args.discord
GUILD_ID = args.guild
contact_table = "website-contact"

sts_client = boto3.client('sts')
assumed_role_object = sts_client.assume_role(
    RoleArn=f"arn:aws:iam::{args.account}:role/penguin-dynamodb-role",
    RoleSessionName=f"AssumeRole{BOT}"
)
credentials = assumed_role_object['Credentials']

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

if BOT == "BabyPenguin":
    bot = commands.Bot(command_prefix=",", intents=discord.Intents.all())
else:
    bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

bot.add_cog(admin.admin(bot, GUILD_ID, logger))
bot.add_cog(notifications.notifications(bot, logger))
bot.add_cog(responses.responses(bot, logger))
bot.add_cog(roles.roles(bot, GUILD_ID, logger))
bot.add_cog(tutoring.tutoring(bot, GUILD_ID, tutor_table, credentials, logger))
bot.add_cog(suggestions.suggestions(bot, GUILD_ID, logger))
bot.add_cog(coder.coder(bot, GUILD_ID, logger))
bot.add_cog(todo.todo(bot, GUILD_ID, logger))
bot.add_cog(bn_interviews.bn_interviews(bot, GUILD_ID, logger))
bot.add_cog(github.github(bot, GUILD_ID, logger))
bot.add_cog(contact.contact(bot, GUILD_ID, contact_table, credentials, logger))
# bot.add_cog(tutoring_commands.tutoring_commands(bot, table, credentials, logger))
# bot.add_cog(background.background(bot))
# bot.add_cog(testing.testing(bot, GUILD_ID, logger))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")

bot.run(TOKEN)
