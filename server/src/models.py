import pickle
from typing import Any
from .database import *
from .miscs import *


class Base:
    def __init__(self, name: str, password: str):
        self.name = name
        self.password = password

    def __bool__(self):
        return True

    def __str__(self):
        return f"{self.__class__.__name__}({self.name})"

    def __repr__(self) -> str:
        return f"<{self}>"

    @property
    def path(self):
        return self.name

    def comparePassword(self, password: str):
        return sha224(password) == self.password

    def rename(self, name: str):
        self.create()
        dirname = os.path.dirname(self.path)
        newName = os.path.join(dirname, name)
        os.rename(self.path, newName)
        self.name = name

    def delete(self):
        if self.exists():
            os.remove(self.path)

    def create(self):
        ...

    def exists(self) -> bool:
        return os.path.exists(self.path)

    def to_json(self) -> str:
        ...


class Folder(Base):
    folders: DictObj[str, "Folder"] = DictObj()

    @classmethod
    def _folderExists(cls, name: str) -> bool:
        return name.lower() in cls.folders

    @classmethod
    def checkFolder(cls, name: str, password: str) -> tuple[int, "Folder"]:
        folder: Folder = None
        if cls._folderExists(name):
            folder = cls.folders[name]
            if folder.comparePassword(password):
                status = FOLDER_EXISTS
            else:
                status = FOLDER_PASSWORD_IS_INCORRECT
                folder = None
        else:
            status = FOLDER_DOES_NOT_EXISTS

        return status, folder

    @classmethod
    def folderExists(cls, name: str) -> int:
        return [FOLDER_DOES_NOT_EXISTS, FOLDER_EXISTS][cls._folderExists(name)]

    @classmethod
    def createFolder(cls, name: str, password: str):
        status = cls.folderExists(name)
        if status == FOLDER_DOES_NOT_EXISTS:
            password = sha224(password)
            folder = Folder(name, password)

            status = FOLDER_CREATED_SUCCESSFULLY
            sql_status, sql_error = InternalDB.save(folder)

            if sql_status == SUCCESS:
                cls.folders[name] = folder
                folder.create()
                THREAD_SAVE()

            else:
                status = FAILED

            status = DictObj(
                status=status,
                sql_status=sql_status,
                sql_error=sql_error,
            )

        return status

    @classmethod
    def getFolder(cls, name: str, password: str):
        status, folder = cls.checkFolder(name, password)
        if status == FOLDER_EXISTS:
            status = DictObj(
                status=status,
                name=name,
                totalDatabases=len(folder.databases),
                databases=list(folder.databases.keys()),
            )
        return status

    @classmethod
    def renameFolder(cls, name: str, password: str, newName: str):
        status, folder = cls.checkFolder(name, password)
        if status == FOLDER_EXISTS:
            if not cls._folderExists(newName):
                folder.rename(newName)
                status = FOLDER_RENAMED_SUCCESSFULLY
                sql_status, sql_error = InternalDB.save(folder)

                if sql_status == SUCCESS:
                    cls.folders[newName] = folder
                    del cls.folders[name]
                    THREAD_SAVE()

                else:
                    folder.rename(name)
                    status = FAILED

                status = DictObj(
                    status=status,
                    name=newName,
                    oldName=name,
                    sql_status=sql_status,
                    sql_error=sql_error,
                )
            else:
                status = NEW_FOLDER_NAME_EXISTS
        return status

    @classmethod
    def deleteFolder(cls, name: str, password: str):
        status, folder = cls.checkFolder(name, password)
        if status == FOLDER_EXISTS:
            status = FOLDER_DELETED_SUCCESSFULLY
            sql_status, sql_error, _ = InternalDB.delete(folder)

            if sql_status == SUCCESS:
                del cls.folders[name]
                folder.delete()
                THREAD_SAVE()

            else:
                cls.folders[name] = folder
                status = FAILED

            status = DictObj(
                status=status,
                name=name,
                sql_status=sql_status,
                sql_error=sql_error,
            )
        return status

    def __init__(self, name: str, password: str):
        super().__init__(name, password)
        self.databases: DictObj[str, Database] = DictObj()

    @property
    def path(self):
        return os.path.join(DatabaseFolder, self.name)

    def create(self):
        if not self.exists():
            os.mkdir(self.path)

    def delete(self):
        if self.exists():
            os.rmdir(self.path)

    def to_json(self) -> str:
        databases = DictObj()
        dictObj = DictObj(name=self.name, password=self.password, databases=databases)

        database: Database
        for name, database in self.databases.items():
            databases[name] = database.to_json()
        return dictObj.to_json()


class Database(Base):
    databases: DictObj[str, "Database"] = DictObj()

    @classmethod
    def _databaseExists(
        cls, name: str, folder: str = "", folderPassword: str = ""
    ) -> Union[bool, int, "Database", Folder]:
        databases = cls.databases
        status, boolean = DATABASE_DOES_NOT_EXISTS, False
        folder_: Folder = None

        if folder:
            status, folder_ = Folder.checkFolder(folder, folderPassword)
            if status == FOLDER_EXISTS:
                databases = folder_.databases

        if boolean := name in databases:
            status = DATABASE_EXISTS

        return boolean, status, databases.get(name), folder_

    @classmethod
    def databaseExists(cls, name: str, folder: str = "", folderPassword: str = ""):
        status = cls._databaseExists(name, folder, folderPassword)[1]
        if status == FOLDER_EXISTS:
            status = DATABASE_DOES_NOT_EXISTS
        return status

    @classmethod
    def checkDatabase(
        cls, name: str, password: str, folder: str = "", folderPassword: str = ""
    ) -> tuple[int, "Database", Folder]:
        database: Database = None
        folder_: Folder = None
        databases = {}
        status = DATABASE_DOES_NOT_EXISTS

        boolean, status, database, folder_ = cls._databaseExists(
            name, folder, folderPassword
        )

        if boolean and database:
            if database.comparePassword(password):
                status = DATABASE_EXISTS

            else:
                status = DATABASE_PASSWORD_IS_INCORRECT
                database = None

        return status, database, folder_

    @classmethod
    def createDatabase(
        cls, name: str, password: str, folder: str = "", folderPassword: str = ""
    ):
        status, database, folder_ = cls.checkDatabase(
            name,
            password,
            folder,
            folderPassword,
        )
        if status == DATABASE_DOES_NOT_EXISTS:
            databases = folder_.databases if folder_ else cls.databases
            password = sha224(password)
            status = DATABASE_CREATED_SUCCESSFULLY
            database = Database(name, password, folder_)

            sql_status, sql_error = InternalDB.save(database)

            if sql_status == SUCCESS:
                databases[name] = database
                database.create()
                THREAD_SAVE()

            else:
                status = FAILED

            status = DictObj(
                status=status,
                name=name,
                folder=folder,
                sql_status=sql_status,
                sql_error=sql_error,
            )
        return status

    @classmethod
    def getDatabase(
        cls, name: str, password: str, folder: str = "", folderPassword: str = ""
    ):
        status, database, folder_ = cls.checkDatabase(
            name,
            password,
            folder,
            folderPassword,
        )
        if status == DATABASE_EXISTS:
            status = DictObj(
                status=status,
                name=name,
                folder=database.foldername,
                tablesAndColumns=database.details,
            )

        return status

    @classmethod
    def renameDatabase(
        cls,
        name: str,
        password: str,
        newName: str,
        folder: str = "",
        folderPassword: str = "",
    ):
        status, database, folder_ = cls.checkDatabase(
            name,
            password,
            folder,
            folderPassword,
        )
        if status == DATABASE_EXISTS:
            if not cls._databaseExists(newName, folder, folderPassword):
                databases = folder_.databases if folder_ else cls.databases
                database.rename(newName)
                status = (DATABASE_RENAMED_SUCCESSFULLY,)
                sql_status, sql_error = InternalDB.save(database)

                if sql_status == SUCCESS:
                    databases[newName] = database
                    del databases[name]
                    THREAD_SAVE()

                else:
                    database.rename(name)
                    status = FAILED

                status = DictObj(
                    status=status,
                    name=newName,
                    oldName=name,
                    folder=folder,
                    sql_status=sql_status,
                    sql_error=sql_error,
                )
            else:
                status = NEW_DATABASE_NAME_EXISTS

        return status

    @classmethod
    def dropDatabase(
        cls, name: str, password: str, folder: str = "", folderPassword: str = ""
    ):
        status, database, folder_ = cls.checkDatabase(
            name,
            password,
            folder,
            folderPassword,
        )
        if status == DATABASE_EXISTS:
            databases = folder_.databases if folder_ else cls.databases
            status = DATABASE_DELETED_SUCCESSFULLY
            sql_status, sql_error, _ = InternalDB.delete(database)

            if sql_status == SUCCESS:
                del databases[name]
                database.delete()
                THREAD_SAVE()

            else:
                databases[name] = database
                status = FAILED

            status = DictObj(
                status=status,
                name=name,
                sql_status=sql_status,
                sql_error=sql_error,
            )

        return status

    def __init__(self, name: str, password: str, folder: Folder = None):
        super().__init__(name, password)

        self.folder = folder
        self.tables: DictObj[str, Table] = DictObj()
        self.db = DB(self.path)

    @property
    def path(self):
        root = self.folder.path if self.folder else DatabaseFolder
        return os.path.join(root, f"{self.name}.db")

    @property
    def foldername(self):
        return self.folder.name if self.folder else ""

    @property
    def details(self) -> DictObj:
        details = DictObj()
        for table, table_ in self.tables.items():
            details[table] = table_.details
        return details

    def create(self):
        if not self.exists():
            open(self.path, "w").close()

    def to_json(self) -> str:
        dictObj = DictObj(name=self.name, password=self.password, details=self.details)
        return dictObj.to_json()


class Column:
    def __init__(self, table: "Table", name: str, datatype: str):
        self.table = table
        self.name = name.lower()
        self.datatype = datatype.upper()

    @property
    def details(self):
        return [self.name, self.datatype]


class Table:
    @classmethod
    def checkTable(
        cls,
        database: str,
        password: str,
        table: str,
        folder: str = "",
        folderPassword: str = "",
    ):
        status, database_, folder_ = Database.checkDatabase(
            database,
            password,
            folder,
            folderPassword,
        )
        table_: Table = None

        if status == DATABASE_EXISTS:
            status = TABLE_DOES_NOT_EXISTS

            if table in database_.tables:
                status = TABLE_EXISTS
                table_ = database_.tables[table]

        return status, table_, database_, folder_

    @classmethod
    def createTable(
        cls,
        database: str,
        password: str,
        name: str,
        columns: list[list[str, str]],
        folder: str = "",
        folderPassword: str = "",
    ):
        status, table_, database_, folder_ = cls.checkTable(
            database,
            password,
            name,
            folder,
            folderPassword,
        )
        if status == TABLE_DOES_NOT_EXISTS:
            table_ = Table(database_, name)
            columns_: list[Column] = []
            for column in columns:
                if len(column) == 2:
                    name_, datatype = column
                    if name_ and datatype:
                        column_ = Column(table_, *column)
                        table_.columns[name_] = column_
                        columns_.append(column_)
                    else:
                        return NOT_ENOUGH_VALUES_FOR_COLUMNS
                else:
                    return NOT_ENOUGH_VALUES_FOR_COLUMNS

            statement = Statement.createTable(name, columns_)
            sql_status, sql_error, _ = database_.db.try_exec(statement)

            if sql_status == SUCCESS:
                sql_status, sql_error = InternalDB.save(folder_ or database_)
                if sql_status == SUCCESS:
                    database_.tables[name] = table_

            status = DictObj(
                status=TABLE_CREATED_SUCCESSFULLY,
                name=name,
                database=database_.name,
                folder=database_.foldername,
                sql_status=sql_status,
                sql_error=sql_error,
            )

        return status

    @classmethod
    def dropTable(
        cls,
        database: str,
        password: str,
        name: str,
        folder: str = "",
        folderPassword: str = "",
    ):
        status, database_, folder_ = Database.checkDatabase(
            database,
            password,
            folder,
            folderPassword,
        )
        if status == DATABASE_EXISTS:
            status = TABLE_DOES_NOT_EXISTS
            if name in database_.tables:

                statement = Statement.dropTable(name)
                sql_status, sql_error, _ = database_.db.try_exec(statement)

                if sql_status == SUCCESS:
                    sql_status, sql_error = InternalDB.save(folder_ or database_)
                    if sql_status == SUCCESS:
                        del database_.tables[name]

                status = DictObj(
                    status=TABLE_DELETED_SUCCESSFULLY,
                    name=name,
                    database=database_.name,
                    folder=database_.foldername,
                    sql_status=sql_status,
                    sql_error=sql_error,
                )
        return status

    @classmethod
    def checkColumn(
        cls,
        database: str,
        password: str,
        table: str,
        column: str,
        folder: str = "",
        folderPassword: str = "",
    ):
        status, table_, database_, folder_ = cls.checkTable(
            database,
            password,
            table,
            folder,
            folderPassword,
        )
        column_: Column = None

        if status == TABLE_EXISTS:
            status = COLUMN_DOES_NOT_EXISTS
            if column in table_.columns:
                status = COLUMN_EXISTS
                column_ = table_.columns[column]
        return status, column_, table_, database_, folder_

    @classmethod
    def addColumn(
        cls,
        database: str,
        password: str,
        table: str,
        column: str,
        datatype: str,
        folder: str = "",
        folderPassword: str = "",
    ):
        status, column_, table_, database_, folder_ = cls.checkColumn(
            database,
            password,
            table,
            column,
            folder,
            folderPassword,
        )
        if status == COLUMN_DOES_NOT_EXISTS:
            status = COLUMN_CREATED_SUCCESSFULLY
            column_ = Column(table_, column, datatype)

            statement = Statement.addColumn(table, column, datatype)
            sql_status, sql_error, _ = database_.db.try_exec(statement)

            if sql_status == SUCCESS:
                sql_status, sql_error = InternalDB.save(folder_ or database_)
                if sql_status == SUCCESS:
                    table_[column] = column_

            status = DictObj(
                status=status,
                column=column,
                table=table,
                database=database_.name,
                folder=database_.foldername,
                sql_status=sql_status,
                sql_error=sql_error,
            )

        return status

    # @classmethod
    # def alterColumn(
    #     cls,
    #     database: str,
    #     password: str,
    #     table: str,
    #     column: str,
    #     datatype: str,
    #     folder: str = "",
    #     folderPassword: str = "",
    # ):
    #     status, column_, table_, database_, folder_ = cls.checkColumn(
    #         database,
    #         password,
    #         table,
    #         column,
    #         folder,
    #         folderPassword,
    #     )
    #     if status == COLUMN_EXISTS:
    #         column_.datatype = datatype
    #         status = COLUMN_EDITED_SUCCESSFULLY

    #     return status

    # @classmethod
    # def dropColumn(
    #     cls,
    #     database: str,
    #     password: str,
    #     table: str,
    #     column: str,
    #     folder: str = "",
    #     folderPassword: str = "",
    # ):
    #     status, column_, table_, database_, folder_ = cls.checkColumn(
    #         database,
    #         password,
    #         table,
    #         column,
    #         folder,
    #         folderPassword,
    #     )
    #     if status == COLUMN_EXISTS:
    #         del table_.columns[column]
    #         status = COLUMN_DELETED_SUCCESSFULLY
    #     return status

    def __init__(self, database: Database, name: str):
        self.database = database
        self.name = name
        self.columns: dict[str, Column] = {}

    @property
    def details(self):
        return [column.details for column in self.columns.values()]


class CRUD:
    @classmethod
    def select(
        cls,
        database: str,
        password: str,
        table: str,
        columns: Union[str, list[str]],
        where: str = "",
        folder: str = "",
        folderPassword: str = "",
    ):
        status, database_, _ = Database.checkDatabase(
            database, password, folder, folderPassword
        )

        if status == DATABASE_EXISTS:
            statement = Statement.select(table, columns or "*", where)
            sql_status, sql_error, results = database_.db.try_exec(statement)

            status = DictObj(
                status=status,
                table=table,
                database=database_.name,
                folder=database_.foldername,
                sql_status=sql_status,
                sql_error=sql_error,
            )

        return status

    @classmethod
    def insert(
        cls,
        database: str,
        password: str,
        table: str,
        values: list[Any],
        columns: list[str] = [],
        multiValues: list[list[Any]] = [],
        folder: str = "",
        folderPassword: str = "",
    ):
        status, database_, _ = Database.checkDatabase(
            database, password, folder, folderPassword
        )

        if status == DATABASE_EXISTS:
            status = SUCCESS

            multiValues = multiValues or [values]

            for values in multiValues:
                if values and columns:
                    if len(values) == len(columns):
                        statement = Statement.insert(table, values, columns)
                        sql_status, sql_error, _ = database_.db.try_exec(statement)

                        status = DictObj(
                            status=status,
                            table=table,
                            database=database_.name,
                            folder=database_.foldername,
                            sql_status=sql_status,
                            sql_error=sql_error,
                        )

                    else:
                        status = NOT_ENOUGH_VALUES_FOR_COLUMNS
                        break

            return status

    @classmethod
    def update(
        cls,
        database: str,
        password: str,
        table: str,
        values: list[Any],
        where: str,
        columns: list[str] = [],
        folder: str = "",
        folderPassword: str = "",
    ):
        status, database_, _ = Database.checkDatabase(
            database, password, folder, folderPassword
        )

        if status == DATABASE_EXISTS:
            if len(values) == len(columns):
                statement = Statement.update(table, columns, values, where)
                sql_status, sql_error, _ = database_.db.try_exec(statement)

                status = DictObj(
                    status=status,
                    table=table,
                    database=database_.name,
                    folder=database_.foldername,
                    sql_status=sql_status,
                    sql_error=sql_error,
                )
            else:
                status = NOT_ENOUGH_VALUES_FOR_COLUMNS
        return status

    @classmethod
    def delete(
        cls,
        database: str,
        password: str,
        table: str,
        where: str,
        folder: str = "",
        folderPassword: str = "",
    ):
        status, database_, _ = Database.checkDatabase(
            database, password, folder, folderPassword
        )

        if status == DATABASE_EXISTS:
            statement = Statement.delete(table, where)
            sql_status, sql_error, _ = database_.db.try_exec(statement)

            status = DictObj(
                status=status,
                table=table,
                database=database_.name,
                folder=database_.foldername,
                sql_status=sql_status,
                sql_error=sql_error,
            )

        return status

    @classmethod
    def sql(
        cls,
        database: str,
        password: str,
        table: str,
        statement: str,
        folder: str = "",
        folderPassword: str = "",
    ):
        status, database_, _ = Database.checkDatabase(
            database, password, folder, folderPassword
        )

        if status == DATABASE_EXISTS:
            sql_status, sql_error, results = database_.db.try_exec(statement)

            status = DictObj(
                status=status,
                table=table,
                database=database_.name,
                folder=database_.foldername,
                sql_status=sql_status,
                sql_error=sql_error,
            )

        return status


class Statement:
    @classmethod
    def createTable(cls, table: str, columns: list[Column]):
        statement = f"CREATE TABLE {table} ("
        for column in columns:
            statement += f"{column.name} {column.datatype}, "
        statement = statement[:-2]
        return statement + ");"

    @classmethod
    def dropTable(cls, table: str):
        return f"DROP TABLE {table};"

    @classmethod
    def addColumn(cls, table: str, column: str, datatype: str):
        return f"ALTER TABLE {table} ADD {column} {datatype};"

    # @classmethod
    # def alterColumn(cls, table: str):
    #     return f"DROP TABLE {table};"

    # @classmethod
    # def dropColumn(cls, table: str):
    #     return f"DROP TABLE {table};"

    @classmethod
    def columnString(cls, columns: Union[str, list[str]]):
        if columns and not isinstance(columns, str):
            columns_ = "("
            for column in columns:
                columns_ += f"{column}, "
            columns_ = columns_[:-2]
            columns = columns_ + ")"

        return columns

    @classmethod
    def valueSQL(cls, value) -> str:
        if isinstance(value, str):
            value = f"'{value}'"
        elif isinstance(value, bool):
            value = "true" if value else "false"

        return value

    @classmethod
    def valueString(cls, values: Union[str, list[str]]):
        if not isinstance(values, str):
            values_ = "("
            for value in values:
                values_ += f"{cls.valueSQL(value)}, "
            values_ = values_[:-2]
            values = values_ + ")"

        return values

    @classmethod
    def whereStatement(cls, where: list):
        a, o, b = where
        assert isinstance(o, str), "Operator must be a string e.g +, AND etc."
        o = o.upper()

        if isinstance(a, list):
            a = cls.whereStatement(a)
        else:
            assert isinstance(a, str), "Column name must be a string."

        if isinstance(b, list):
            b = cls.whereStatement(b)
        else:
            b = cls.valueSQL(b)

        return f"({a} {o} {b})"

    @classmethod
    def select(
        cls,
        table: str,
        columns: Union[str, list[str]],
        where: str = "",
    ):
        statement = f"prmp_sql.SELECT {cls.columnString(columns)} FROM {table}"
        if where:
            statement += f" WHERE {where}"
        return statement + ";"

    @classmethod
    def insert(
        cls,
        table: str,
        values: list,
        columns: Union[str, list[str]] = [],
    ):
        return f"INSERT INTO {table} {cls.columnString(columns)} VALUES {cls.valueString(values)};"

    @classmethod
    def equateColumnValues(cls, columns: list[str], values: list):
        res = ""
        for column, value in zip(columns, values):
            res += f"{column} = {cls.valueSQL(value)}, "
        return res[:-2]

    @classmethod
    def update(
        cls,
        table: str,
        columns: list[str],
        values: list[str],
        where: str,
    ):
        return f"UPDATE {table} SET {cls.equateColumnValues(columns, values)} WHERE {where};"

    @classmethod
    def delete(
        cls,
        table: str,
        where: str,
    ):
        return f"DELETE FROM {table} WHERE {where};"


class InternalDB(iDB):
    folders_columns = [
        prmp_sql.UNIQUE(prmp_sql.VARCHAR("name", 255)),
        prmp_sql.TEXT("json"),
    ]
    databases_columns = [
        prmp_sql.UNIQUE(prmp_sql.VARCHAR("name", 255)),
        prmp_sql.TEXT("json"),
    ]

    def __init__(
        self,
    ) -> None:
        super().__init__(SQL_DB, init=True, check_same_thread=False)

        self.create_tables()
        self.load()

    def create_tables(self):
        folders = prmp_sql.CREATE_TABLE(
            "folders", self.folders_columns, check_exist=True
        )
        databases = prmp_sql.CREATE_TABLE(
            "databases", self.databases_columns, check_exist=True
        )

        for table in (folders, databases):
            query: str = str(table)
            self.exec(query)

    def parse_database_json(
        self, name: str, json: str, folder: Folder = None
    ) -> Database:
        databaseDictObj = DictObj.from_json(json)
        database = Database(name, databaseDictObj.password, folder)

        details: DictObj = databaseDictObj.details
        for table_name, columns in details.items():
            table = Table(database, table_name)
            database.tables[table_name] = table

            for column_name, datatype in columns:
                column = Column(table, column_name, datatype)
                table.columns[column_name] = column

        return database

    def load(self):
        results = self.query(prmp_sql.SELECT("*", "folders"))
        if results:
            for name, json in results:
                folder = Folder()
                Folder.folders[name] = folder
                folderDictObj = DictObj.from_json(json)
                databases: DictObj = folderDictObj.databases
                for database_name, json in databases.items():
                    folder.databases[name] = self.parse_database_json(
                        database_name, json, folder
                    )

        results = self.query(prmp_sql.SELECT("*", "databases"))
        if results:
            for name, json in results:
                Database.databases[name] = self.parse_database_json(name, json)

    def save(self, obj: Union[Folder, Database]):
        table = f"{obj.__class__.__name__.lower()}s"
        where = prmp_sql.WHERE(
            prmp_sql.EQUAL_TO_STRING("name", obj.name),
        )
        json = obj.to_json()
        sql_status, sql_error, value = self.check_if_exists(table, where)
        if value:
            statement = prmp_sql.UPDATE(
                table,
                prmp_sql.SET(
                    [
                        prmp_sql.EQUAL_TO_STRING("name", obj.name),
                        prmp_sql.EQUAL_TO_STRING("json", json),
                    ],
                ),
                where=where,
            )
        elif value == False:
            statement = prmp_sql.INSERT(
                table,
                columns=prmp_sql.Columns(
                    ["name", "json"],
                    parenthesis=True,
                ),
                values=prmp_sql.VALUES(
                    [obj.name, json],
                ),
            )
        else:
            return sql_status, sql_error
        return self.try_exec(statement)[:-1]

    def delete(self, obj: Union[Folder, Database]):
        table = f"{obj.__class__.__name__.lower()}s"
        where = prmp_sql.WHERE(
            prmp_sql.EQUAL_TO_STRING("name", obj.name),
        )
        statement = prmp_sql.DELETE(table, where)
        return self.try_exec(statement)


InternalDB = InternalDB()


def SAVE():
    dictObj = DictObj(folders=Folder.folders, databases=Database.databases)
    file = open(PICKLE_DB, "wb")
    pickle.dump(dictObj, file)


def THREAD_SAVE():
    threading.Thread(target=SAVE).start()


def LOAD():
    try:
        file = open(PICKLE_DB, "rb")
        dictObj = pickle.load(file)

        Folder.folders = dictObj.folders
        Database.databases = dictObj.databases

    except (FileNotFoundError, EOFError, TypeError) as err:
        SAVE()
