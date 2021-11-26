import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import logging

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
    testing
)  # , tutoring_commands


MYBOTS = ["Penguin", "BabyPenguin"]
BOT = MYBOTS[0]

load_dotenv()
if BOT == "BabyPenguin":
    TOKEN = os.getenv("DISCORD_TOKEN2")
    table = "tutoring-dev"
else:
    TOKEN = os.getenv("DISCORD_TOKEN")
    table = "tutoring-base"
GUILD_ID = os.getenv("DISCORD_GUILD")

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
bot.add_cog(tutoring.tutoring(bot, GUILD_ID, table, logger))
bot.add_cog(suggestions.suggestions(bot, GUILD_ID, logger))
bot.add_cog(coder.coder(bot, GUILD_ID, logger))
bot.add_cog(todo.todo(bot, GUILD_ID, logger))
bot.add_cog(bn_interviews.bn_interviews(bot, GUILD_ID, logger))
bot.add_cog(github.github(bot, GUILD_ID, logger))
# bot.add_cog(tutoring_commands.tutoring_commands(bot, table, logger))
# bot.add_cog(background.background(bot))
# bot.add_cog(testing.testing(bot, GUILD_ID, logger))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")

bot.run(TOKEN)
