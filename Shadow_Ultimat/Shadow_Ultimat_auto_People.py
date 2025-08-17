import asyncio
import re
from herokutl.types import Message
import time

VERSION = "1.0.0"
STATE = False

class ShadowUltimatAutoPeople:
    """Автофарм для команды .люди: отправляет команду 'Б', парсит ответ и впускает людей в бункер."""

    def __init__(self, client, db, parent_module):
        self.client = client
        self.db = db
        self.parent_module = parent_module
        self.task = None

    async def start(self):
        """Запуск автофарма, если STATE = True."""
        if STATE and not self.task:
            self.task = asyncio.create_task(self.auto_people())

    async def stop(self):
        """Остановка автофарма."""
        if self.task:
            self.task.cancel()
            self.task = None

    async def auto_people(self):
        """Основной цикл автофарма: отправка 'Б' и обработка ответа."""
        while STATE:
            try:
                # Отправляем команду 'Б' боту @bfgbunker_bot
                await self.client.send_message("@bfgbunker_bot", "Б")
                # Ожидаем ответа от бота (реализуется через watcher в основном модуле)
                # Здесь предполагаем, что ответ обрабатывается в watcher
                await asyncio.sleep(1800)  # Ждём 30 минут до следующей итерации
            except Exception as e:
                print(f"Ошибка в автофарме людей: {str(e)}")
                await asyncio.sleep(60)  # Ждём 1 минуту перед повтором в случае ошибки

    async def watcher(self, message: Message):
        """Обработка сообщений от бота @bfgbunker_bot."""
        if not STATE:
            return

        # Проверяем, что сообщение от @bfgbunker_bot и содержит нужные данные
        if message.from_user.username == "bfgbunker_bot" and "Макс. вместимость людей" in message.text:
            try:
                # Парсим данные из сообщения
                max_capacity = int(re.search(r"Макс\. вместимость людей: (\d+)", message.text).group(1))
                current_people = int(re.search(r"Людей в бункере: (\d+)", message.text).group(1))
                queue = int(re.search(r"Людей в очереди в бункер: (\d+)/\d+", message.text).group(1))

                # Рассчитываем, сколько людей можно впустить
                free_slots = max_capacity - current_people  # Свободные места
                people_to_admit = min(queue, free_slots)  # Впускать не больше, чем очередь или свободные места

                if people_to_admit > 0:
                    # Отправляем команду 'Впустить X'
                    await self.client.send_message("@bfgbunker_bot", f"Впустить {people_to_admit}")
                    print(f"Отправлена команда: Впустить {people_to_admit}")
                else:
                    print("Нет людей для впуска (очередь пуста или бункер полон).")

            except Exception as e:
                print(f"Ошибка при парсинге ответа бота: {str(e)}")
