import threading
from menu_app import WhisprApp
from app_controller import AppController
from key_listener import start_key_listener
from notifier import notify


def run():
    controller = AppController()
    try:
        controller.start()
    except RuntimeError as error:
        message = str(error)
        print(message)
        notify("Whispr launch error", message)
        controller.close()
        return 0

    threading.Thread(target=start_key_listener, args=(controller.state_machine,), daemon=True).start()

    WhisprApp(controller).run()

    return 0


if __name__ == '__main__':
    raise SystemExit(run())
