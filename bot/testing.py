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
#         self.reactions = ["LARGE GREEN CIRCLE", "LARGE RED CIRCLE"]
#         self.potential_roles = {
#             "Developer-Admin" : 908646555408535562,
#             "Consult-Admin" : 908645981753585674,
#             "Tutor-Admin" : 895262367112384522,
#             "Bot-Admin" : 883346863326117888,
#             "Crypto-Admin" : 883346863326117888,
#             "Coder-Admin" : 883346863326117888
#         }

#     @commands.command(name="request_role", help="Requests a given Admin role [role]")
#     @commands.has_role("Administrator")
#     async def admin_roles(self, ctx, *args):
#         channel = ctx.message.channel
#         helpers.command_log(ctx, logger=self.logger)
        
#         role = False
#         for potential in list(self.potential_roles.keys()):
#             check = "".join(args).lower()
#             if check[:3] == potential.lower()[:3]:
#                 role = potential

#         if role:
#             channel = self.bot.get_channel(self.potential_roles[role])

#             role_embed = discord.Embed(
#                 title=f"New {role} Role Request from {ctx.message.author.name}!",
#                 description=f"""
#                 {helpers.find_emoji(self.reactions[0])} - if you would like to accept this request\n
#                 {helpers.find_emoji(self.reactions[1])} - if you would like to decline this request\n
#                 """,
#                 color=0xB4E4F9,
#             )
#             role_embed.add_field(name="UserID", value=ctx.message.author.id)
#             role_embed.add_field(name="Role", value=role)

#             message = await channel.send(embed=role_embed)

#             for emoji in self.reactions:
#                 await message.add_reaction(emoji=helpers.find_emoji(emoji))

#     async def reaction_edits(self, payload):
#         channel = self.bot.get_channel(payload.channel_id)
#         if channel.id not in list(self.potential_roles.values()):
#             return False

#         guild = self.bot.get_guild(payload.guild_id)
#         user = guild.get_member(payload.user_id)
#         emoji = unicodedata.name(payload.emoji.name)
#         message = await channel.fetch_message(payload.message_id)
        
#         if user.name in ["Penguin", "BabyPenguin"] or emoji not in self.reactions:
#             return False

#         for emb in message.embeds[0].fields:
#             if emb.name == "UserID":
#                 req = guild.get_member(int(emb.value))
#             elif emb.name == "Role":
#                 role = get(guild.roles, name=emb.value)

#         if emoji == "LARGE GREEN CIRCLE":
#             await req.add_roles(role)
#             await req.create_dm()
#             await req.dm_channel.send(
#                 f"Hi {req.name}, your request for {role.name} has been approved! Check out the respective Admin channel to get started."
#             )
#         elif emoji == "LARGE RED CIRCLE":
#             await req.remove_roles(role)
#             await req.create_dm()
#             await req.dm_channel.send(
#                 f"Hi {req.name}, your request for {role.name} has been rejected/removed! Please follow up with {user.name} if you require more information."
#             )

#         helpers.role_log(
#             req, payload.emoji, channel, role, payload.event_type, logger=self.logger
#         )

#     @commands.Cog.listener()
#     async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
#         await self.reaction_edits(payload)

