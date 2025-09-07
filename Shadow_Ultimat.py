__version__ = (7, 7, 7, 0, 1, 0)
# meta developer: @shadow_mod777

import logging
import time
import asyncio
import typing
import re
from telethon.tl.functions.messages import ReadMentionsRequest
from telethon.tl.types import Message as TelethonMessage
from .. import loader, utils
from ..inline.types import InlineCall

# Настройка логирования
logger = logging.getLogger(__name__)

@loader.tds
class Shadow_Ultimat(loader.Module):
    """Афто фарм Бфгб от #тени"""
    
    strings = {
        "name": "Shadow_Ultimat",
        "header": (
            "📓  | Shadow_Ultimat | ~ [ v777 ] \n"
            "╔═╣═════————═══════╗\n"
            "╠══╣══&lt;🕷ГАЙД🕷&gt;════╣\n"
            "╚═╣═════————══════╝"
        ),
        "version_header": (
            "📓  | Shadow_Ultimat | ~ [ v777 ] \n"
            "╔═╣═════————═══════╗\n"
            "╠══╣═&lt;🕷Версия🕷&gt;════╣\n"
            "╚═╣═════————══════╝"
        ),
        "main_menu": "⚙ Нажми на кнопку ниже...",
        "section_1": (
            "🛢 Авто Бензин:\n"
            "⚙ Инструкция для запуска:\n"
            "1⃣ Через fcfg: <code>{prefix}fcfg Shadow_Ultimat Auto_Бензин on/off</code>\n"
            "2⃣ Через команду: <code>{prefix}бензин</code>\n"
            "( Выведит: 🛢 Авто Бензин: ✅/❌ )"
        ),
        "section_2": (
            "👫 Авто Люди:\n"
            "⚙ Инструкция для запуска:\n"
            "1⃣ Через fcfg: <code>{prefix}fcfg Shadow_Ultimat Auto_Люди on/off</code>\n"
            "2⃣ Через команду: <code>{prefix}люди</code>\n"
            "( Выведит: 👫 Авто Люди: ✅/❌ )"
        ),
        "section_3": (
            "🎁 Авто Бонус:\n"
            "⚙ Инструкция для запуска:\n"
            "1⃣ Через fcfg: <code>{prefix}fcfg Shadow_Ultimat Auto_Бонус on/off</code>\n"
            "2⃣ Через команду: <code>{prefix}бонус</code>\n"
            "( Выведит: 🎁 Авто Бонус: ✅/❌ )"
        ),
        "section_4": (
            "🌱 Авто Теплица:\n"
            "⚙ Инструкция для запуска:\n"
            "1⃣ Через fcfg: <code>{prefix}fcfg Shadow_Ultimat Auto_Теплица on/off</code>\n"
            "2⃣ Через команду: <code>{prefix}теплица</code>\n"
            "( Выведит: 🌱 Авто Теплица: ✅/❌ )"
        ),
        "section_5": "♠️♥️ Просмотр Профиля ...",
        "section_6": (
            "👜 Просмотр Людей:\n"
            "⚙ Инструкция для запуска:\n"
            "1⃣ Через реплей на сообщение @bfgbunker_bot: <code>{prefix}вл</code>\n"
            "( Выведит: 👜 Вместимость: текущие люди, макс. вместимость, открытые комнаты. 🆙 — комната с минимальной вместимостью )"
        ),
        "section_7": (
            "🏛 Авто Гильдия:\n"
            "⚙ Инструкция для запуска:\n"
            "⚙ Авто-банки: ✔️ / ✖️ \n⚙ Авто-бутылки: ✔️ / ✖️ \n⚙ Авто-атака-ги: ✔️ / ✖️ \n⚙ Авто-атака-босса: ✔️ / ✖️ \n⚙ Авто-закуп: ✔️ / ✖️ \n"
            "1⃣ Через fcfg: <code>{prefix}fcfg Shadow_Ultimat Auto_Гильдия_банки on/off</code>\n"
            "2️⃣ Через fcfg: <code>{prefix}fcfg Shadow_Ultimat Auto_Гильдия_бутылки on/off</code>\n"
            "3️⃣ Через fcfg: <code>{prefix}fcfg Shadow_Ultimat Auto_Гильдия_атака_ги on/off</code>\n"
            "4️⃣ Через fcfg: <code>{prefix}fcfg Shadow_Ultimat Auto_Гильдия_атака_босса on/off</code>\n"
            "5️⃣ Через fcfg: <code>{prefix}fcfg Shadow_Ultimat Auto_Гильдия_закуп on/off</code>\n"
            "6️⃣ Через команду: <code>{prefix}гильдия</code>\n"
            "( Выведит: 🏛 Авто Гильдия: ✅/❌ )"
        ),
        "section_8": (
            "⛏ Авто Шахта:\n"
            "⚙ Инструкция для запуска:\n"
            "1⃣ Через fcfg: <code>{prefix}fcfg Shadow_Ultimat Auto_Шахта on/off</code>\n"
            "2⃣ Через команду: <code>{prefix}шахта</code>\n"
            "( Выведит: ⛏ Авто Шахта: ✅/❌ )"
        ),
        "section_9": (
            "🌳 Авто Сад:\n"
            "⚙ Инструкция для запуска:\n"
            "1⃣ Через fcfg: <code>{prefix}fcfg Shadow_Ultimat Auto_Сад on/off</code>\n"
            "2⃣ Через команду: <code>{prefix}сад</code>\n"
            "( Выведит: 🌳 Авто Сад: ✅/❌ )"
        ),
        "section_10": (
            "🏜 Авто Пустошь:\n"
            "⚙ Инструкция для запуска:\n"
            "1⃣ Через fcfg: <code>{prefix}fcfg Shadow_Ultimat Auto_Пустошь on/off</code>\n"
            "2⃣ Через команду: <code>{prefix}пустошь</code>\n"
            "( Выведит: 🏜 Авто Пустошь: ✅/❌ )"
        ),
        "section_11": (
            "🍾 Просмотр 5%:\n"
            "⚙ Инструкция для запуска:\n"
            "1⃣ Через реплей: <code>{prefix}g5</code>"
        ),
        "back_button": "⬅️ Назад к гайду",
        "auto_benzin_on": "🛢 Авто Бензин: ✅",
        "auto_benzin_off": "🛢 Авто Бензин: ❌",
        "auto_people_on": "👫 Авто Люди: ✅",
        "auto_people_off": "👫 Авто Люди: ❌",
        "auto_bonus_on": "🎁 Авто Бонус: ✅",
        "auto_bonus_off": "🎁 Авто Бонус: ❌",
        "auto_greenhouse_on": "🌱 Авто Теплица: ✅",
        "auto_greenhouse_off": "🌱 Авто Теплица: ❌",
        "auto_guild_on": "🏛 Авто Гильдия: ✅",
        "auto_guild_off": "🏛 Авто Гильдия: ❌",
        "auto_mine_on": "⛏ Авто Шахта: ✅",
        "auto_mine_off": "⛏ Авто Шахта: ❌",
        "auto_garden_on": "🌳 Авто Сад: ✅",
        "auto_garden_off": "🌳 Авто Сад: ❌",
        "auto_wasteland_on": "🏜 Авто Пустошь: ✅",
        "auto_wasteland_off": "🏜 Авто Пустошь: ❌",
        "version_prev": "⬅️ Предыдущая",
        "version_next": "Следующая ➡️",
        "no_reply": "<b>Ответь на сообщение с информацией о бутылках!</b>",
        "invalid_multiplier": "<b>Второй аргумент должен быть числом!</b>",
        "capacity_template": (
            "📓  | Shadow_Ultimat | ~ [ v777 ]\n"
            "╔═╣════════════════╗\n"
            "║  🔻СТАТУС |💣| BFGB🔻\n"
            "╠══════════════════╣\n"
            "║~$ 👜 Вместимость\n"
            "╠══════════════════╣\n"
            "{rooms}\n"
            "╠══════════════════╣\n"
            "║~$ 👥 Людей сейчас: {current_people}\n"
            "║~$ 📊 Макс. мест: {max_capacity}\n"
            "║~$ 🚪 Открыто: {open_rooms}/18\n"
            "║~$ {overflow_warning}\n"
            "╠══════════════════╣\n"
            "║👁‍🗨 Команда:\n"
            "╠═╣<code>{prefix}вл</code> - Людей в бункере\n"
            "╚═══════════════════"
        ),
        "room_active": "║~$ 🔹 K{room_num} - {capacity} чел.{upgrade}",
        "room_inactive": "║~$ 🔻 K{room_num} - {capacity} чел.{upgrade}",
        "capacity_error": "<b>Не удалось получить данные о бункере. Попробуйте позже.</b>",
        "no_reply_vl": "<b>Ответьте на сообщение от @bfgbunker_bot для обработки статистики бункера.</b>",
        "invalid_reply_vl": "<b>Сообщение, на которое вы ответили, не содержит корректной статистики бункера.</b>",
        "db_cleared": "<b>База данных модуля Shadow_Ultimat успешно очищена!</b>",
        "db_clear_error": "<b>Ошибка при очистке базы данных: {error}</b>"
    }

    class OnOffValidator(loader.validators.Validator):
        """Валидатор для значений on/off, хранит строку 'on'/'off'"""
        def __init__(self):
            super().__init__(self._validate, {"en": "on/off", "ru": "вкл/выкл"})

        @staticmethod
        def _validate(value: typing.Any) -> str:
            if isinstance(value, str) and value.lower() in ["on", "off"]:
                return value.lower()
            raise loader.validators.ValidationError("Значение должно быть 'on' или 'off'")

        def _clean(self, value: str) -> str:
            return "вкл" if value == "on" else "выкл"

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("Auto_Бензин", "off", "Включить/выключить авто бензин (on/off)", validator=self.OnOffValidator()),
            loader.ConfigValue("Auto_Люди", "off", "Включить/выключить авто люди (on/off)", validator=self.OnOffValidator()),
            loader.ConfigValue("Auto_Бонус", "off", "Включить/выключить авто бонус (on/off)", validator=self.OnOffValidator()),
            loader.ConfigValue("Auto_Теплица", "off", "Включить/выключить авто теплица (on/off)", validator=self.OnOffValidator()),
            loader.ConfigValue("Auto_Гильдия_банки", "off", "Включить/выключить авто гильдия банки (on/off)", validator=self.OnOffValidator()),
            loader.ConfigValue("Auto_Гильдия_бутылки", "off", "Включить/выключить авто гильдия бутылки (on/off)", validator=self.OnOffValidator()),
            loader.ConfigValue("Auto_Гильдия_атака_ги", "off", "Включить/выключить авто гильдия атака ги (on/off)", validator=self.OnOffValidator()),
            loader.ConfigValue("Auto_Гильдия_атака_босса", "off", "Включить/выключить авто гильдия атака босса (on/off)", validator=self.OnOffValidator()),
            loader.ConfigValue("Auto_Гильдия_закуп", "off", "Включить/выключить авто гильдия закуп (on/off)", validator=self.OnOffValidator()),
            loader.ConfigValue("Auto_Шахта", "off", "Включить/выключить авто шахта (on/off)", validator=self.OnOffValidator()),
            loader.ConfigValue("Auto_Сад", "off", "Включить/выключить авто сад (on/off)", validator=self.OnOffValidator()),
            loader.ConfigValue("Auto_Пустошь", "off", "Включить/выключить авто пустошь (on/off)", validator=self.OnOffValidator())
        )
        self.bot = "@bfgbunker_bot"
        self.formatted_strings = {}
        self.version_history = [
            {
                "version": (7, 7, 7, 0, 0, 0),
                "description": "Была создана бета версия команды гайд",
                "formatted": "🗃 Была добавлена команда <code>{prefix}гайд</code>"
            },
            {
                "version": (7, 7, 7, 0, 0, 1),
                "description": "Была создана информация для авто Бензин",
                "formatted": "🗃 Была добавлена информация для авто Бензин с командой <code>{prefix}бензин</code>"
            },
            {
                "version": (7, 7, 7, 0, 0, 2),
                "description": "Была создана команда .версия которая показывает всё версии, патчи и фиксы и бета",
                "formatted": "🗃 Была создана команда <code>{prefix}версия</code> для отображения версий, патчей, фиксов и бета"
            },
            {
                "version": (7, 7, 7, 0, 0, 3),
                "description": "Добавлены команды и настройки для всех авто-фармов в гайд",
                "formatted": (
                    "🗃 Добавлены команды и настройки для всех авто-фармов:\n"
                    "<code>{prefix}люди</code>, <code>{prefix}бонус</code>, <code>{prefix}теплица</code>, "
                    "<code>{prefix}гильдия</code>, <code>{prefix}шахта</code>, <code>{prefix}сад</code>, "
                    "<code>{prefix}пустошь</code>"
                )
            },
            {
                "version": (7, 7, 7, 0, 0, 4),
                "description": "Добавлена механика просмотра 5% в гильдии",
                "formatted": "🗃 Добавлена команда <code>{prefix}g5</code> для просмотра статистики 5% в гильдии"
            },
            {
                "version": (7, 7, 7, 0, 0, 5),
                "description": "Добавлен функционал для просмотра вместимости людей в бункере",
                "formatted": "🗃 Добавлена команда <code>{prefix}вл</code> для просмотра количества людей и вместимости комнат в бункере"
            },
            {
                "version": (7, 7, 7, 0, 0, 6),
                "description": "Обновлен дизайн команды .вл с отображением всех 18 комнат и индикатором 🆙 для комнаты с минимальной вместимостью",
                "formatted": "🗃 Обновлен дизайн команды <code>{prefix}вл</code> с отображением всех 18 комнат и индикатором 🆙 для комнаты с минимальной вместимостью"
            },
            {
                "version": (7, 7, 7, 0, 0, 7),
                "description": "Исправлен вывод команды .вл: показываются только комнаты из профиля, 🔻 для комнат с ❗️, 🆙 для минимальной вместимости",
                "formatted": "🗃 Исправлен вывод команды <code>{prefix}вл</code>: показываются только комнаты из профиля, 🔻 для комнат с ❗️, 🆙 для минимальной вместимости"
            },
            {
                "version": (7, 7, 7, 0, 0, 8),
                "description": "Обновлен дизайн команды .вл с единым блоком цитирования и отправкой новым сообщением",
                "formatted": "🗃 Обновлен дизайн команды <code>{prefix}вл</code> с единым блоком цитирования и отправкой новым сообщением"
            },
            {
                "version": (7, 7, 7, 0, 0, 9),
                "description": "Исправлена синтаксическая ошибка в g5cmd, связанная с некорректным использованием enforce_newline",
                "formatted": "🗃 Исправлена синтаксическая ошибка в команде <code>{prefix}g5</code>, связанная с некорректным использованием enforce_newline"
            },
            {
                "version": (7, 7, 7, 0, 1, 0),
                "description": "Добавлен функционал авто-фарма бензина",
                "formatted": "🗃 Добавлен авто-фарм бензина с проверкой по таймеру каждые 3629 секунд"
            }
        ]
        self.result_list = []
        self.monday_bottles_list = []
        self.five_percent_bonus_list = []
        self.total_bottles = 0
        self.total_monday_bottles = 0
        self.total_five_percent_bonus = 0
        self.total_bottles_str = ""
        self.total_monday_bottles_str = ""
        self.total_five_percent_bonus_str = ""

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.prefix = (
            self.db.get("hikka.main", "command_prefix", None) or
            self.db.get("heroku.main", "command_prefix", ".")
        )
        for i in range(1, 12):
            self.formatted_strings[f"section_{i}"] = self.strings[f"section_{i}"].format(prefix=self.prefix)
        for version_info in self.version_history:
            version_info["formatted"] = version_info["formatted"].format(prefix=self.prefix)

    async def _fuel(self, conv):
        """Метод для авто-фарма бензина"""
        try:
            await asyncio.sleep(2)
            await conv.send_message('Бензин')
            r = await conv.get_response()
            await asyncio.sleep(1)
            if r.buttons:
                await r.click(0)
            await self.client(ReadMentionsRequest(self.bot))
        except Exception as e:
            logger.error(f"Ошибка в авто-фарме бензина: {e}")

    async def _people(self, conv):
        """Метод для авто-фарма людей"""
        try:
            await asyncio.sleep(2)
            await conv.send_message('Люди')
            r = await conv.get_response()
            await asyncio.sleep(1)
            if r.buttons:
                await r.click(0)
            await self.client(ReadMentionsRequest(self.bot))
        except Exception as e:
            logger.error(f"Ошибка в авто-фарме людей: {e}")

    async def _bonus(self, conv):
        """Метод для авто-фарма бонусов"""
        try:
            await asyncio.sleep(2)
            await conv.send_message('Бонус')
            r = await conv.get_response()
            await asyncio.sleep(1)
            if r.buttons:
                await r.click(0)
            await self.client(ReadMentionsRequest(self.bot))
        except Exception as e:
            logger.error(f"Ошибка в авто-фарме бонусов: {e}")

    async def _greenhouse(self, conv):
        """Метод для авто-фарма теплицы"""
        try:
            await asyncio.sleep(2)
            await conv.send_message('Теплица')
            r = await conv.get_response()
            await asyncio.sleep(1)
            if r.buttons:
                await r.click(0)
            await self.client(ReadMentionsRequest(self.bot))
        except Exception as e:
            logger.error(f"Ошибка в авто-фарме теплицы: {e}")

    async def _guild(self, conv):
        """Метод для авто-фарма гильдии"""
        try:
            if self.config["Auto_Гильдия_банки"] == "on":
                await asyncio.sleep(2)
                await conv.send_message('Банки')
                r = await conv.get_response()
                await asyncio.sleep(1)
                if r.buttons:
                    await r.click(0)
            if self.config["Auto_Гильдия_бутылки"] == "on":
                await asyncio.sleep(2)
                await conv.send_message('Бутылки')
                r = await conv.get_response()
                await asyncio.sleep(1)
                if r.buttons:
                    await r.click(0)
            if self.config["Auto_Гильдия_атака_ги"] == "on":
                await asyncio.sleep(2)
                await conv.send_message('Атака ги')
                r = await conv.get_response()
                await asyncio.sleep(1)
                if r.buttons:
                    await r.click(0)
            if self.config["Auto_Гильдия_атака_босса"] == "on":
                await asyncio.sleep(2)
                await conv.send_message('Атака босса')
                r = await conv.get_response()
                await asyncio.sleep(1)
                if r.buttons:
                    await r.click(0)
            if self.config["Auto_Гильдия_закуп"] == "on":
                await asyncio.sleep(2)
                await conv.send_message('Закуп')
                r = await conv.get_response()
                await asyncio.sleep(1)
                if r.buttons:
                    await r.click(0)
            await self.client(ReadMentionsRequest(self.bot))
        except Exception as e:
            logger.error(f"Ошибка в авто-фарме гильдии: {e}")

    async def _mine(self, conv):
        """Метод для авто-фарма шахты"""
        try:
            await asyncio.sleep(2)
            await conv.send_message('Шахта')
            r = await conv.get_response()
            await asyncio.sleep(1)
            if r.buttons:
                await r.click(0)
            await self.client(ReadMentionsRequest(self.bot))
        except Exception as e:
            logger.error(f"Ошибка в авто-фарме шахты: {e}")

    async def _garden(self, conv):
        """Метод для авто-фарма сада"""
        try:
            await asyncio.sleep(2)
            await conv.send_message('Сад')
            r = await conv.get_response()
            await asyncio.sleep(1)
            if r.buttons:
                await r.click(0)
            await self.client(ReadMentionsRequest(self.bot))
        except Exception as e:
            logger.error(f"Ошибка в авто-фарме сада: {e}")

    async def _wasteland(self, conv):
        """Метод для авто-фарма пустоши"""
        try:
            await asyncio.sleep(2)
            await conv.send_message('Пустошь')
            r = await conv.get_response()
            await asyncio.sleep(1)
            if r.buttons:
                await r.click(0)
            await self.client(ReadMentionsRequest(self.bot))
        except Exception as e:
            logger.error(f"Ошибка в авто-фарме пустоши: {e}")

    async def watcher(self, message: TelethonMessage):
        """Основной цикл для авто-фарма с индивидуальными кулдаунами"""
        while True:
            try:
                # Проверяем, есть ли активные авто-фармы, готовые к выполнению
                tasks = []
                current_time = time.time()

                # Авто Бензин
                if self.config["Auto_Бензин"] == "on":
                    fuel_time = self.db.get("Shadow_Ultimat", "fuel_time", 0)
                    if not fuel_time or (current_time - fuel_time) >= 3629:
                        tasks.append(("fuel", self._fuel, 3629))

                # Авто Люди
                if self.config["Auto_Люди"] == "on":
                    people_time = self.db.get("Shadow_Ultimat", "people_time", 0)
                    if not people_time or (current_time - people_time) >= 3600:
                        tasks.append(("people", self._people, 3600))

                # Авто Бонус
                if self.config["Auto_Бонус"] == "on":
                    bonus_time = self.db.get("Shadow_Ultimat", "bonus_time", 0)
                    if not bonus_time or (current_time - bonus_time) >= 7200:
                        tasks.append(("bonus", self._bonus, 7200))

                # Авто Теплица
                if self.config["Auto_Теплица"] == "on":
                    greenhouse_time = self.db.get("Shadow_Ultimat", "greenhouse_time", 0)
                    if not greenhouse_time or (current_time - greenhouse_time) >= 3600:
                        tasks.append(("greenhouse", self._greenhouse, 3600))

                # Авто Гильдия
                if any(self.config[key] == "on" for key in [
                    "Auto_Гильдия_банки", "Auto_Гильдия_бутылки", 
                    "Auto_Гильдия_атака_ги", "Auto_Гильдия_атака_босса", 
                    "Auto_Гильдия_закуп"
                ]):
                    guild_time = self.db.get("Shadow_Ultimat", "guild_time", 0)
                    if not guild_time or (current_time - guild_time) >= 3600:
                        tasks.append(("guild", self._guild, 3600))

                # Авто Шахта
                if self.config["Auto_Шахта"] == "on":
                    mine_time = self.db.get("Shadow_Ultimat", "mine_time", 0)
                    if not mine_time or (current_time - mine_time) >= 3600:
                        tasks.append(("mine", self._mine, 3600))

                # Авто Сад
                if self.config["Auto_Сад"] == "on":
                    garden_time = self.db.get("Shadow_Ultimat", "garden_time", 0)
                    if not garden_time or (current_time - garden_time) >= 3600:
                        tasks.append(("garden", self._garden, 3600))

                # Авто Пустошь
                if self.config["Auto_Пустошь"] == "on":
                    wasteland_time = self.db.get("Shadow_Ultimat", "wasteland_time", 0)
                    if not wasteland_time or (current_time - wasteland_time) >= 3600:
                        tasks.append(("wasteland", self._wasteland, 3600))

                # Если есть задачи, открываем сессию conversation и выполняем их
                if tasks:
                    async with self.client.conversation(self.bot, timeout=30) as conv:
                        for task_name, task_func, cooldown in tasks:
                            await task_func(conv)
                            self.db.set("Shadow_Ultimat", f"{task_name}_time", int(time.time()))

                await asyncio.sleep(60)  # Проверка каждую минуту
            except Exception as e:
                logger.error(f"Ошибка в цикле watcher: {e}")
                await asyncio.sleep(60)

    async def гайдcmd(self, message: TelethonMessage):
        """Показать гайд Shadow_Ultimat"""
        await utils.answer(
            message,
            f"<blockquote>{self.strings['header']}\n{self.strings['main_menu']}</blockquote>",
            reply_markup=self._get_main_menu()
        )

    async def бензинcmd(self, message: TelethonMessage):
        """Включить/выключить или показать статус Авто Бензин"""
        current_state = self.config["Auto_Бензин"]
        self.config["Auto_Бензин"] = "on" if current_state == "off" else "off"
        state_str = self.strings["auto_benzin_on"] if self.config["Auto_Бензин"] == "on" else self.strings["auto_benzin_off"]
        await utils.answer(message, state_str)

    async def людиcmd(self, message: TelethonMessage):
        """Включить/выключить или показать статус Авто Люди"""
        current_state = self.config["Auto_Люди"]
        self.config["Auto_Люди"] = "on" if current_state == "off" else "off"
        state_str = self.strings["auto_people_on"] if self.config["Auto_Люди"] == "on" else self.strings["auto_people_off"]
        await utils.answer(message, state_str)

    async def бонусcmd(self, message: TelethonMessage):
        """Включить/выключить или показать статус Авто Бонус"""
        current_state = self.config["Auto_Бонус"]
        self.config["Auto_Бонус"] = "on" if current_state == "off" else "off"
        state_str = self.strings["auto_bonus_on"] if self.config["Auto_Бонус"] == "on" else self.strings["auto_bonus_off"]
        await utils.answer(message, state_str)

    async def теплицаcmd(self, message: TelethonMessage):
        """Включить/выключить или показать статус Авто Теплица"""
        current_state = self.config["Auto_Теплица"]
        self.config["Auto_Теплица"] = "on" if current_state == "off" else "off"
        state_str = self.strings["auto_greenhouse_on"] if self.config["Auto_Теплица"] == "on" else self.strings["auto_greenhouse_off"]
        await utils.answer(message, state_str)

    async def гильдияcmd(self, message: TelethonMessage):
        """Включить/выключить или показать статус Авто Гильдия"""
        current_state = self.config["Auto_Гильдия_банки"]
        self.config["Auto_Гильдия_банки"] = "on" if current_state == "off" else "off"
        self.config["Auto_Гильдия_бутылки"] = "on" if current_state == "off" else "off"
        self.config["Auto_Гильдия_атака_ги"] = "on" if current_state == "off" else "off"
        self.config["Auto_Гильдия_атака_босса"] = "on" if current_state == "off" else "off"
        self.config["Auto_Гильдия_закуп"] = "on" if current_state == "off" else "off"
        state_str = self.strings["auto_guild_on"] if self.config["Auto_Гильдия_банки"] == "on" else self.strings["auto_guild_off"]
        await utils.answer(message, state_str)

    async def шахтаcmd(self, message: TelethonMessage):
        """Включить/выключить или показать статус Авто Шахта"""
        current_state = self.config["Auto_Шахта"]
        self.config["Auto_Шахта"] = "on" if current_state == "off" else "off"
        state_str = self.strings["auto_mine_on"] if self.config["Auto_Шахта"] == "on" else self.strings["auto_mine_off"]
        await utils.answer(message, state_str)

    async def садcmd(self, message: TelethonMessage):
        """Включить/выключить или показать статус Авто Сад"""
        current_state = self.config["Auto_Сад"]
        self.config["Auto_Сад"] = "on" if current_state == "off" else "off"
        state_str = self.strings["auto_garden_on"] if self.config["Auto_Сад"] == "on" else self.strings["auto_garden_off"]
        await utils.answer(message, state_str)

    async def пустошьcmd(self, message: TelethonMessage):
        """Включить/выключить или показать статус Авто Пустошь"""
        current_state = self.config["Auto_Пустошь"]
        self.config["Auto_Пустошь"] = "on" if current_state == "off" else "off"
        state_str = self.strings["auto_wasteland_on"] if self.config["Auto_Пустошь"] == "on" else self.strings["auto_wasteland_off"]
        await utils.answer(message, state_str)

    async def версияcmd(self, message: TelethonMessage):
        """Показать историю версий Shadow_Ultimat"""
        current_version_index = len(self.version_history) - 1
        version_info = self.version_history[current_version_index]
        version_str = ".".join(map(str, version_info["version"]))
        message_text = (
            f"{self.strings['version_header']}\n"
            f"🛟: v{version_str}\n"
            f"{version_info['formatted']}"
        )
        await utils.answer(
            message,
            f"<blockquote>{message_text}</blockquote>",
            reply_markup=self._get_version_buttons(current_version_index)
        )

    async def g5cmd(self, message: TelethonMessage):
        """Показать статистику гильдии по бутылкам"""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings["no_reply"])
            return

        args = utils.get_args(message)
        if args and len(args) > 0:
            try:
                multiplier = float(args[0])
            except ValueError:
                await utils.answer(message, self.strings["invalid_multiplier"])
                return
        else:
            multiplier = 1.2

        self.result_list = []
        self.monday_bottles_list = []
        self.five_percent_bonus_list = []
        self.total_bottles = 0
        self.total_monday_bottles = 0
        self.total_five_percent_bonus = 0

        for line in reply.text.splitlines():
            if " - " in line:
                parts = line.split(" - ")
                nick = parts[0].strip()
                bottles_str = parts[1].strip()[:-1]  # Remove 🍾
                bottles_str = bottles_str.replace('.', '')  # Remove dots
                try:
                    bottles = int(bottles_str) // 10
                except ValueError:
                    continue
                self.total_bottles += bottles
                bottles_str = self.format_number(bottles)
                self.result_list.append(f"║~$ [{nick} - {bottles_str} 🍾]")

                monday_bottles = int(bottles * multiplier)
                self.total_monday_bottles += monday_bottles
                monday_bottles_str = self.format_number(monday_bottles)
                self.monday_bottles_list.append(f"║~$ [{nick} - {monday_bottles_str} 🍾]")

                five_percent_bonus = int(monday_bottles / 20)
                self.total_five_percent_bonus += five_percent_bonus
                five_percent_bonus_str = self.format_number(five_percent_bonus)
                self.five_percent_bonus_list.append(f"║~$ [{nick} - {five_percent_bonus_str} 🍾]")

        self.total_bottles_str = self.format_number(self.total_bottles)
        self.total_monday_bottles_str = self.format_number(self.total_monday_bottles)
        self.total_five_percent_bonus_str = self.format_number(self.total_five_percent_bonus)

        total_bottles_format = (
            f"║~$ 📊 Макс. {self.total_bottles_str} 🍾"
            if self.total_bottles <= 9999
            else f"║~$ 📊 Макс. бутылок:\n║~$ {self.total_bottles_str} 🍾"
        )

        result_message = (
            "📓  | Shadow_Ultimat | ~ [ v777 ]\n"
            "╔═╣════════════════╗\n"
            "║  🔻СТАТУС |💣| BFGB🔻\n"
            "╠══════════════════╣\n"
            "║~$  📊 Статистика 📊\n"
            "║  ( За текущую неделю )\n"
            "╠══════════════════╣\n"
            + "\n".join(self.result_list) +
            "\n╠══════════════════╣\n"
            f"{total_bottles_format}\n"
            "╠══════════════════╣\n"
            "║👁‍🗨 Команда:\n"
            f"╠═╣{self.prefix}g5 - стата в гильдии\n"
            "╚═══════════════════"
        )

        await self.inline.form(
            text=f"<blockquote>{result_message}</blockquote>",
            message=message,
            reply_markup=[
                [
                    {"text": "📊 Проценты", "callback": self.five_percent},
                    {"text": "📊 Понедельник", "callback": self.monday}
                ]
            ]
        )

    async def five_percent(self, call: InlineCall):
        total_five_percent_format = (
            f"║~$ 📊 Всего в 5% — {self.total_five_percent_bonus_str} 🍾"
            if self.total_five_percent_bonus <= 9999
            else f"║~$ 📊 Всего в 5%:\n║~$ {self.total_five_percent_bonus_str} 🍾"
        )

        result_message = (
            "📓  | Shadow_Ultimat | ~ [ v777 ]\n"
            "╔═╣════════════════╗\n"
            "║  🔻СТАТУС |💣| BFGB🔻\n"
            "╠══════════════════╣\n"
            "║~$  📊 Статистика 📊\n"
            "║             ( 5% в ПН )\n"
            "╠══════════════════╣\n"
            + "\n".join(self.five_percent_bonus_list) +
            "\n╠══════════════════╣\n"
            f"{total_five_percent_format}\n"
            "╠══════════════════╣\n"
            "║👁‍🗨 Команда:\n"
            f"╠═╣{self.prefix}g5 - стата в гильдии\n"
            "╚═══════════════════"
        )
        await call.edit(
            f"<blockquote>{result_message}</blockquote>",
            reply_markup=[
                [{"text": "⬅️ Назад", "callback": self.back}]
            ]
        )

    async def monday(self, call: InlineCall):
        total_monday_format = (
            f"║~$ 📊 Макс. в пн — {self.total_monday_bottles_str} 🍾"
            if self.total_monday_bottles <= 9999
            else f"║~$ 📊 Макс. в пн:\n║~$ {self.total_monday_bottles_str} 🍾"
        )

        result_message = (
            "📓  | Shadow_Ultimat | ~ [ v777 ]\n"
            "╔═╣════════════════╗\n"
            "║  🔻СТАТУС |💣| BFGB🔻\n"
            "╠══════════════════╣\n"
            "║~$  📊 Статистика 📊\n"
            "║        ( Понедельник )\n"
            "╠══════════════════╣\n"
            + "\n".join(self.monday_bottles_list) +
            "\n╠══════════════════╣\n"
            f"{total_monday_format}\n"
            "╠══════════════════╣\n"
            "║👁‍🗨 Команда:\n"
            f"╠═╣{self.prefix}g5 - стата в гильдии\n"
            "╚═══════════════════"
        )
        await call.edit(
            f"<blockquote>{result_message}</blockquote>",
            reply_markup=[
                [{"text": "⬅️ Назад", "callback": self.back}]
            ]
        )

    async def back(self, call: InlineCall):
        total_bottles_format = (
            f"║~$ 📊 Макс. {self.total_bottles_str} 🍾"
            if self.total_bottles <= 9999
            else f"║~$ 📊 Макс. бутылок:\n║~$ {self.total_bottles_str} 🍾"
        )

        result_message = (
            "📓  | Shadow_Ultimat | ~ [ v777 ]\n"
            "╔═╣════════════════╗\n"
            "║  🔻СТАТУС |💣| BFGB🔻\n"
            "╠══════════════════╣\n"
            "║~$  📊 Статистика 📊\n"
            "║  ( За текущую неделю )\n"
            "╠══════════════════╣\n"
            + "\n".join(self.result_list) +
            "\n╠══════════════════╣\n"
            f"{total_bottles_format}\n"
            "╠══════════════════╣\n"
            "║👁‍🗨 Команда:\n"
            f"╠═╣{self.prefix}g5 - стата в гильдии\n"
            "╚═══════════════════"
        )
        await call.edit(
            f"<blockquote>{result_message}</blockquote>",
            reply_markup=[
                [
                    {"text": "📊 Проценты", "callback": self.five_percent},
                    {"text": "📊 Понедельник", "callback": self.monday}
                ]
            ]
        )

    async def влcmd(self, message: TelethonMessage):
        """Показывает количество людей и вместимость комнат."""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings["no_reply_vl"])
            return
        if reply.sender_id != (await self.client.get_entity(self.bot)).id or not reply.text:
            await utils.answer(message, self.strings["invalid_reply_vl"])
            return

        current_people = re.search(r"🧍 Людей в бункере: <b>(\d+)</b>", reply.text)
        max_capacity = re.search(r"Макс\. вместимость людей: (\d+)", reply.text)
        rooms_section = re.search(r"🏠 Комнаты:([\s\S]*?)(?=(💵 (?:Общая прибыль|Бункер не работает!)|📅|\Z))", reply.text)

        if not (current_people and max_capacity and rooms_section):
            await utils.answer(message, self.strings["invalid_reply_vl"])
            return

        current_people = int(current_people.group(1))
        max_capacity = int(max_capacity.group(1))
        rooms_text = rooms_section.group(1).strip()

        # Базовые вместимости комнат
        base_capacities = [6, 6, 6, 6, 12, 20, 32, 52, 92, 144, 234, 380, 520, 750, 1030, 1430, 2020, 3520]
        rooms = []
        open_rooms = 0

        # Парсинг комнат из сообщения бота
        room_lines = rooms_text.split("\n")
        for line in room_lines:
            line = line.strip()
            if not line:
                continue
            match = re.match(
                r"(?:(1️⃣|2️⃣|3️⃣|4️⃣|5️⃣|6️⃣|7️⃣|8️⃣|9️⃣|🔟|1️⃣[1-8]️⃣))\s*(❗️)?\s*([^\d][^\n]*?)\s*(\d+)\s*ур\.|(?:(1️⃣|2️⃣|3️⃣|4️⃣|5️⃣|6️⃣|7️⃣|8️⃣|9️⃣|🔟|1️⃣[1-8]️⃣))\s*(❗️)?\s*([^\d][^\n]*?)\s*Цена:\s*(\d+)\s*крышек",
                line
            )
            if match:
                room_emoji = match.group(1) or match.group(5)
                room_num_map = {
                    "1️⃣": 1, "2️⃣": 2, "3️⃣": 3, "4️⃣": 4, "5️⃣": 5,
                    "6️⃣": 6, "7️⃣": 7, "8️⃣": 8, "9️⃣": 9, "🔟": 10,
                    "1️⃣1️⃣": 11, "1️⃣2️⃣": 12, "1️⃣3️⃣": 13, "1️⃣4️⃣": 14,
                    "1️⃣5️⃣": 15, "1️⃣6️⃣": 16, "1️⃣7️⃣": 17, "1️⃣8️⃣": 18
                }
                room_num = room_num_map.get(room_emoji)
                if not room_num:
                    continue
                warning = bool(match.group(2) or match.group(6))
                if match.group(4):  # Комната открыта (указан уровень)
                    level = int(match.group(4))
                    capacity = base_capacities[room_num - 1] + 2 * (level - 1)
                    rooms.append({"num": room_num, "warning": warning, "capacity": capacity, "upgrade": ""})
                    open_rooms += 1
                elif match.group(7):  # Комната закрыта (указана цена)
                    capacity = base_capacities[room_num - 1]
                    rooms.append({"num": room_num, "warning": True, "capacity": capacity, "upgrade": ""})
                    open_rooms += 1

        # Сортировка комнат по номеру
        rooms.sort(key=lambda x: x["num"])

        # Определение комнат с минимальной вместимостью
        if rooms:
            min_capacity = min(room["capacity"] for room in rooms)
            for room in rooms:
                if room["capacity"] == min_capacity:
                    room["upgrade"] = " 🆙"

        # Формирование строки комнат
        rooms_str = ""
        for room in rooms:
            room_num = room["num"]
            capacity = room["capacity"]
            warning = room["warning"]
            upgrade = room["upgrade"]
            room_key = "room_inactive" if warning else "room_active"
            rooms_str += self.strings[room_key].format(room_num=room_num, capacity=capacity, upgrade=upgrade) + "\n"

        # Предупреждение о переполнении
        overflow_warning = "⚠️ Бункер переполнен!\n║~$    Улучшите комнаты." if current_people > max_capacity else ""

        formatted_message = self.strings["capacity_template"].format(
            rooms=rooms_str.rstrip("\n"),
            current_people=current_people,
            max_capacity=max_capacity,
            open_rooms=open_rooms,
            overflow_warning=overflow_warning,
            prefix=self.prefix
        )

        await utils.answer(message, f"<blockquote>{formatted_message}</blockquote>", reply_to=reply)

    async def очисткабдcmd(self, message: TelethonMessage):
        """Очистить базу данных модуля Shadow_Ultimat"""
        try:
            # Список ключей, которые нужно удалить
            keys = [
                "fuel_time", "people_time", "bonus_time", "greenhouse_time",
                "guild_time", "mine_time", "garden_time", "wasteland_time"
            ]
            for key in keys:
                self.db.pop("Shadow_Ultimat", key, None)
            await utils.answer(message, self.strings["db_cleared"])
        except Exception as e:
            await utils.answer(message, self.strings["db_clear_error"].format(error=str(e)))

    def format_number(self, number):
        number_str = str(number)
        result = []
        for i in range(len(number_str) - 1, -1, -3):
            result.append(number_str[max(0, i - 2):i + 1])
        return ".".join(reversed(result))

    def _get_main_menu(self) -> typing.List[typing.List[dict]]:
        """Возвращает разметку главного меню с инлайн кнопками в формате 4-4-3"""
        return [
            [
                {"text": "🛢", "callback": self._show_section, "args": (1,)},
                {"text": "👫", "callback": self._show_section, "args": (2,)},
                {"text": "🎁", "callback": self._show_section, "args": (3,)},
                {"text": "🌱", "callback": self._show_section, "args": (4,)}
            ],
            [
                {"text": "♠️♥️", "callback": self._show_section, "args": (5,)},
                {"text": "👜", "callback": self._show_section, "args": (6,)},
                {"text": "🏛", "callback": self._show_section, "args": (7,)},
                {"text": "⛏", "callback": self._show_section, "args": (8,)}
            ],
            [
                {"text": "🌳", "callback": self._show_section, "args": (9,)},
                {"text": "🍾", "callback": self._show_section, "args": (11,)},
                {"text": "🏜", "callback": self._show_section, "args": (10,)}
            ]
        ]

    def _get_back_button(self) -> typing.List[typing.List[dict]]:
        """Возвращает разметку с кнопкой 'Назад к гайду'"""
        return [[
            {"text": self.strings["back_button"], "callback": self._show_main_menu}
        ]]

    def _get_version_buttons(self, current_index: int) -> typing.List[typing.List[dict]]:
        """Возвращает инлайн кнопки для навигации по версиям"""
        buttons = []
        if current_index > 0:
            buttons.append({"text": self.strings["version_prev"], "callback": self._show_version, "args": (current_index - 1,)})
        if current_index < len(self.version_history) - 1:
            buttons.append({"text": self.strings["version_next"], "callback": self._show_version, "args": (current_index + 1,)})
        return [buttons] if buttons else []

    async def _show_section(self, call: InlineCall, section_id: int):
        """Обработчик нажатия на кнопку раздела"""
        section_text = self.formatted_strings[f"section_{section_id}"]
        await call.edit(
            f"<blockquote>{self.strings['header']}\n{section_text}</blockquote>",
            reply_markup=self._get_back_button()
        )

    async def _show_main_menu(self, call: InlineCall):
        """Обработчик нажатия на кнопку 'Назад к гайду'"""
        await call.edit(
            f"<blockquote>{self.strings['header']}\n{self.strings['main_menu']}</blockquote>",
            reply_markup=self._get_main_menu()
        )

    async def _show_version(self, call: InlineCall, version_index: int):
        """Обработчик нажатия на кнопки версий"""
        version_info = self.version_history[version_index]
        version_str = ".".join(map(str, version_info["version"]))
        message_text = (
            f"{self.strings['version_header']}\n"
            f"🛟: v{version_str}\n"
            f"{version_info['formatted']}"
        )
        await call.edit(
            f"<blockquote>{message_text}</blockquote>",
            reply_markup=self._get_version_buttons(version_index)
        )
