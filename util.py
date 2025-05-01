import threading
import signal
import time

def wait_for_signal(sig: int):
    shutdown_event = threading.Event()

    def handle_signal(signum, frame):
        shutdown_event.set()

    signal.signal(sig, handle_signal)   # Interrupt signal (Ctrl+C)

    while not shutdown_event.is_set():
        time.sleep(1)
