from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from config import cfg
from indexer import incremental_update

class Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        try:
            incremental_update()
        except Exception as e:
            print(f"[WATCHER][ERROR] Failed to update index incrementally: {e}")

observer = Observer()
observer.schedule(Handler(), str(cfg.PROJECT_DIR), recursive=True)
observer.start()

try:
    while True:
        sleep(cfg.WATCH_INTERVAL_SEC)
except KeyboardInterrupt:
    observer.stop()
observer.join()
