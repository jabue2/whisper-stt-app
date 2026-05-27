import subprocess


def notify(text):
    subprocess.run(["osascript", "-e",
                    f'display notification "{text}" with title "Whisper"'])
