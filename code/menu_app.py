from pathlib import Path

import rumps

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ICON_PATH = PROJECT_ROOT / "resources" / "whispr-app-icon-enamel-mic.icns"


class WhisprApp(rumps.App):
    def __init__(self, controller):
        super().__init__("Whispr",
                         menu=["Status: Idle",
                               None,
                               "Model",
                               "Clipboard History",
                               None,
                               "Quit",
                               ],
                         quit_button=None,
                         icon=str(ICON_PATH)
                         )
        self.controller = controller

        self.menu["Quit"].set_callback(self.quit_app)

        self.menu["Model"].update([
            "distil-large-v3",
            "base",
            "small",
        ])

    def quit_app(self, _):
        self.controller.close()
        rumps.quit_application()
