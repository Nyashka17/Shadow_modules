# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔐 Licensed under the GNU AGPLv3.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: ShadowUpdate
# Author: @familiarrrrrr
# Commands:
# .check
# .shupdate
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
from herokutl.types import Message
from .. import loader, utils

@loader.tds
class ShadowUpdate(loader.Module):
    """Module for managing updates of Shadow_Ultimat and its sub-modules"""
    strings = {
        "name": "ShadowUpdate",
        "check_desc": "Проверить наличие обновлений",
        "shupdate_desc": "Обновить модули до последней версии",
        "up_to_date": "У вас текущая версия! Обновлений нет.",
        "new_version": "Новая версия доступна! Используйте .shupdate для обновления.",
        "update_loading": "Загружаю обновления с GitHub...",
        "update_success": "Модули успешно обновлены до версии {}. Новое: [укажите изменения], Убрано: [укажите удалённое].",
        "update_error": "Ошибка при обновлении: {}"
    }
    strings_ru = strings

    async def client_ready(self, client, db):
        """Initialize database and load Shadow_Ultimat"""
        self._db = db
        if "ShadowUpdate" not in self._db:
            self._db["ShadowUpdate"] = {}
        if "update_log" not in self._db["ShadowUpdate"]:
            self._db["ShadowUpdate"]["update_log"] = "Изначальная установка: 7.7.7"

        self.core_file = os.path.join(pathlib.Path.home(), ".heroku", "Shadow_Ultimat.py")
        os.makedirs(os.path.dirname(self.core_file), exist_ok=True)
        self._lock = asyncio.Lock()
        await self._load_core_module()

    async def _load_core_module(self):
        """Загрузка модуля Shadow_Ultimat с GitHub"""
        github_url = "https://raw.githubusercontent.com/Nyashka17/Shadow_modules/refs/heads/main/Shadow_Ultimat/Shadow_Ultimat.py"
        try:
            async with self._lock:
                response = requests.get(github_url, timeout=10)
                response.raise_for_status()
                with open(self.core_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                spec = importlib.util.spec_from_file_location("Shadow_Ultimat", self.core_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                # Предполагаем, что класс называется Shadow_Ultimat
                self.shadow_ultimat = module.Shadow_Ultimat(self.bot, self._db, self.config, self.strings)
        except Exception as e:
            self.shadow_ultimat = None
            self.logger.error(f"Failed to load Shadow_Ultimat: {e}")

    def reload_module(self, module_name, file_path):
        """Перезагрузка модуля из файла"""
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module

    @loader.command(ru_doc="Проверить наличие обновлений")
    async def check(self, message: Message):
        """Check for available updates"""
        current_version = self.config["current_version"]
        module_dir = os.path.join(pathlib.Path.home(), ".heroku")
        main_url = "https://raw.githubusercontent.com/Nyashka17/Shadow_modules/refs/heads/main/Shadow_Ultimat/Shadow_Ultimat.py"
        response = requests.get(main_url)
        content = response.text
        # Parse version (simplified, adjust with regex if needed)
        latest_version = "7.7.7"  # Replace with actual version extraction logic
        if current_version == latest_version:
            await utils.answer(message, self.strings["up_to_date"])
        else:
            await utils.answer(message, self.strings["new_version"])

    @loader.command(ru_doc="Обновить модули до последней версии")
    async def shupdate(self, message: Message):
        """Update all modules to the latest version"""
        await utils.answer(message, self.strings["update_loading"])
        module_dir = os.path.join(pathlib.Path.home(), ".heroku")
        os.makedirs(module_dir, exist_ok=True)
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
                filename = os.path.join(module_dir, url.split("/")[-1])
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(response.text)

            # Перезагрузка модулей
            main_file = os.path.join(module_dir, "Shadow_Ultimat.py")
            self.reload_module("Shadow_Ultimat", main_file)
            update_file = os.path.join(module_dir, "Shadow_Ultimat_update.py")
            self.reload_module("ShadowUpdate", update_file)

            # Перезагрузка подмодулей
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
                sub_file = os.path.join(module_dir, f"{sub}.py")
                if os.path.exists(sub_file):
                    self.reload_module(sub, sub_file)

            # Update version
            with open(main_file, "r", encoding="utf-8") as f:
                content = f.read()
                latest_version = "7.7.7"  # Extract actual version
            self.config["current_version"] = latest_version
            self._db["ShadowUpdate"]["update_log"] = f"Обновлено до {latest_version} в {utils.get_current_time()}"

            await utils.answer(message, self.strings["update_success"].format(latest_version))

        except requests.RequestException as e:
            await utils.answer(message, self.strings["update_error"].format(str(e)))
        except Exception as e:
            await utils.answer(message, self.strings["update_error"].format(str(e)))
