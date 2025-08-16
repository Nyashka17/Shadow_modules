# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔐 Licensed under the GNU AGPLv3.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: Shadow_Ultimat_update
# Author: @familiarrrrrr
# Commands:
# .check
# .shupdate
# .sh
# .люди
# .бонус
# .бензин
# .теплица
# .пустошь
# .сад
# .шахта
# .гильдия
# .pref
# ---------------------------------------------------------------------------------

# meta pic: https://raw.githubusercontent.com/Nyashka17/Shadow_modules/refs/heads/main/Shadow_Ultimat/update_icon.png
# meta banner: https://raw.githubusercontent.com/Nyashka17/Shadow_modules/refs/heads/main/Shadow_Ultimat/update_banner.jpg
# meta developer: @familiarrrrrr
# scope: hikka_only
# scope: hikka_min 1.3.0

import os
import sys
import requests
import importlib.util
import asyncio
import pathlib
import logging
from datetime import datetime
from herokutl.types import Message
from heroku import loader, utils

@loader.tds
class Shadow_Ultimat_update(loader.Module):
    """Module for managing updates and commands of Shadow_Ultimat and its sub-modules"""
    strings = {
        "name": "Shadow_Ultimat_update",
        "check_desc": "Проверить наличие обновлений",
        "shupdate_desc": "Обновить модули до последней версии",
        "up_to_date": "У вас текущая версия! Обновлений нет.",
        "new_version": "Новая версия доступна! Используйте .shupdate для обновления.",
        "update_loading": "Загружаю обновления с GitHub...",
        "update_success": "👻 Модули успешно обновлены до версии 7.7.8\n———————————————————————————\n🎡 Новое: Обновлённый дизайн для модуля обновлений,\n🎢 Убрано: Старый дизайн больше не используется для модуля Shadow_Ultimat_update.py.",
        "update_error": "Ошибка при обновлении: {}",
        "load_error": "Ошибка при загрузке Shadow_Ultimat: {}"
    }
    strings_ru = strings

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)
        if not self.log.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.log.addHandler(handler)
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "current_version",
                "0.0.0",
                "Current version of the module",
                validator=loader.validators.String()
            )
        )
        self.shadow_ultimat = None
        self.client = None

    async def client_ready(self, client, db):
        """Initialize database and load Shadow_Ultimat"""
        self._db = db
        self.client = client
        self.log.debug("Initializing ShadowUpdate module")
        if "ShadowUpdate" not in self._db:
            self._db["ShadowUpdate"] = {}
            self.log.info("Initialized new ShadowUpdate database entry")
        if "update_log" not in self._db["ShadowUpdate"]:
            self._db["ShadowUpdate"]["update_log"] = "Изначальная установка: 7.7.8"
            self.log.info("Set initial update log")

        self.core_file = os.path.join(pathlib.Path.home(), "Heroku", "loaded_modules", "Shadow_Ultimat.py")
        os.makedirs(os.path.dirname(self.core_file), exist_ok=True)
        self._lock = asyncio.Lock()
        self.log.debug(f"Core file path: {self.core_file}")
        await self._load_core_module()

    async def _load_core_module(self):
        """Загрузка модуля Shadow_Ultimat с GitHub"""
        self.log.debug("Attempting to load Shadow_Ultimat module")
        github_url = "https://raw.githubusercontent.com/Nyashka17/Shadow_modules/refs/heads/main/Shadow_Ultimat/Shadow_Ultimat.py"
        try:
            async with self._lock:
                self.log.debug(f"Fetching from {github_url}")
                response = requests.get(github_url, timeout=10)
                response.raise_for_status()
                with open(self.core_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                self.log.info("Successfully downloaded Shadow_Ultimat.py")
                spec = importlib.util.spec_from_file_location("Shadow_Ultimat", self.core_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.log.debug("Executed module from spec")
                # Initialize Shadow_Ultimat with required parameters
                self.shadow_ultimat = module.Shadow_Ultimat()
                self.shadow_ultimat._db = self._db
                self.shadow_ultimat.client = self.client
                self.shadow_ultimat.config = self.shadow_ultimat.config
                self.log.info("Successfully initialized Shadow_Ultimat module")
        except Exception as e:
            self.shadow_ultimat = None
            self.log.error(f"Failed to load Shadow_Ultimat: {e}")
            # Log error instead of using _last_message
            self.log.error(f"Error loading Shadow_Ultimat: {str(e)}")

    def reload_module(self, module_name, file_path):
        """Перезагрузка модуля из файла"""
        self.log.debug(f"Reloading module: {module_name} from {file_path}")
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        self.log.info(f"Successfully reloaded module: {module_name}")
        return module

    @loader.command(ru_doc="Проверить наличие обновлений")
    async def check(self, message: Message):
        """Check for available updates"""
        self.log.debug("Checking for updates")
        current_version = self.config["current_version"]
        module_dir = os.path.join(pathlib.Path.home(), "Heroku", "loaded_modules")
        main_url = "https://raw.githubusercontent.com/Nyashka17/Shadow_modules/refs/heads/main/Shadow_Ultimat/Shadow_Ultimat.py"
        response = requests.get(main_url)
        content = response.text
        latest_version = "7.7.8"
        if current_version == latest_version:
            await utils.answer(message, self.strings["up_to_date"])
        else:
            await utils.answer(message, self.strings["new_version"])
        self.log.info(f"Version check completed. Current: {current_version}, Latest: {latest_version}")

    @loader.command(ru_doc="Обновить модули до последней версии")
    async def shupdate(self, message: Message):
        """Update all modules to the latest version"""
        self.log.debug("Starting update process")
        await utils.answer(message, self.strings["update_loading"])
        module_dir = os.path.join(pathlib.Path.home(), "Heroku", "loaded_modules")
        os.makedirs(module_dir, exist_ok=True)
        user_id = str(getattr(message, "sender_id", None) or getattr(message, "from_id", None))
        if not user_id:
            await utils.answer(message, "Ошибка: Не удалось определить ID пользователя.")
            self.log.error("Failed to determine user ID from message.")
            return
        try:
            module_urls = [
                "https://raw.githubusercontent.com/Nyashka17/Shadow_modules/refs/heads/main/Shadow_Ultimat/Shadow_Ultimat.py",
                "https://raw.githubusercontent.com/Nyashka17/Shadow_modules/refs/heads/main/Shadow_Ultimat/Shadow_Ultimat_update.py",
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
            ]
            for url in module_urls:
                base_filename = url.split("/")[-1]
                filename_without_ext = os.path.splitext(base_filename)[0]
                filename = os.path.join(module_dir, f"{filename_without_ext}_{user_id}.py")
                self.log.debug(f"Downloading {url} to {filename}")
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(response.text)
                self.log.info(f"Successfully downloaded {filename}")

            main_file = os.path.join(module_dir, f"Shadow_Ultimat_{user_id}.py")
            self.reload_module("Shadow_Ultimat", main_file)
            update_file = os.path.join(module_dir, f"Shadow_Ultimat_update_{user_id}.py")
            self.reload_module("ShadowUpdate", update_file)

            sub_modules = [
                "Shadow_Ultimat_auto_Bonus",
                "Shadow_Ultimat_auto_Garden",
                "Shadow_Ultimat_auto_Greenhouse",
                "Shadow_Ultimat_auto_Guild",
                "Shadow_Ultimat_auto_Mine",
                "Shadow_Ultimat_auto_People",
                "Shadow_Ultimat_auto_Petrol",
                "Shadow_Ultimat_auto_Wasteland",
                "Shadow_Ultimat_state_Guild",
                "Shadow_Ultimat_state_People",
                "Shadow_Ultimat_state_Profile",
            ]
            for sub in sub_modules:
                sub_file = os.path.join(module_dir, f"{sub}_{user_id}.py")
                if os.path.exists(sub_file):
                    self.reload_module(sub, sub_file)

            with open(main_file, "r", encoding="utf-8") as f:
                content = f.read()
                latest_version = "7.7.8"
            self.config["current_version"] = latest_version
            self._db["ShadowUpdate"]["update_log"] = f"Обновлено до {latest_version} в {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.log.info(f"Updated to version {latest_version}")

            await utils.answer(message, self.strings["update_success"])

        except requests.RequestException as e:
            self.log.error(f"Request error during update: {str(e)}")
            await utils.answer(message, self.strings["update_error"].format(str(e)))
        except Exception as e:
            self.log.error(f"Unexpected error during update: {str(e)}")
            await utils.answer(message, self.strings["update_error"].format(str(e)))

    @loader.command(ru_doc="Показать статус авто-фермы для @bfgbunker_bot")
    async def sh(self, message: Message):
        """Show auto-farm status for @bfgbunker_bot"""
        if self.shadow_ultimat:
            await self.shadow_ultimat.sh(message)
        else:
            await utils.answer(message, self.strings["load_error"].format("Shadow_Ultimat не загружен"))

    @loader.command(ru_doc="Вкл/выкл авто-ферму для людей в @bfgbunker_bot")
    async def люди(self, message: Message):
        """Toggle people auto-farm for @bfgbunker_bot"""
        if self.shadow_ultimat:
            await self.shadow_ultimat.люди(message)
        else:
            await utils.answer(message, self.strings["load_error"].format("Shadow_Ultimat не загружен"))

    @loader.command(ru_doc="Вкл/выкл авто-ферму для бонусов в @bfgbunker_bot")
    async def бонус(self, message: Message):
        """Toggle bonus auto-farm for @bfgbunker_bot"""
        if self.shadow_ultimat:
            await self.shadow_ultimat.бонус(message)
        else:
            await utils.answer(message, self.strings["load_error"].format("Shadow_Ultimat не загружен"))

    @loader.command(ru_doc="Вкл/выкл авто-ферму для бензина в @bfgbunker_bot")
    async def бензин(self, message: Message):
        """Toggle petrol auto-farm for @bfgbunker_bot"""
        if self.shadow_ultimat:
            await self.shadow_ultimat.бензин(message)
        else:
            await utils.answer(message, self.strings["load_error"].format("Shadow_Ultimat не загружен"))

    @loader.command(ru_doc="Вкл/выкл авто-ферму для теплицы в @bfgbunker_bot")
    async def теплица(self, message: Message):
        """Toggle greenhouse auto-farm for @bfgbunker_bot"""
        if self.shadow_ultimat:
            await self.shadow_ultimat.теплица(message)
        else:
            await utils.answer(message, self.strings["load_error"].format("Shadow_Ultimat не загружен"))

    @loader.command(ru_doc="Вкл/выкл авто-ферму для пустоши в @bfgbunker_bot")
    async def пустошь(self, message: Message):
        """Toggle wasteland auto-farm for @bfgbunker_bot"""
        if self.shadow_ultimat:
            await self.shadow_ultimat.пустошь(message)
        else:
            await utils.answer(message, self.strings["load_error"].format("Shadow_Ultimat не загружен"))

    @loader.command(ru_doc="Вкл/выкл авто-ферму для сада в @bfgbunker_bot")
    async def сад(self, message: Message):
        """Toggle garden auto-farm for @bfgbunker_bot"""
        if self.shadow_ultimat:
            await self.shadow_ultimat.сад(message)
        else:
            await utils.answer(message, self.strings["load_error"].format("Shadow_Ultimat не загружен"))

    @loader.command(ru_doc="Вкл/выкл авто-ферму для шахты в @bfgbunker_bot")
    async def шахта(self, message: Message):
        """Toggle mine auto-farm for @bfgbunker_bot"""
        if self.shadow_ultimat:
            await self.shadow_ultimat.шахта(message)
        else:
            await utils.answer(message, self.strings["load_error"].format("Shadow_Ultimat не загружен"))

    @loader.command(ru_doc="Вкл/выкл авто-ферму для гильдии в @bfgbunker_bot")
    async def гильдия(self, message: Message):
        """Toggle guild auto-farm for @bfgbunker_bot"""
        if self.shadow_ultimat:
            await self.shadow_ultimat.гильдия(message)
        else:
            await utils.answer(message, self.strings["load_error"].format("Shadow_Ultimat не загружен"))

    @loader.command(ru_doc="Установить новый префикс")
    async def pref(self, message: Message):
        """Set a new command prefix"""
        if self.shadow_ultimat:
            await self.shadow_ultimat.pref(message)
        else:
            await utils.answer(message, self.strings["load_error"].format("Shadow_Ultimat не загружен"))
