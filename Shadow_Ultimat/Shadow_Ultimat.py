import importlib.util
import sys
import requests
import os
from .. import loader, utils

@loader.tds
class ShadowUltimatMod(loader.Module):
    strings = {"name": "Shadow_Ultimat"}

    def __init__(self):
        self.version = "v777"  # Версия основного модуля
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "prefix",
                ".",
                "Префикс команд для быстрого копирования",
                validator=loader.validators.String()
            )
        )
        self.modules = {
            "Bonus": "Shadow_Ultimat_auto_Bonus",
            "Garden": "Shadow_Ultimat_auto_Garden",
            "Greenhouse": "Shadow_Ultimat_auto_Greenhouse",
            "Guild": "Shadow_Ultimat_auto_Guild",
            "Mine": "Shadow_Ultimat_auto_Mine",
            "People": "Shadow_Ultimat_auto_People",
            "Petrol": "Shadow_Ultimat_auto_Petrol",
            "Wasteland": "Shadow_Ultimat_auto_Wasteland",
            "StateGuild": "Shadow_Ultimat_state_Guild",
            "StatePeople": "Shadow_Ultimat_state_People",
            "StateProfile": "Shadow_Ultimat_state_Profile",
            "Update": "Shadow_Ultimat_update"
        }
        self.module_urls = {
            name: f"https://raw.githubusercontent.com/Nyashka17/Shadow_modules/refs/heads/main/Shadow_Ultimat/{module_name}.py"
            for name, module_name in self.modules.items()
        }
        self.module_urls["Main"] = "https://raw.githubusercontent.com/Nyashka17/Shadow_modules/refs/heads/main/Shadow_Ultimat/Shadow_Ultimat.py"
        self.module_states = {name: False for name in self.modules}
        self.module_versions = {name: "Unknown" for name in self.modules}
        self.loaded_modules = {}  # Хранилище загруженных модулей
        self.load_modules()

    def load_module_from_string(self, name, code):
        """Динамическая загрузка модуля из строки."""
        try:
            # Удаляем относительные импорты для избежания ошибок
            code = code.replace("from .. import loader, utils", "")
            spec = importlib.util.spec_from_loader(name, loader=None)
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            exec(code, module.__dict__)
            return module
        except Exception as e:
            print(f"Ошибка загрузки модуля {name}: {str(e)}")  # Исправленная строка
            return None

    def fetch_module(self, url):
        """Получение кода модуля по URL."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Ошибка загрузки модуля с {url}: {str(e)}")
            return None

    def load_modules(self):
        """Загрузка всех подмодулей и обновление их состояний и версий."""
        for name, module_name in self.modules.items():
            code = self.fetch_module(self.module_urls[name])
            if code:
                module = self.load_module_from_string(module_name, code)
                if module:
                    self.loaded_modules[name] = module
                    self.module_states[name] = getattr(module, "STATE", False)
                    self.module_versions[name] = getattr(module, "VERSION", "Unknown")
                else:
                    self.module_states[name] = False
                    self.module_versions[name] = "Unknown"
                    self.loaded_modules[name] = None

    async def shcmd(self, message: Message):
        """Отображение статуса автофарма Shadow_Ultimat."""
        status_emoji = lambda state: "✅" if state else "⛔️"
        prefix = self.config["prefix"]
        reply = (
            f"📓  | Shadow_Ultimat | ~ [ {self.version} ]\n"
            "╔═╣════════════════╗\n"
            "║  🔻СТАТУС |💣| BFGB🔻\n"
            "╠══════════════════╣\n"
            f"║~$ 👫 Люди: {status_emoji(self.module_states['People'])}\n"
            "╠══════════════════╣\n"
            f"║~$ 🎁 Бонус: {status_emoji(self.module_states['Bonus'])}\n"
            "╠══════════════════╣\n"
            f"║~$ 🛢 Бензин: {status_emoji(self.module_states['Petrol'])}\n"
            "╠══════════════════╣\n"
            f"║~$ 🌱 Теплица: {status_emoji(self.module_states['Greenhouse'])}\n"
            "╠══════════════════╣\n"
            f"║~$ 🏜 Пустошь: {status_emoji(self.module_states['Wasteland'])}\n"
            "╠══════════════════╣\n"
            f"║~$ 🌳 Сад: {status_emoji(self.module_states['Garden'])}\n"
            "╠══════════════════╣\n"
            f"║~$ ⛏ Шахта: {status_emoji(self.module_states['Mine'])}\n"
            "╠══════════════════╣\n"
            f"║~$ 🏛 Гильдия: {status_emoji(self.module_states['Guild'])}\n"
            "╠══════════════════╣\n"
            "║👁‍🗨 Команды: \n"
            f"╠═╣<code>{prefix}люди</code> - вкл/выкл\n"
            f"╠═╣<code>{prefix}бонус</code> - вкл/выкл\n"
            f"╠═╣<code>{prefix}бензин</code> - вкл/выкл\n"
            f"╠═╣<code>{prefix}теплица</code> - вкл/выкл\n"
            f"╠═╣<code>{prefix}пустошь</code> - вкл/выкл\n"
            f"╠═╣<code>{prefix}сад</code> - вкл/выкл\n"
            f"╠═╣<code>{prefix}шахта</code> - вкл/выкл\n"
            f"╠═╣<code>{prefix}гильдия</code> - вкл/выкл\n"
            f"╠═╣<code>{prefix}shupdate</code> - обновить модули\n"
            f"╠═╣<code>{prefix}check</code> - проверить обновления\n"
            f"╠═╣<code>{prefix}pref</code> - установить префикс\n"
            "╚═══════════════════"
        )
        await utils.answer(message, reply)

    async def shupdatecmd(self, message: Message):
        """Обновление всех модулей с GitHub."""
        await utils.answer(message, "🔄 Обновление модулей...")
        self.load_modules()  # Перезагрузка подмодулей
        main_code = self.fetch_module(self.module_urls["Main"])
        if main_code:
            try:
                # Проверка наличия __file__, fallback на имя файла
                file_path = getattr(sys.modules.get(__name__), '__file__', 'Shadow_Ultimat.py')
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(main_code)
                await utils.answer(message, "✅ Все модули и основной модуль обновлены! Перезагрузите бота для применения изменений.")
            except Exception as e:
                await utils.answer(message, f"❌ Ошибка при обновлении основного модуля: {str(e)}")
        else:
            await utils.answer(message, "❌ Не удалось загрузить основной модуль.")

    async def checkcmd(self, message: Message):
        """Проверка обновлений модулей по версиям."""
        await utils.answer(message, "🔍 Проверка обновлений...")
        updates = []
        for name, url in self.module_urls.items():
            code = self.fetch_module(url)
            if code:
                try:
                    # Уникальное имя для избежания конфликтов
                    module = self.load_module_from_string(f"check_{name}_{id(name)}", code)
                    if module:
                        remote_version = getattr(module, "VERSION", "Unknown")
                        local_version = self.module_versions.get(name, self.version if name == "Main" else "Unknown")
                        if remote_version != local_version:
                            updates.append(f"📦 {name}: {local_version} -> {remote_version}")
                    else:
                        updates.append(f"❌ {name}: Не удалось загрузить модуль")
                except Exception as e:
                    updates.append(f"❌ {name}: Ошибка при проверке ({str(e)})")
            else:
                updates.append(f"❌ {name}: Не удалось загрузить")
        reply = "📋 Результаты проверки обновлений:\n" + "\n".join(updates) if updates else "✅ Все модули актуальны!"
        await utils.answer(message, reply)

    async def prefcmd(self, message: Message):
        """Установка пользовательского префикса команд."""
        args = utils.get_args_raw(message).strip()
        if not args:
            await utils.answer(message, f"❌ Укажите префикс, например: {self.config['prefix']}pref !")
            return
        self.config["prefix"] = args
        await utils.answer(message, f"✅ Префикс установлен: {args}")

    async def peoplecmd(self, message: Message):
        """Переключение автофарма Люди."""
        await self.toggle_module(message, "People")

    async def bonuscmd(self, message: Message):
        """Переключение автофарма Бонус."""
        await self.toggle_module(message, "Bonus")

    async def petrolcmd(self, message: Message):
        """Переключение автофарма Бензин."""
        await self.toggle_module(message, "Petrol")

    async def greenhousecmd(self, message: Message):
        """Переключение автофарма Теплица."""
        await self.toggle_module(message, "Greenhouse")

    async def wastelandcmd(self, message: Message):
        """Переключение автофарма Пустошь."""
        await self.toggle_module(message, "Wasteland")

    async def gardencmd(self, message: Message):
        """Переключение автофарма Сад."""
        await self.toggle_module(message, "Garden")

    async def minecmd(self, message: Message):
        """Переключение автофарма Шахта."""
        await self.toggle_module(message, "Mine")

    async def guildcmd(self, message: Message):
        """Переключение автофарма Гильдия."""
        await self.toggle_module(message, "Guild")

    async def toggle_module(self, message: Message, module_name: str):
        """Переключение состояния указанного модуля."""
        module = self.loaded_modules.get(module_name)
        if module:
            try:
                module.STATE = not module.STATE
                self.module_states[module_name] = module.STATE
                status = "включен" if module.STATE else "выключен"
                await utils.answer(message, f"✅ {module_name}: Автофарм {status}")
            except Exception as e:
                await utils.answer(message, f"❌ Ошибка при переключении {module_name}: {str(e)}")
        else:
            await utils.answer(message, f"❌ Модуль {module_name} не загружен")

    async def client_ready(self, client, db):
        """Инициализация модуля при запуске клиента."""
        self.load_modules()
