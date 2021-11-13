from discord.ext import commands
import discord
from bot import helpers


class bn_interviews(commands.Cog):
    def __init__(self, bot, GUILD_ID, logger):
        self.bot = bot
        self.GUILD_ID = GUILD_ID
        self.logger = logger
        self.INTERVIEWS_ID = 909022516041875487
        self.reactions = [
            "LARGE BLUE CIRCLE",
            "LARGE GREEN CIRCLE",
            "LARGE RED CIRCLE",
        ]

    @commands.command(
        name="new_interview",
        help="Adds a new potential interview [who][from][*details]",
    )
    @commands.has_role("\\n")
    async def new_interview(self, ctx, *args):
        channel = self.bot.get_channel(self.INTERVIEWS_ID)
        if ctx.channel.id != channel.id:
            return False

        content = args[2] + "\n" if len(args) > 2 else ""
        new_interview_embed = discord.Embed(
            title=f"New Interview!",
            description=f"""
            Interviewee: {args[0]}
            Company: {args[1]}
            {content}
            {helpers.find_emoji(self.reactions[0])} - This person has agreed to the interview
            {helpers.find_emoji(self.reactions[1])} - This interview has been completed
            {helpers.find_emoji(self.reactions[2])} - This interview has been cancelled\n
            """,
            color=0xB4E4F9,
        )

        await ctx.message.delete()
        new_message = await channel.send(embed=new_interview_embed)

        for emoji in self.reactions:
            await new_message.add_reaction(emoji=helpers.find_emoji(emoji))

        helpers.command_log(ctx, logger=self.logger)
