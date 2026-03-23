# src/server_control.py
import subprocess
import time


class ServerController:
    def __init__(self, caddyfile: str):
        self.caddyfile = caddyfile
        self.proc = None

    def start(self) -> None:
        if self.proc is not None:
            return
        self.proc = subprocess.Popen(
            ["caddy", "run", "--config", self.caddyfile],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        time.sleep(2)

    def stop(self) -> None:
        if self.proc is None:
            return
        self.proc.terminate()
        self.proc.wait(timeout=5)
        self.proc = None