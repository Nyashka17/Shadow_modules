from herokutl.types import Message
from .. import loader, utils  # Оставляем как есть, но проверим позже
import requests
import importlib.util
import os
import sys

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
        "update_error": "Ошибка при обновлении: {}",
        "log_desc": "Показать лог последних обновлений",
        "log_msg": "Лог обновлений: [укажите лог здесь]"
    }
    strings_ru = strings

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("current_version", "7.7.7", "Current module version", validator=loader.validators.String()),
        )
        self.module_urls = [
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

    async def client_ready(self, client, db):
        """Initialize database when client is ready"""
        self._db = db
        if "ShadowUpdate" not in self._db:
            self._db["ShadowUpdate"] = {}
        if "update_log" not in self._db["ShadowUpdate"]:
            self._db["ShadowUpdate"]["update_log"] = "Изначальная установка: 7.7.7"

    def reload_module(self, module_name, file_path):
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module

    @loader.command(ru_doc="Проверить наличие обновлений")
    async def check(self, message: Message):
        """Check for available updates"""
        current_version = self.config["current_version"]
        module_dir = "."  # Используем текущую директорию
        main_url = self.module_urls[0]  # URL for Shadow_Ultimat.py
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
        module_dir = "."  # Используем текущую директорию
        try:
            for url in self.module_urls:
                filename = os.path.join(module_dir, url.split("/")[-1])
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                with open(filename, "wb") as f:
                    f.write(response.content)

            # Reload main module
            main_file = os.path.join(module_dir, "Shadow_Ultimat.py")
            self.reload_module("Shadow_Ultimat", main_file)

            # Reload sub-modules
            sub_modules = [f"Shadow_Ultimat_{part}" for part in [
                "auto_Bonus", "auto_Garden", "auto_Greenhouse", "auto_Guild",
                "auto_Mine", "auto_People", "auto_Petrol", "auto_Wasteland",
                "state_Guild", "state_People", "state_Profile", "update"
            ]]
            for sub in sub_modules:
                sub_file = os.path.join(module_dir, f"{sub}.py")
                if os.path.exists(sub_file):
                    self.reload_module(sub, sub_file)

            # Update version (parse from main module if needed)
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

    @loader.command(ru_doc="Показать лог последних обновлений")
    async def log(self, message: Message):
        """Show update log"""
        log = self._db.get("ShadowUpdate", {}).get("update_log", "Нет логов")
        await utils.answer(message, self.strings["log_msg"].format(log))
