import prmp_sql, threading, time
from typing import Union
from ..commons import *
from .miscs import ENV


def get_error_status(error: Union[Exception, str]):
    error = str(error)

    if error.startswith("no such table: "):
        return TABLE_DOES_NOT_EXISTS

    elif error.startswith("no such column: "):
        return COLUMN_DOES_NOT_EXISTS

    elif error.startswith("table ") and "already exists" in error:
        return TABLE_EXISTS

    elif error.startswith("UNIQUE constraint failed:  "):
        return UNIQUE_CONSTRAINT_FAILED

    return SQL_ERROR, error


class iDB(prmp_sql.Database):
    def _try(self, func, *args, **kwargs) -> Union[int, str, list]:
        sql_status, sql_error, results = SUCCESS, "", []
        try:
            results = func(*args, **kwargs)
        except Exception as err:
            sql_status, sql_error = get_error_status(err)
            sql_error = f"{err.__class__.__name__}: {sql_error}"

        return sql_status, sql_error, results

    def try_exec(self, *args, **kwargs):
        return self._try(self.exec, *args, **kwargs)

    def try_query(self, *args, **kwargs) -> Union[int, str, list]:
        return self._try(self.query, *args, **kwargs)

    def check_if_exists(self, table: str, where: prmp_sql.WHERE) -> bool:
        count_1 = prmp_sql.COUNT(1)
        select = prmp_sql.SELECT(
            count_1,
            table,
            where=where,
            limit=prmp_sql.LIMIT(1),
        )

        sql_status, sql_error, results = self.try_query(select)

        value = None
        if results:
            value = results[0][0] != 0
        elif sql_status == SUCCESS:
            value = False

        return sql_status, sql_error, value


class DB(iDB):
    IdleTime = int(ENV.IdleTime or 5000)

    def __init__(self, *args, **kwargs) -> None:
        self.last_time = 0
        self.count_down_on = False
        super().__init__(*args, **kwargs)

    def init(self):
        if not self.count_down_on:
            self.count_down_on = True
            threading.Thread(target=self.idle).start()

        return super().init()

    def exec(self, *args, **kwargs):
        if not self.initialized:
            self.init()

        return super().exec(*args, **kwargs)

    def idle(self):
        while self.count_down_on:
            if (time.time() - self.last_time) > self.IdleTime:
                self.close()
                self.count_down_on = False
