import asyncio
from discord.ext import tasks, commands
from datetime import datetime, date, time, timedelta


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

    @staticmethod
    async def stream_date():
        hour = 19
        minute = 25
        current_day = date.today()
        days = background.next_weekday(current_day, 4)
        target = datetime.combine(days, time(hour, minute, 0))
        seconds = (target - datetime.now()).total_seconds()
        await asyncio.sleep(seconds)

        # If 24 hours before -> send message to admin channel
        # if current.weekday() == day - 1 and current.hour == hour - 1 and current.minute == minute:
        #     tomorrow = datetime.combine(current.date() + timedelta(days=1), time(0))
        #     seconds = (tomorrow - current).total_seconds()
        #     await asyncio.sleep(seconds)

        # If emoji is yes -> post message at stream time
        # If emoji is no -> skip to next 24 hours before
        # Sleep in between

    @staticmethod
    def next_weekday(today, weekday):
        days_ahead = weekday - today.isoweekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return today + timedelta(days_ahead)
