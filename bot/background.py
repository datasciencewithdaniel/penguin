import asyncio
from discord.ext import tasks, commands


class background(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.twitch_check())
        self.index = 0

    async def twitch_check(self):
        while True:
            print(self.index)
            self.index += 1
            await asyncio.sleep(2)
            if self.index == 5:
                break
