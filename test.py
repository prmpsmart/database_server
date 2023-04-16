import os

os.sys.path.append("/storage/emulated/0/Prog/Python/")
from prmp_sql import *
from src.server.models import *

get = lambda code: SERVER_REQUEST_SCHEMA.status[f"S{code}"]


db = DB("test.db", init=True)
q = 1
d = 0

table = "test_table"
where = WHERE(
    AND(
        EQUAL_TO_STRING(
            "column1",
            "value1",
        ),
        EQUAL_TO_STRING(
            "column2",
            "value2",
        ),
    )
)
create = CREATE_TABLE(
    table,
    (
        UNIQUE(VARCHAR("column1")),
        VARCHAR("column2"),
        VARCHAR("column3"),
    ),
    check_exist=0,
)

insert = INSERT(
    table,
    columns=Columns(
        (
            "column1",
            "column2",
            "column3",
        ),
    ),
    values=VALUES(
        (
            "test_value1",
            "value2",
            "value3",
        ),
    ),
)
# statement.columns = ''

update = UPDATE(
    table,
    set=SET(
        [
            EQUAL("column1", CONSTANT("value1")),
            EQUAL("column2", CONSTANT("value2")),
            EQUAL("column3", CONSTANT("value3")),
        ]
    ),
    where=where,
)

drop = DROP_TABLE(table)
select = SELECT("*", table, where=where)
addColumn = ALTER_TABLE(table, ADD_COLUMN(INT("column1")))
alterColumn = ALTER_TABLE(table, ALTER_COLUMN(INT("column1")))
dropColumn = ALTER_TABLE(table, DROP_COLUMN("column1"))
delete = DELETE(table, where)

statement = create
statement = select
statement = drop
statement = dropColumn
statement = alterColumn
statement = addColumn
statement = insert
statement = update
statement = delete

res = db.execute_statement(statement, quietError=q, dry=d)

print(f"Valid = {db.VALIDATE_STATEMENT(str(statement))}")
res = get_error_status(res)


db.commit()
if res:
    print(get(res))
