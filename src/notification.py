from pathlib import Path
from winotify import Notification, audio

class Notifier:
    def __init__(self):
        self.desktop_notification = True
        # Create an absolute Windows path with backslashes
        self.icon_path = Path(__file__).parent  / 'logo.ico'
        # self.icon_path = self.icon_path.resolve().as_posix().replace('/', '\\')  # Convert to Windows backslashes

    def notify(self, longshort, openclose):
        if self.desktop_notification:
            toast = Notification(
                app_id="AutoTrader App",
                title="AutoTrader",
                msg=f'A {longshort} position has been {openclose}!',
                icon=self.icon_path  # Absolute path to icon
            )
            toast.set_audio(audio.LoopingAlarm3, loop=False)
            toast.show()

def main():
    notifier = Notifier()
    notifier.notify('long', 'opened')

if __name__ == "__main__":
    main()
