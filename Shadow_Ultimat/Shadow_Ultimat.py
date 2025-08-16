from herokutl.types import Message
from .. import loader, utils

@loader.tds
class Shadow_Ultimat(loader.Module):
    """Shadow Ultimat Auto Farm Manager for @bfgbunker_bot"""
    strings = {
        "name": "Shadow_Ultimat",
        "version": "7.7.7",
        "author": "@familiarrrrrr",
        "sh_desc": "Показать статус авто-фермы для @bfgbunker_bot",
        "sh_status": "📓 | Shadow_Ultimat | ~ [ v{} ]\n╔═╣════════════════╗\n║  🔻СТАТУС |💣| BFGB🔻\n╠══════════════════╣\n",
        "sh_people": "║~$ 👫 Люди: {}\n",
        "sh_bonus": "║~$ 🎁 Бонус: {}\n",
        "sh_petrol": "║~$ 🛢 Бензин: {}\n",
        "sh_greenhouse": "║~$ 🌱 Теплица: {}\n",
        "sh_wasteland": "║~$ 🏜 Пустошь: {}\n",
        "sh_garden": "║~$ 🌳 Сад: {}\n",
        "sh_mine": "║~$ ⛏ Шахта: {}\n",
        "sh_guild": "║~$ 🏛 Гильдия: {}\n",
        "sh_commands": "║👁‍🗨 Команды:\n",
        "sh_cmd_template": "╠═╣<code>{}{}</code> - вкл/выкл\n",
        "sh_footer": "╚═══════════════════",
        "pref_desc": "Установить новый префикс",
        "pref_updated": "💻 Ваш префикс был обновлен в подсказках на {}"
    }
    strings_ru = strings

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("version", "7.7.7", "Current module version", validator=loader.validators.String()),
            loader.ConfigValue("prefix", ".", "Current command prefix", validator=loader.validators.String()),
        )
        self.statuses = {
            "people": False,
            "bonus": False,
            "petrol": False,
            "greenhouse": False,
            "wasteland": False,
            "garden": False,
            "mine": False,
            "guild": False
        }
        self._db.set("statuses", self.statuses)
        if not self._db.get("prefix", None):
            self._db.set("prefix", self.config["prefix"])

    def get_prefix(self):
        return self._db.get("prefix", ".")

    @loader.command(ru_doc="Показать статус авто-фермы для @bfgbunker_bot")
    async def sh(self, message: Message):
        """Show auto-farm status for @bfgbunker_bot"""
        statuses = self._db.get("statuses", self.statuses)
        prefix = self.get_prefix()
        status_msg = self.strings["sh_status"].format(self.strings["version"])
        for key, value in statuses.items():
            status_msg += self.strings[f"sh_{key}"].format("✅" if value else "⛔️")
        status_msg += self.strings["sh_commands"]
        for cmd in ["люди", "бонус", "бензин", "теплица", "пустошь", "сад", "шахта", "гильдия"]:
            status_msg += self.strings["sh_cmd_template"].format(prefix, cmd)
        status_msg += self.strings["sh_footer"]
        await utils.answer(message, status_msg)

    @loader.command(ru_doc="Вкл/выкл авто-ферму для людей в @bfgbunker_bot")
    async def люди(self, message: Message):
        """Toggle people auto-farm for @bfgbunker_bot"""
        self._toggle_status("people", message)
    @loader.command(ru_doc="Вкл/выкл авто-ферму для бонусов в @bfgbunker_bot")
    async def бонус(self, message: Message):
        """Toggle bonus auto-farm for @bfgbunker_bot"""
        self._toggle_status("bonus", message)
    @loader.command(ru_doc="Вкл/выкл авто-ферму для бензина в @bfgbunker_bot")
    async def бензин(self, message: Message):
        """Toggle petrol auto-farm for @bfgbunker_bot"""
        self._toggle_status("petrol", message)
    @loader.command(ru_doc="Вкл/выкл авто-ферму для теплицы в @bfgbunker_bot")
    async def теплица(self, message: Message):
        """Toggle greenhouse auto-farm for @bfgbunker_bot"""
        self._toggle_status("greenhouse", message)
    @loader.command(ru_doc="Вкл/выкл авто-ферму для пустоши в @bfgbunker_bot")
    async def пустошь(self, message: Message):
        """Toggle wasteland auto-farm for @bfgbunker_bot"""
        self._toggle_status("wasteland", message)
    @loader.command(ru_doc="Вкл/выкл авто-ферму для сада в @bfgbunker_bot")
    async def сад(self, message: Message):
        """Toggle garden auto-farm for @bfgbunker_bot"""
        self._toggle_status("garden", message)
    @loader.command(ru_doc="Вкл/выкл авто-ферму для шахты в @bfgbunker_bot")
    async def шахта(self, message: Message):
        """Toggle mine auto-farm for @bfgbunker_bot"""
        self._toggle_status("mine", message)
    @loader.command(ru_doc="Вкл/выкл авто-ферму для гильдии в @bfgbunker_bot")
    async def гильдия(self, message: Message):
        """Toggle guild auto-farm for @bfgbunker_bot"""
        self._toggle_status("guild", message)

    def _toggle_status(self, key, message):
        statuses = self._db.get("statuses", self.statuses)
        statuses[key] = not statuses[key]
        self._db.set("statuses", statuses)
        await utils.answer(message, f"Авто-ферма для {key} в @bfgbunker_bot теперь {'включена ✅' if statuses[key] else 'выключена ⛔️'}")

    @loader.command(ru_doc="Установить новый префикс")
    async def pref(self, message: Message):
        """Set a new command prefix"""
        args = utils.get_args(message)
        if not args or len(args) != 1:
            await utils.answer(message, "Использование: .pref <префикс>")
            return
        new_prefix = args[0]
        self._db.set("prefix", new_prefix)
        await utils.answer(message, self.strings["pref_updated"].format(new_prefix))
