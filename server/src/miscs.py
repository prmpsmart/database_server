import os, hashlib, dotenv, socket
from .server_request_schema import SERVER_REQUEST_SCHEMA
from .commons import *


CONFIG_ERROR = True
CWD = os.path.dirname(__file__)
PICKLE_DB = os.path.join(CWD, "PICKLE_DB")
SQL_DB = os.path.join(CWD, "SQL_DB")

ENV = DictObj()

CONFIG = "server_config.env"
CONFIG = os.path.join(CWD, CONFIG)


try:
    ENV.update(dotenv.Dotenv(CONFIG))
    DatabaseFolder = ENV.DatabaseFolder
    if DatabaseFolder:
        try:
            assert os.path.isabs(
                DatabaseFolder
            ), f'DatabaseFolder in the "{CONFIG}" must be an ablsolute path.\ne.g DatabaseFolder=path to folder'
            CONFIG_ERROR = False

            if os.path.isdir(os.path.dirname(DatabaseFolder)):
                if not os.path.isdir(DatabaseFolder):
                    os.mkdir(DatabaseFolder)
            else:
                print("Invalid directory used as DatabaseFolder")

        except AssertionError as err:
            print(err)
    else:
        print(f'DatabaseFolder not set in the "{CONFIG}" file')

except FileNotFoundError as err:
    print(f"{err} file not present in the installation directory.")

if CONFIG_ERROR:
    exit()

Host = socket.gethostbyname(socket.gethostname())
Port = ENV.Port

try:
    Port = int(Port)
except:
    Port = 0

if not Port:
    Port = 80
    print('Port not provided in the server_config.env file, port 80 is used.')


sha224 = lambda password: hashlib.sha224(password.encode()).hexdigest()

SERVER_REQUEST_SCHEMA = DictObj.from_json(SERVER_REQUEST_SCHEMA)
