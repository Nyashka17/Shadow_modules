import importlib.util
import sys
import requests
import os
from herokutl.types import Message
from .. import loader, utils

@loader.tds
class ShadowUltimatMod(loader.Module):
    strings = {"name": "Shadow_Ultimat"}

    def __init__(self):
        self.version = "v777"  # Version of the main module
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "prefix",
                ".",
                "Command prefix for quick copying",
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
        self.loaded_modules = {}  # Store loaded module objects
        self.load_modules()

    def load_module_from_string(self, name, code):
        """Dynamically load a module from a string."""
        spec = importlib.util.spec_from_loader(name, loader=None)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        exec(code, module.__dict__)
        return module

    def fetch_module(self, url):
        """Fetch module code from a URL."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Failed to fetch module from {url}: {e}")
            return None

    def load_modules(self):
        """Load all submodules and update their states and versions."""
        for name, module_name in self.modules.items():
            code = self.fetch_module(self.module_urls[name])
            if code:
                try:
                    module = self.load_module_from_string(module_name, code)
                    self.loaded_modules[name] = module
                    self.module_states[name] = getattr(module, "STATE", False)
                    self.module_versions[name] = getattr(module, "VERSION", "Unknown")
                except Exception as e:
                    print(f"Failed to load module {module_name}: {e}")
                    self.module_states[name] = False
                    self.module_versions[name] = "Unknown"
                    self.loaded_modules[name] = None

    async def shcmd(self, message: Message):
        """Display the status of Shadow_Ultimat auto-farm."""
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
        """Update all modules from GitHub."""
        await utils.answer(message, "🔄 Обновление модулей...")
        self.load_modules()  # Reload all submodules
        main_code = self.fetch_module(self.module_urls["Main"])
        if main_code:
            try:
                with open(__file__, "w") as f:
                    f.write(main_code)
                await utils.answer(message, "✅ Все модули и основной модуль обновлены! Перезагрузите бота для применения изменений.")
            except Exception as e:
                await utils.answer(message, f"❌ Ошибка при обновлении основного модуля: {e}")
        else:
            await utils.answer(message, "❌ Не удалось загрузить основной модуль.")

    async def checkcmd(self, message: Message):
        """Check for module updates by comparing versions."""
        await utils.answer(message, "🔍 Проверка обновлений...")
        updates = []
        for name, url in self.module_urls.items():
            if name == "Main":
                continue
            code = self.fetch_module(url)
            if code:
                try:
                    module = self.load_module_from_string(f"check_{name}", code)
                    remote_version = getattr(module, "VERSION", "Unknown")
                    local_version = self.module_versions.get(name, "Unknown")
                    if remote_version != local_version:
                        updates.append(f"📦 {name}: {local_version} -> {remote_version}")
                except Exception as e:
                    updates.append(f"❌ {name}: Ошибка при проверке ({e})")
            else:
                updates.append(f"❌ {name}: Не удалось загрузить")
        main_code = self.fetch_module(self.module_urls["Main"])
        if main_code:
            try:
                module = self.load_module_from_string("check_main", main_code)
                remote_version = getattr(module, "VERSION", "Unknown")
                if remote_version != self.version:
                    updates.append(f"📦 Main: {self.version} -> {remote_version}")
            except Exception as e:
                updates.append(f"❌ Main: Ошибка при проверке ({e})")
        else:
            updates.append("❌ Main: Не удалось загрузить")
        reply = "📋 Результаты проверки обновлений:\n" + "\n".join(updates) if updates else "✅ Все модули актуальны!"
        await utils.answer(message, reply)

    async def prefcmd(self, message: Message):
        """Set a custom command prefix."""
        args = utils.get_args_raw(message).strip()
        if not args:
            await utils.answer(message, f"❌ Укажите префикс, например: {self.config['prefix']}pref !")
            return
        self.config["prefix"] = args
        await utils.answer(message, f"✅ Префикс установлен: {args}")

    async def peoplecmd(self, message: Message):
        """Toggle People auto-farm."""
        await self.toggle_module(message, "People")

    async def bonuscmd(self, message: Message):
        """Toggle Bonus auto-farm."""
        await self.toggle_module(message, "Bonus")

    async def petrolcmd(self, message: Message):
        """Toggle Petrol auto-farm."""
        await self.toggle_module(message, "Petrol")

    async def greenhousecmd(self, message: Message):
        """Toggle Greenhouse auto-farm."""
        await self.toggle_module(message, "Greenhouse")

    async def wastelandcmd(self, message: Message):
        """Toggle Wasteland auto-farm."""
        await self.toggle_module(message, "Wasteland")

    async def gardencmd(self, message: Message):
        """Toggle Garden auto-farm."""
        await self.toggle_module(message, "Garden")

    async def minecmd(self, message: Message):
        """Toggle Mine auto-farm."""
        await self.toggle_module(message, "Mine")

    async def guildcmd(self, message: Message):
        """Toggle Guild auto-farm."""
        await self.toggle_module(message, "Guild")

    async def toggle_module(self, message: Message, module_name: str):
        """Toggle the state of a specific module."""
        module = self.loaded_modules.get(module_name)
        if module:
            try:
                module.STATE = not module.STATE
                self.module_states[module_name] = module.STATE
                status = "включен" if module.STATE else "выключен"
                await utils.answer(message, f"✅ {module_name}: Автофарм {status}")
            except Exception as e:
                await utils.answer(message, f"❌ Ошибка при переключении {module_name}: {e}")
        else:
            await utils.answer(message, f"❌ Модуль {module_name} не загружен")

    async def client_ready(self, client, db):
        """Initialize module on client ready."""
        self.load_modules()
