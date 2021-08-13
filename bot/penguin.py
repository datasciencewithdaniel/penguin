import os
from dotenv import load_dotenv

from discord.ext import commands

from bot import admin, notifications, responses, roles

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

bot = commands.Bot(command_prefix=".")

bot.add_cog(admin.admin(bot, GUILD))
bot.add_cog(notifications.notifications(bot))
bot.add_cog(responses.responses(bot))
bot.add_cog(roles.roles(bot))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")


bot.run(TOKEN)
