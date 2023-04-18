from typing import Any, Union
import time, json
from http.client import HTTPConnection
from .miscs import *


class Request:
    def __init__(self, timeout=0):
        self.timeout = timeout

    def post(self, **kwargs):
        dump = json.dumps(kwargs)
        return print(dump)

        connection = HTTPConnection("localhost", 5000, timeout=self.timeout)
        connection.request("POST", "/", dump)
        response = connection.getresponse()
        body = response.read(response.headers.get(b"content-length"))

        return json.loads(body, object_hook=DictObj)

    def folderExists(self, name: str):
        return self.post(
            action="FolderExists",
            name=name,
        )

    def createFolder(self, name: str, password: str):
        return self.post(
            action="CreateFolder",
            name=name,
            password=password,
        )

    def getFolder(self, name: str, password: str):
        return self.post(
            action="GetFolder",
            name=name,
            password=password,
        )

    def renameFolder(self, name: str, password: str, newName: str):
        return self.post(
            action="RenameFolder", name=name, password=password, newName=newName
        )

    def deleteFolder(self, name: str, password: str):
        return self.post(
            action="DeleteFolder",
            name=name,
            password=password,
        )

    #
    #
    #

    def databaseExists(
        self, name: str, folder: str = "", folderPassword: str = "", **kwargs
    ):
        return self.post(
            action="DatabaseExists",
            name=name,
            folder=folder,
            folderPassword=folderPassword,
            **kwargs,
        )

    def createDatabase(
        self,
        name: str,
        password: str,
        folder: str = "",
        folderPassword: str = "",
        **kwargs,
    ):
        return self.post(
            action="CreateDatabase",
            name=name,
            password=password,
            folder=folder,
            folderPassword=folderPassword,
            **kwargs,
        )

    def getDatabase(
        self,
        name: str,
        password: str,
        folder: str = "",
        folderPassword: str = "",
        **kwargs,
    ):
        return self.post(
            action="GetDatabase",
            name=name,
            password=password,
            folder=folder,
            folderPassword=folderPassword,
            **kwargs,
        )

    def renameDatabase(
        self,
        name: str,
        password: str,
        newName: str,
        folder: str = "",
        folderPassword: str = "",
        **kwargs,
    ):
        return self.post(
            action="RenameDatabase",
            name=name,
            password=password,
            newName=newName,
            folder=folder,
            folderPassword=folderPassword,
            **kwargs,
        )

    def dropDatabase(
        self,
        name: str,
        password: str,
        folder: str = "",
        folderPassword: str = "",
        **kwargs,
    ):
        return self.post(
            action="DropDatabase",
            name=name,
            password=password,
            folder=folder,
            folderPassword=folderPassword,
            **kwargs,
        )

    #
    #
    #

    def createTable(
        self,
        database: str,
        password: str,
        name: str,
        columns: list[list[str, str]],
        folder: str = "",
        folderPassword: str = "",
        **kwargs,
    ):
        return self.post(
            action="CreateTable",
            database=database,
            password=password,
            name=name,
            columns=columns,
            folder=folder,
            folderPassword=folderPassword,
            **kwargs,
        )

    def dropTable(
        self,
        database: str,
        password: str,
        name: str,
        folder: str = "",
        folderPassword: str = "",
        **kwargs,
    ):
        return self.post(
            action="DropTable",
            database=database,
            password=password,
            name=name,
            folder=folder,
            folderPassword=folderPassword,
            **kwargs,
        )

    #
    #
    #

    def addColumn(
        self,
        database: str,
        password: str,
        table: str,
        column: str,
        datatype: str,
        folder: str = "",
        folderPassword: str = "",
        **kwargs,
    ):
        return self.post(
            action="AddColumn",
            database=database,
            password=password,
            table=table,
            column=column,
            datatype=datatype,
            folder=folder,
            folderPassword=folderPassword,
            **kwargs,
        )

    #
    #
    #

    def select(
        self,
        database: str,
        password: str,
        table: str,
        columns: Union[str, list[str]],
        where: list = [],
        folder: str = "",
        folderPassword: str = "",
        **kwargs,
    ):
        return self.post(
            action="Select",
            database=database,
            password=password,
            table=table,
            columns=columns,
            where=where,
            folder=folder,
            folderPassword=folderPassword,
            **kwargs,
        )

    def insert(
        self,
        database: str,
        password: str,
        table: str,
        values: list[Any],
        columns: list[str] = [],
        multiValues: list[list[Any]] = [],
        folder: str = "",
        folderPassword: str = "",
        **kwargs,
    ):
        return self.post(
            action="Insert",
            database=database,
            password=password,
            table=table,
            values=values,
            columns=columns,
            multiValues=multiValues,
            folder=folder,
            folderPassword=folderPassword,
            **kwargs,
        )

    def update(
        self,
        database: str,
        password: str,
        table: str,
        columns: list[str],
        values: list[Any],
        where: str = "",
        folder: str = "",
        folderPassword: str = "",
        **kwargs,
    ):
        return self.post(
            action="Update",
            database=database,
            password=password,
            table=table,
            columns=columns,
            values=values,
            where=where,
            folder=folder,
            folderPassword=folderPassword,
            **kwargs,
        )

    def delete(
        self,
        database: str,
        password: str,
        table: str,
        where: str = "",
        folder: str = "",
        folderPassword: str = "",
        **kwargs,
    ):
        return self.post(
            action="Delete",
            database=database,
            password=password,
            table=table,
            where=where,
            folder=folder,
            folderPassword=folderPassword,
            **kwargs,
        )

    #
    #
    #

    def sql(
        self,
        database: str,
        password: str,
        table: str,
        statement: str,
        folder: str = "",
        folderPassword: str = "",
        **kwargs,
    ):

        return self.post(
            action="SQL",
            database=database,
            password=password,
            table=table,
            statement=statement,
            folder=folder,
            folderPassword=folderPassword,
            **kwargs,
        )
