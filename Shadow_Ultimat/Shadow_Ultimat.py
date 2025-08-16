from herokutl.types import Message
from .. import loader, utils
import requests
import importlib.util
import os
import sys

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
        "shupdate_desc": "Обновить модули до последней версии",
        "up_to_date": "У вас текущая версия! Обновлений нет.",
        "new_version": "Новая версия доступна! Установите обновление: https://github.com/Nyashka17/Shadow_modules",
        "update_success": "Модули успешно обновлены до версии 7.7.7. Новое: [укажите изменения], Убрано: [укажите удалённое].",
        "update_loading": "Загружаю подмодули с GitHub...",
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
    # ... (other toggle commands remain the same, e.g., бонус, бензин, etc.)

    def _toggle_status(self, key, message):
        statuses = self._db.get("statuses", self.statuses)
        statuses[key] = not statuses[key]
        self._db.set("statuses", statuses)
        await utils.answer(message, f"Авто-ферма для {key} в @bfgbunker_bot теперь {'включена ✅' if statuses[key] else 'выключена ⛔️'}")

    @loader.command(ru_doc="Обновить модули до последней версии")
    async def shupdate(self, message: Message):
        """Update all modules to the latest version for @bfgbunker_bot"""
        await utils.answer(message, self.strings["update_loading"])
        current_version = self.config["version"]
        module_urls = [
            "https://raw.githubusercontent.com/Nyashka17/Shadow_modules/refs/heads/main/Shadow_Ultimat/Shadow_Ultimat.py",
            "https://raw.githubusercontent.com/Nyashka17/Shadow_modules/refs/heads/main/Shadow_Ultimat/Shadow_Ultimat_auto_Bonus.py",
            "https://raw.githubusercontent.com/Nyashka17/Shadow_modules/refs/heads/main/Shadow_Ultimat/Shadow_Ultimat_auto_Garden.py",
            "https://raw.githubusercontent.com/Nyashka17/Shadow_modules/refs/heads/main/Shadow_Ultimat/Shadow_Ultimat_auto_Greenhouse.py",
            "https://raw.githubusercontent.com/Nyashka17/Shadow_modules/refs/heads/main/Shadow_Ultimat/Shadow_Ultimat_auto_Guild.py",
            "https://raw.githubusercontent.com/Nyashka17/Shadow_modules/refs/heads/main/Shadow_Ultimat/Shadow_Ultimat_auto_Mine.py",
            "https://raw.githubusercontent.com/Nyashka17/Shadow_modules/refs/heads/main/Shadow_Ultimat/Shadow_Ultimat_auto_People.py",
            "https://raw.githubusercontent.com/Nyashka17/Shadow_modules/refs/heads/main/Shadow_Ultimat/Shadow_Ultimat_auto_Petrol.py",
            "https://raw.githubusercontent.com/Nyashka17/Shadow_modules/refs/heads/main/Shadow_Ultimat/Shadow_Ultimat_auto_Wasteland.py",
            "https://raw.githubusercontent.com/Nyashka17/Shadow_modules/refs/heads/main/Shadow_Ultimat/Shadow_Ultimat_state_Guild.py",
            "https://raw.githubusercontent.com/Nyashka17/Shadow_modules/refs/heads/main/Shadow_Ultimat/Shadow_Ultimat_state_People.py",
            "https://raw.githubusercontent.com/Nyashka17/Shadow_modules/refs/heads/main/Shadow_Ultimat/Shadow_Ultimat_state_Profile.py",
            "https://raw.githubusercontent.com/Nyashka17/Shadow_modules/refs/heads/main/Shadow_Ultimat/Shadow_Ultimat_update.py"
        ]

        module_dir = os.path.dirname(__file__) or "."
        for url in module_urls:
            filename = os.path.join(module_dir, url.split("/")[-1])
            response = requests.get(url)
            with open(filename, "wb") as f:
                f.write(response.content)

        def reload_module(module_name, file_path):
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            return module

        reload_module("Shadow_Ultimat", os.path.join(module_dir, "Shadow_Ultimat.py"))
        sub_modules = [f"Shadow_Ultimat_{part}" for part in [
            "auto_Bonus", "auto_Garden", "auto_Greenhouse", "auto_Guild",
            "auto_Mine", "auto_People", "auto_Petrol", "auto_Wasteland",
            "state_Guild", "state_People", "state_Profile", "update"
        ]]
        for sub in sub_modules:
            sub_file = os.path.join(module_dir, f"{sub}.py")
            if os.path.exists(sub_file):
                reload_module(sub, sub_file)

        self.config["version"] = "7.7.7"  # Update with actual version if parsed
        await utils.answer(message, self.strings["update_success"])

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

    def get_prefix(self):
        return self._db.get("prefix", ".")
