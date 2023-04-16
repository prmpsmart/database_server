import json

# Database Response Codes

SUCCESS = 200
FAILED = 400
NOT_ENOUGH_VALUES_FOR_COLUMNS = 401
UNIQUE_CONSTRAINT_FAILED = 402

FOLDER_DOES_NOT_EXISTS = 1000
FOLDER_EXISTS = 1001
FOLDER_CREATED_SUCCESSFULLY = 1002
FOLDER_PASSWORD_IS_INCORRECT = 1003
NEW_FOLDER_NAME_EXISTS = 1004
FOLDER_RENAMED_SUCCESSFULLY = 1005
FOLDER_DELETED_SUCCESSFULLY = 1006

DATABASE_DOES_NOT_EXISTS = 2000
DATABASE_EXISTS = 2001
DATABASE_CREATED_SUCCESSFULLY = 2002
DATABASE_PASSWORD_IS_INCORRECT = 2003
NEW_DATABASE_NAME_EXISTS = 2004
DATABASE_RENAMED_SUCCESSFULLY = 2005
DATABASE_DELETED_SUCCESSFULLY = 2006

TABLE_DOES_NOT_EXISTS = 3000
TABLE_EXISTS = 3001
TABLE_CREATED_SUCCESSFULLY = 3002
TABLE_DELETED_SUCCESSFULLY = 3006

COLUMN_DOES_NOT_EXISTS = 4000
COLUMN_EXISTS = 4001
COLUMN_CREATED_SUCCESSFULLY = 4002
COLUMN_EDITED_SUCCESSFULLY = 4005
COLUMN_DELETED_SUCCESSFULLY = 4006

SQL_ERROR = 5000
UNIQUE_CONSTRAINT_FAILED = 5001

INVALID_REQUEST = 6000


class DictObj(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getattr__(self, key):
        if key in self:
            return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def __getstate__(self):
        return dict(self)

    def __setstate__(self, value):
        return self.update(value)

    def to_json(self):
        return json.dumps(self)

    @classmethod
    def from_json(cls, string: str):
        return json.loads(string, object_hook=cls)
