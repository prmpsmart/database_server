import os, dotenv
from .commons import *


CONFIG_ERROR = False
CWD = os.path.dirname(__file__)
PICKLE_DB = os.path.join(CWD, "PICKLE_DB")
SQL_DB = os.path.join(CWD, "SQL_DB")

ENV = DictObj()

CONFIG = "client_config.env"
CONFIG_ENV = os.path.join(CWD, CONFIG)
CONFIG_ENV = CONFIG


try:
    ENV.update(dotenv.Dotenv(CONFIG_ENV))
    assert ENV.Server, f"Server link must be set in the {CONFIG}"
except FileNotFoundError as err:
    print(f"{err} '{CONFIG}' file not present in the running directory.")
    CONFIG_ERROR = True
except AssertionError as err:
    CONFIG_ERROR = True
    print(err)


if CONFIG_ERROR:
    exit()
