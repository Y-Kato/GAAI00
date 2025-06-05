"""Filesystem watcher that triggers incremental indexing as soon as files change."""
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from config import PROJECT_DIR, WATCH_INTERVAL_SEC
from indexer import incremental_update

class Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        incremental_update()

observer = Observer()
observer.schedule(Handler(), str(PROJECT_DIR), recursive=True)
observer.start()

try:
    while True:
        sleep(WATCH_INTERVAL_SEC)
except KeyboardInterrupt:
    observer.stop()
observer.join()