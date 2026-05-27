import sys
from pathlib import Path

import pyperclip
import rumps

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MENU_BAR_ICON_TEMPLATE = True
MAX_HISTORY_TITLE_LENGTH = 66


def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parents[1] / "Resources" / relative_path
    return PROJECT_ROOT / relative_path


MENU_BAR_ICON_PATH = resource_path("resources/menu-bar-mic-template.png")


class WhisprApp(rumps.App):
    def __init__(self, controller):
        self.status_item = rumps.MenuItem("Status: Starting")
        super().__init__("Whispr",
                         menu=[self.status_item,
                               None,
                               "Model",
                               "Clipboard History",
                               None,
                               "Quit",
                               ],
                         quit_button=None,
                         icon=str(MENU_BAR_ICON_PATH),
                         template=MENU_BAR_ICON_TEMPLATE
                         )
        self.controller = controller

        self.menu["Quit"].set_callback(self.quit_app)
        self.model_items = {}
        self.build_model_menu()
        self.refresh_menu(None)

        self.refresh_timer = rumps.Timer(self.refresh_menu, 1)
        self.refresh_timer.start()

    def build_model_menu(self):
        model_menu = self.menu["Model"]
        self.model_items = {}
        items = []
        for model_name in self.controller.available_models:
            item = rumps.MenuItem(model_name, callback=self.select_model)
            self.model_items[model_name] = item
            items.append(item)
        self.replace_menu_items(model_menu, items)

    def refresh_menu(self, _):
        self.refresh_status()
        self.refresh_model_menu()
        self.refresh_history_menu()

    def refresh_status(self):
        self.status_item.title = f"Status: {self.controller.get_status_text()}"

    def refresh_model_menu(self):
        for model_name, item in self.model_items.items():
            item.state = int(model_name == self.controller.model_name)

    def refresh_history_menu(self):
        history_menu = self.menu["Clipboard History"]

        history = self.controller.get_history()
        if not history:
            self.replace_menu_items(history_menu, [rumps.MenuItem("No transcriptions yet")])
            return

        items = []
        for text in history:
            item = rumps.MenuItem(self._history_title(text), callback=self.copy_history_item)
            item.transcription_text = text
            items.append(item)

        items.append(rumps.MenuItem("Clear History", callback=self.clear_history))
        self.replace_menu_items(history_menu, items)

    def replace_menu_items(self, menu, items):
        if getattr(menu, "_menu", None) is not None:
            menu.clear()
        menu.update(items)

    def _history_title(self, text):
        if len(text) <= MAX_HISTORY_TITLE_LENGTH:
            return text
        return f"{text[:MAX_HISTORY_TITLE_LENGTH - 3]}..."

    def select_model(self, sender):
        if self.controller.set_model(sender.title):
            self.refresh_model_menu()

    def copy_history_item(self, sender):
        pyperclip.copy(sender.transcription_text)

    def clear_history(self, _):
        self.controller.clear_history()
        self.refresh_history_menu()

    def quit_app(self, _):
        self.controller.close()
        rumps.quit_application()
