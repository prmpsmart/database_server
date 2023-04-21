from src.server import *
from src.reloader import run_with_reloader
import signal


def quit(*args):
    exit()


signal.signal(signal.SIGINT, quit)


LOAD()

server = DatabaseServer()

r = 1
r = 0
if r:
    run_with_reloader(server.serve_forever, interval=3)
else:
    server.serve_forever()
