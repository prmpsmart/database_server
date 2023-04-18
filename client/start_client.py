from src.client.request import Request

request = Request(2)
response = {}

# Folder
folder = "folder"
folderPassword = "folderPassword"
newFolder = "newFolder"

# response = request.folderExists(folder)
# response = request.createFolder(folder, folderPassword)
# response = request.getFolder(folder, folderPassword)
# response = request.renameFolder(folder, folderPassword, newFolder)
# response = request.deleteFolder(folder, folderPassword)

# Database
database = "database"
databasePassword = "databasePassword"
newDatabase = "newDatabase"
# folderPassword = ""
# newFolder = ""

# response = request.databaseExists(
#     database,
#     folder,
#     folderPassword,
# )
# response = request.createDatabase(
#     database,
#     databasePassword,
#     folder,
#     folderPassword,
# )
# response = request.getDatabase(
#     database,
#     databasePassword,
#     folder,
#     folderPassword,
# )
# response = request.renameDatabase(
#     database,
#     databasePassword,
#     newDatabase,
#     folder,
#     folderPassword,
# )
# response = request.dropDatabase(
#     database,
#     databasePassword,
#     folder,
#     folderPassword,
# )

# Table
table = "table"
newTable = "newTable"
columns = ["col1", "col2", "col3"]
column = "col4"
datatype = "TEXT"

# response = request.createTable(
#     database,
#     databasePassword,
#     table,
#     columns,
#     folder,
#     folderPassword,
# )
# response = request.dropTable(
#     database,
#     databasePassword,
#     table,
#     folder,
#     folderPassword,
# )
# response = request.addColumn(
#     database,
#     databasePassword,
#     table,
#     column,
#     datatype,
#     folder,
#     folderPassword,
# )

# CRUD
values = ["val1", "val2", "val3"]
# values = []
columns = [column[0] for column in columns][:]
# columns = '*'
multiValues = [
    values,
    ["val11", "val22", "val33"],
    ["val111", "val222", "val333"],
]
# multiValues = []
where = []

# response = request.select(
#     database,
#     databasePassword,
#     table,
#     columns,
#     where,
#     folder,
#     folderPassword,
# )
# response = request.insert(
#     database,
#     databasePassword,
#     table,
#     values,
#     columns,
#     multiValues,
#     folder,
#     folderPassword,
# )
# response = request.update(
#     database,
#     databasePassword,
#     table,
#     values,
#     columns,
#     where,
#     folder,
#     folderPassword,
# )
# response = request.delete(
#     database,
#     databasePassword,
#     table,
#     where,
#     folder,
#     folderPassword,
# )

# sql
statement = ""

response = request.sql(
    database,
    databasePassword,
    table,
    statement,
    folder,
    folderPassword,
)
