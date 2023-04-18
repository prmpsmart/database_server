from http import HTTPStatus
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import socket

from ..commons import DictObj
from .models import *

Host = socket.gethostbyname(socket.gethostname())
Port = int(ENV.Port or 5000)


class DatabaseServer(ThreadingHTTPServer):
    allow_reuse_address = 1

    def __init__(self) -> None:
        super().__init__(
            (Host, Port),
            DatabaseHTTPRequestHandler,
        )

    def serve_forever(self):
        print("Serving on http://%s:%d" % self.server_address)
        super().serve_forever()


class DatabaseHTTPRequestHandler(BaseHTTPRequestHandler):
    @property
    def dictObj(self) -> DictObj:
        content_length = self.headers["content-length"]
        content_length = int(content_length)
        dictObj, data = DictObj(), ""
        message = "Request body should be a valid JSON."
        explain = "The request body should be a valid JSON text."

        if content_length:
            data = self.rfile.read(content_length).decode()
            print(data)
            try:
                dictObj = DictObj.from_json(data)
            except:
                self.send_error(500, message, explain)
        else:
            self.send_error(500, message, explain)

        return dictObj

    def sendDictObj(self, dictObj: DictObj, status: int = HTTPStatus.OK):
        json = dictObj.to_json().encode()
        self.send_response_only(status)
        self.send_header("content-length", len(json))
        self.end_headers()
        self.wfile.write(json)
        self.wfile.flush()

    def getMessage(self, status: int):
        if status := SERVER_REQUEST_SCHEMA.status[f"S{status}"]:
            return status.message

    def do_POST(self):
        if dictObj := self.dictObj:
            # print(f"Request: {dictObj.to_json()}")

            if dictObj.action in SERVER_REQUEST_SCHEMA.actions:
                action_method = getattr(self, dictObj.action, None)
                status = action_method(dictObj)

            else:
                status = INVALID_REQUEST

            if isinstance(status, int):
                status = DictObj(
                    status=status,
                    message=self.getMessage(status),
                )

            elif isinstance(status, DictObj):
                status.message = self.getMessage(status.status)

            self.sendDictObj(status)

    #
    #
    #

    def FolderExists(self, dictObj: DictObj):
        return Folder.folderExists(dictObj.name)

    def CreateFolder(self, dictObj: DictObj):
        return Folder.createFolder(dictObj.name, dictObj.password)

    def GetFolder(self, dictObj: DictObj):
        return Folder.getFolder(dictObj.name, dictObj.password)

    def RenameFolder(self, dictObj: DictObj):
        return Folder.renameFolder(dictObj.name, dictObj.password, dictObj.newName)

    def DeleteFolder(self, dictObj: DictObj):
        return Folder.deleteFolder(dictObj.name, dictObj.password)

    #
    #
    #

    def DatabaseExists(self, dictObj: DictObj):
        return Database.databaseExists(
            dictObj.name, dictObj.folder, dictObj.folderPassword
        )

    def CreateDatabase(self, dictObj: DictObj):
        return Database.createDatabase(
            dictObj.name, dictObj.password, dictObj.folder, dictObj.folderPassword
        )

    def GetDatabase(self, dictObj: DictObj):
        return Database.getDatabase(
            dictObj.name, dictObj.password, dictObj.folder, dictObj.folderPassword
        )

    def RenameDatabase(self, dictObj: DictObj):
        return Database.renameDatabase(
            dictObj.name,
            dictObj.password,
            dictObj.newName,
            dictObj.folder,
            dictObj.folderPassword,
        )

    def DropDatabase(self, dictObj: DictObj):
        return Database.dropDatabase(
            dictObj.name, dictObj.password, dictObj.folder, dictObj.folderPassword
        )

    #
    #
    #

    def CreateTable(self, dictObj: DictObj):
        return Table.createTable(
            dictObj.database,
            dictObj.password,
            dictObj.name,
            dictObj.columns,
            dictObj.folder,
            dictObj.folderPassword,
        )

    def DropTable(self, dictObj: DictObj):
        return Table.dropTable(
            dictObj.database,
            dictObj.password,
            dictObj.name,
            dictObj.folder,
            dictObj.folderPassword,
        )

    #
    #
    #

    def AddColumn(self, dictObj: DictObj):
        return Table.addColumn(
            dictObj.database,
            dictObj.password,
            dictObj.table,
            dictObj.column,
            dictObj.datatype,
            dictObj.folder,
            dictObj.folderPassword,
        )

    #
    #
    #

    def Select(self, dictObj: DictObj):
        return CRUD.select(
            dictObj.database,
            dictObj.password,
            dictObj.table,
            dictObj.columns,
            dictObj.where,
            dictObj.folder,
            dictObj.folderPassword,
        )

    def Insert(self, dictObj: DictObj):
        return CRUD.insert(
            dictObj.database,
            dictObj.password,
            dictObj.table,
            dictObj["values"],
            dictObj.columns,
            dictObj.multiValues,
            dictObj.folder,
            dictObj.folderPassword,
        )

    def Update(self, dictObj: DictObj):
        return CRUD.update(
            dictObj.database,
            dictObj.password,
            dictObj.table,
            dictObj["values"],
            dictObj.columns,
            dictObj.where,
            dictObj.folder,
            dictObj.folderPassword,
        )

    def Delete(self, dictObj: DictObj):
        return CRUD.delete(
            dictObj.database,
            dictObj.password,
            dictObj.table,
            dictObj.where,
            dictObj.folder,
            dictObj.folderPassword,
        )

    #
    #
    #

    def SQL(self, dictObj: DictObj):
        return CRUD.sql(
            dictObj.database,
            dictObj.password,
            dictObj.table,
            dictObj.statement,
            dictObj.folder,
            dictObj.folderPassword,
        )
