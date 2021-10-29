import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import logging

from bot import admin, notifications, responses, roles, tutoring, tutoring_commands

BOT = "BabyPenguin"  # Penguin

load_dotenv()
if BOT == "BabyPenguin":
    TOKEN = os.getenv("DISCORD_TOKEN2")
else:
    TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

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

bot.add_cog(admin.admin(bot, GUILD, logger))
bot.add_cog(notifications.notifications(bot, logger))
bot.add_cog(responses.responses(bot, logger))
bot.add_cog(roles.roles(bot, GUILD, logger))
bot.add_cog(tutoring.tutoring(bot, GUILD, logger))
bot.add_cog(tutoring_commands.tutoring_commands(bot, logger))
# bot.add_cog(background.background(bot))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")


bot.run(TOKEN)
