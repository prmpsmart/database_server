from src.server.server import *
from src.reloader import run_with_reloader


LOAD()

server = DatabaseServer()

r = 1
r = 0
if r:
    run_with_reloader(server.serve_forever, interval=3)
else:
    server.serve_forever()
