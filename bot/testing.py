# @bot.command(name='create-channel')
# @commands.has_role('bot-testing')
# async def create_channel(ctx, channel_name='real-python'):
#     guild = ctx.guild
#     existing_channel = discord.utils.get(guild.channels, name=channel_name)
#     if not existing_channel:
#         print(f'Creating a new channel: {channel_name}')
#         await guild.create_text_channel(channel_name)

# @bot.command(name='roll_dice', help='Simulates rolling dice.')
# async def roll(ctx, number_of_dice: int, number_of_sides: int):
#     dice = [
#         str(random.choice(range(1, number_of_sides + 1)))
#         for _ in range(number_of_dice)
#     ]
#     await ctx.send(', '.join(dice))


# from discord.ext import commands
# from discord.utils import get
# import unicodedata
# import discord
# from discord import RawReactionActionEvent
# from bot import helpers


# class testing(commands.Cog):
#     def __init__(self, bot, GUILD_ID, logger):
#         self.bot = bot
#         self.GUILD_ID = GUILD_ID
#         self.logger = logger


