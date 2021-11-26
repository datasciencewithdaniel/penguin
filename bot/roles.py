from discord.ext import commands
from discord.utils import get
import unicodedata
import discord
from discord import RawReactionActionEvent
from bot import helpers


class roles(commands.Cog):
    def __init__(self, bot, GUILD_ID, logger):
        self.bot = bot
        self.GUILD_ID = GUILD_ID
        self.logger = logger
        self.WELCOME_ID = 851074616947769354
        self.BANNER_ID = 908916326138007572
        self.TEXT_ID = 908916330743332886
        self.REACT_ID = 908916331888402495
        self.reactions1 = [
            "SNAKE",  # DEVELOPER
            "OCTOPUS",  # OBSERVER
            "OWL",  # CODER
            "SPOUTING WHALE",  # BELUGA
            "PENGUIN",  # PENGUIN
            "SPIDER WEB",  # WEB
            "MONKEY",  # SPACE
        ]
        self.reactions2 = ["PEACOCK"]
        self.DEV_ID = 908646555408535562
        self.CONSULT_ID = 908645981753585674
        self.TUTOR_ID = 895262367112384522
        self.BOT_ID = 883346863326117888
        self.potential_roles = {
            "Developer-Admin" : 908646555408535562,
            "Consult-Admin" : 908645981753585674,
            "Tutor-Admin" : 895262367112384522,
            "Bot-Admin" : 883346863326117888,
            "Crypto-Admin" : 883346863326117888,
            "Coder-Admin" : 883346863326117888
        }

    async def reaction_edits(self, payload, action="remove"):
        channel = self.bot.get_channel(payload.channel_id)
        if channel == self.bot.get_channel(self.WELCOME_ID):
            await self.welcome_reactions(payload, action)
        elif channel.id in list(self.potential_roles.values()):
            await self.admin_reactions(payload, action)

    async def welcome_reactions(self, payload, action="remove"):
        channel = self.bot.get_channel(payload.channel_id)
        if channel != self.bot.get_channel(self.WELCOME_ID):
            return False

        if payload.message_id != self.REACT_ID:
            return False

        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        emoji = unicodedata.name(payload.emoji.name)

        if user.name in ["Penguin", "BabyPenguin"] or emoji not in self.reactions1:
            return False
        if emoji == "SNAKE":
            role = get(guild.roles, name="Developer")
        elif emoji == "OCTOPUS":
            role = get(guild.roles, name="Observer")
        elif emoji == "OWL":
            role = get(guild.roles, name="Coder")
        elif emoji == "SPOUTING WHALE":
            role = get(guild.roles, name="Dev-Beluga")
        elif emoji == "PENGUIN":
            role = get(guild.roles, name="Dev-Penguin")
        elif emoji == "SPIDER WEB":
            role = get(guild.roles, name="Dev-Web")
        elif emoji == "MONKEY":
            role = get(guild.roles, name="Dev-Space")

        helpers.role_log(
            user, payload.emoji, channel, role, payload.event_type, logger=self.logger
        )

        if action == "add":
            await user.add_roles(role)
        else:
            await user.remove_roles(role)

    async def admin_reactions(self, payload, action):
        channel = self.bot.get_channel(payload.channel_id)
        if channel.id not in list(self.potential_roles.values()):
            return False

        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        emoji = unicodedata.name(payload.emoji.name)
        message = await channel.fetch_message(payload.message_id)
        
        if user.name in ["Penguin", "BabyPenguin"] or emoji not in self.reactions2:
            return False

        for emb in message.embeds[0].fields:
            if emb.name == "UserID":
                req = guild.get_member(int(emb.value))
            elif emb.name == "Role":
                role = get(guild.roles, name=emb.value)

        if action == "add":
            await req.add_roles(role)
        else:
            await req.remove_roles(role)
        
        # if emoji == "PEACOCK":
        #     await req.add_roles(role)
        #     await req.create_dm()
        #     await req.dm_channel.send(
        #         f"Hi {req.name}, your request for {role.name} has been approved! Check out the respective Admin channel to get started."
        #     )

        helpers.role_log(
            req, payload.emoji, channel, role, payload.event_type, logger=self.logger
        )

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        await self.reaction_edits(payload, "add")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        await self.reaction_edits(payload)

    @commands.command(
        name="update_welcome", help="Updates the embeds in the welcome channel [new]"
    )
    @commands.has_role("Administrator")
    async def update_welcome(self, ctx, arg):

        guild = discord.utils.get(self.bot.guilds, name=self.GUILD_ID)
        channel = self.bot.get_channel(self.WELCOME_ID)

        banner_embed = discord.Embed(
            color=0xB4E4F9,
        )
        banner_embed.set_image(
            url="https://datasciencewithdaniel.com.au/images/Banner.png"
        )

        text_embed = discord.Embed(
            title="Welcome to Data Science with Daniel!",
            description=f"""
            We seek to build a community of Data Scientists, so that we can share our passion and learn together. We do this by bringing everything and everyone together in one place; Data Science with Daniel.\n
            For Students; We support anyone on their Data Science journey by providing an environment where they can ask questions, find answers and connect with others.\n
            For Industry; We engage with industry to understand the Data Science landscape and ensure that the next generation of Data Scientists develop the skills to succeed in their career.\n
            For Academics; We promote studying Data Science to bring new people into the field and provide feedback to improve these studies.\n
            By being part of this community you agree to be respectful and considerate of other members. Everyone is at a different stage of their Data Science learning journey, and this community is here to help and support everyone.\n
            The announcements and events channels will be used to notify members of important information or when events are running, react to the roles below based on how you want to be notified.\n
            We look forward to being part of your Data Science journey.
            """,
            color=0xB4E4F9,
        )

        roles_embed = discord.Embed(
            title="Reaction Roles",
            description=f"""
                React to this messgage to get your roles!\n
                {helpers.find_emoji("SNAKE")} {get(guild.roles, name="Developer").mention} - if you want to write code and contribute to any project\n
                {helpers.find_emoji("OCTOPUS")} {get(guild.roles, name="Observer").mention} - if you are happy to watch and attend events to learn\n
                {helpers.find_emoji("OWL")} {get(guild.roles, name="Coder").mention} - if you want to be invovled in coding challenges\n
                {helpers.find_emoji("SPOUTING WHALE")} {get(guild.roles, name="Dev-Beluga").mention} - if you want to be part of developing the Beluga library\n
                {helpers.find_emoji("PENGUIN")} {get(guild.roles, name="Dev-Penguin").mention} - if you want to be part of developing the Penguin bot\n
                {helpers.find_emoji("SPIDER WEB")} {get(guild.roles, name="Dev-Web").mention} - if you want to be part of developing the website\n
                {helpers.find_emoji("MONKEY")} {get(guild.roles, name="Dev-Space").mention} - if you want to be part of analysing space data\n
                """,
            color=0xB4E4F9,
        )

        if arg == "new":
            await channel.send(embed=banner_embed)
            await channel.send(embed=text_embed)
            message = await channel.send(embed=roles_embed)
        else:
            message = await channel.fetch_message(self.BANNER_ID)
            await message.edit(embed=banner_embed)

            message = await channel.fetch_message(self.TEXT_ID)
            await message.edit(embed=text_embed)

            message = await channel.fetch_message(self.REACT_ID)
            await message.edit(embed=roles_embed)
            await message.clear_reactions()

        for emoji in self.reactions1:
            await message.add_reaction(emoji=helpers.find_emoji(emoji))

    @commands.command(name="update_role_ids", help="Updates the role ids [var][id]")
    @commands.has_role("Administrator")
    async def update_role_ids(self, ctx, *args):
        try:
            id = int(args[1])
        except ValueError:
            return False

        if args[0] == "WELCOME_ID":
            self.WELCOME_ID = id
        elif args[0] == "BANNER_ID":
            self.BANNER_ID = id
        elif args[0] == "TEXT_ID":
            self.TEXT_ID = id
        elif args[0] == "REACT_ID":
            self.REACT_ID = id

        helpers.command_log(ctx, logger=self.logger)

    @commands.command(name="admin_roles", help="Adds the respective Admin roles to the user [user][role*]")
    @commands.has_role("Administrator")
    async def admin_roles(self, ctx, *args):
        channel = ctx.message.channel
        guild = discord.utils.get(self.bot.guilds, name=self.GUILD_ID)
        user = guild.get_member(int(args[0]))
        helpers.command_log(ctx, logger=self.logger)

        potential_roles = [
            "Developer-Admin",
            "Consult-Admin",
            "Tutor-Admin",
            "Bot-Admin",
            "Crypto-Admin",
            "Coder-Admin"
        ]

        potential_channels = [
            self.DEV_ID,
            self.CONSULT_ID,
            self.TUTOR_ID,
            self.BOT_ID
        ]
        
        roles = []
        for role in args[1:]:
            new_role = None
            if channel.id in potential_channels and role in potential_roles:
                new_role = get(guild.roles, name=role)
            
            if new_role:
                roles.append(new_role)
                await user.add_roles(new_role)

        if len(roles) != len(args[1:]):
            await channel.send("One or more of these roles cannot be added from this channel")
                
    @commands.command(name="request_role", help="Requests a given Admin role [role]")
    @commands.has_role("Administrator")
    async def admin_roles(self, ctx, *args):
        channel = ctx.message.channel
        helpers.command_log(ctx, logger=self.logger)
        
        role = False
        for potential in list(self.potential_roles.keys()):
            check = "".join(args).lower()
            if check[:3] == potential.lower()[:3]:
                role = potential

        if role:
            channel = self.bot.get_channel(self.potential_roles[role])

            role_embed = discord.Embed(
                title=f"New Role Request from {ctx.message.author.name}!",
                description=f"""
                {helpers.find_emoji(self.reactions2[0])} - to accept or decline this request\n
                """,
                color=0xB4E4F9,
            )
            role_embed.add_field(name="UserID", value=ctx.message.author.id)
            role_embed.add_field(name="Role", value=role)

            message = await channel.send(embed=role_embed)

            for emoji in self.reactions2:
                await message.add_reaction(emoji=helpers.find_emoji(emoji))
