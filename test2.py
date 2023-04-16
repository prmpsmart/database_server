from src.server.models import *

LOAD()
print(Folder.folders)

get = lambda code: SERVER_REQUEST_SCHEMA.status[f"S{code}"]

folder_name = "test"
password = "test_pass"
status = Folder.createFolder(folder_name, password)
folder = Folder.folders.get(folder_name)

# status = Folder.deleteFolder(folder_name, password)
status = Database.createDatabase(folder_name, password)

database = Database.databases[folder_name]

status = Table.createTable(
    folder.name,
    password,
    "test_table",
    [
        ["column1", "VARCHAR"],
        ["column2", "UNIQUE INT"],
        ["column3", "datatype"],
    ],
)

if isinstance(status, DictObj):
    status = status.status

print(get(status), folder)
