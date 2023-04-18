from src.server.models import *

columns = "*"
columns = ["love", "hate", "json"]
where = [
    ["column1", "=", True],
    "AND",
    ["column2", "=", 67],
]
where2 = [where, "or", where]
table = "test_table"
where = Statement.whereStatement(where2)


# statement = Statement.select(table, columns, )
statement = Statement.insert(table, ["v", "v", "io", 9, False], columns)
# statement = Statement.update(
#     table,
#     ["col1", "col2", "col3"],
#     ["val1", "val2", True],
# )

# where =0
# statement = Statement.delete(table, where=where)
db = DB()

db.init()
try:
    db.exec(statement)

except Exception as e:
    print(e)

print(f"Valid = {db.VALIDATE_STATEMENT(statement)}")
