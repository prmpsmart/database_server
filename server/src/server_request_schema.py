SERVER_REQUEST_SCHEMA = """{
    "actions": [
        "FolderExists",
        "CreateFolder",
        "GetFolder",
        "RenameFolder",
        "DeleteFolder",
        
        
        "DatabaseExists",
        "CreateDatabase",
        "GetDatabase",
        "RenameDatabase",
        "DropDatabase",
        
        
        "CreateTable",
        "DropTable",
        "#RenameTable",
        
        
        "AddColumn",
        "#AlterColumn",
        "#DropColumn",
        
        "Select",
        "Insert",
        "Update",
        "Delete",
        
        
        "SQL"
    ],
    "SQL_ERROR" : {
        "sql_status": "Status of the DB operation",
        "sql_error": "Error encountered in the DB operation"
    },
    "status": {
        "S200": {
            "status": 200,
            "message": "Success"
        },
        "S400": {
            "status": 400,
            "message": "Error from SQL"
        },
        
        "S401": {
            "status": 401,
            "message": "Not enough values for each columns."
        },
        
        "S402": {
            "status": 402,
            "message": "Unique constraint failed"
        },
        
        
        
        "S1000":{
            "status": 1000,
            "message": "Folder does not exists."
        },
        "S1001":{
            "status": 1001,
            "message": "Folder exists."
        },
        "S1002":{
            "status": 1002,
            "message": "Folder created successfully."
        },
        "S1003":{
            "status": 1003,
            "message": "Folder's password is incorrect."
        },
        "S1004":{
            "status": 1004,
            "message": "New folder name exists."
        },
        "S1005":{
            "status": 1005,
            "message": "Folder renamed successfully."
        },
        "S1006":{
            "status": 1006,
            "message": "Folder deleted successfully"
        },
        
        
        
        "S2000":{
            "status": 2000,
            "message": "Database does not exists."
        },
        "S2001":{
            "status": 2001,
            "message": "Database exists."
        },
        "S2002":{
            "status": 2002,
            "message": "Database created successfully."
        },
        "S2003":{
            "status": 2003,
            "message": "Database's password is incorrect."
        },
        "S2004":{
            "status": 2004,
            "message": "New Database name exists."
        },
        "S2005":{
            "status": 2005,
            "message": "Database renamed successfully."
        },
        "S2006":{
            "status": 2006,
            "message": "Database dropped successfully"
        },
        
        
        
        "S3000":{
            "status": 3000,
            "message": "Table does not exists."
        },
        "S3001":{
            "status": 3001,
            "message": "Table exists."
        },
        "S3002":{
            "status": 3002,
            "message": "Table created successfully."
        },
        "S3006":{
            "status": 3006,
            "message": "Table dropped successfully"
        },
        
        
        
        "S4000":{
            "status": 4000,
            "message": "Column does not exists."
        },
        "S4001":{
            "status": 4001,
            "message": "Column exists."
        },
        "S4002":{
            "status": 4002,
            "message": "Column created successfully."
        },
        "S4006":{
            "status": 4006,
            "message": "Column dropped successfully"
        },


        
        "S5000":{
            "status": 5000,
            "message": "SQL Error encountered"
        },
        "S5001":{
            "status": 5001,
            "message": "UNIQUE_CONSTRAINT_FAILED"
        },


        "S6000":{
            "status": 6000,
            "message": "INVALID_REQUEST"
        }
    },
    
    
    "schema": {
        "FolderExists": {
            "requestData": {
                "action": "FolderExists",
                "name": "Name of the folder to query about."
            },
            "response": 1000,
            "errors": [1001]
        },
        "CreateFolder": {
            "requestData": {
                "action": "CreateFolder",
                "name": "Name of the folder to create.",
                "password": "Password for the folder"
            },
            "response": 1002,
            "errors": [1001]
        },
        "GetFolder": {
            "requestData": {
                "action": "GetFolder",
                "name": "Name of the folder.",
                "password": "Password for the folder"
            },
            "response": {
                "status": 1001,
                "name": "Name of the folder.",
                "totalDatabases": 3,
                "databases": [
                    "database1",
                    "database2",
                    "database3"
                ]
            },
            "errors": [1000,1003]
        },
        "RenameFolder": {
            "requestData": {
                "action": "RenameFolder",
                "name": "Name of the folder.",
                "password": "Password for the folder",
                "newName": "New name of the folder."
            },
            "response": {
                "status": 1005,
                "name": "New name of the folder.",
                "oldName": "Old name of the folder."
            },
            "error": [1000, 1003, 1004]
        },
        "DeleteFolder": {
            "requestData": {
                "action": "DeleteFolder",
                "name": "Name of the folder.",
                "password": "Password for the folder"
            },
            "response": {
                "status": 1006,
                "name": "Folder name."
            },
            "errors": [1000, 1003]
        },
        
        
        
        "DatabaseExists": {
            "requestData": {
                "action": "DatabaseExists",
                "name": "Name of the database to query about.",
                "folder": "Optional, Folder of the database",
                "folderPassword": "Password of the folder, if paassword if provided."
            },
            "response": 2001,
            "errors": [1000, 1003, 2000]
        },
        "CreateDatabase": {
            "requestData": {
                "action": "CreateDatabase",
                "name": "Name of the new database",
                "password": "Password of the database",
                "folder": "Optional, whether to create a folder for the database. If the folder already exist, then save the database in it. Useful for teams in an organisation willing to have all their databases in a folder in the server.",
                "folderPassword": "If folder is provided, the folder password should be provided too."
            },
            "response": {
                "status": 2002,
                "name": "Name of the database",
                "folder": "folder of the database"
            },
            "errors": [1000, 1003, 2001]
        },
        "GetDatabase": {
            "requestData": {
                "action": "GetDatabase",
                "name": "Name of the database",
                "password": "Password of the database",
                "folder": "Optional, Folder of the database",
                "folderPassword": "Password of the folder, if paassword if provided."
            },
            "response": {
                "status": 2001,
                "name": "Name of the database",
                "folder": "folder of the database",
                "tablesAndColumns": {
                    "table1": [
                        ["column1", "datatype"],
                        ["column2", "datatype"],
                        ["column3", "datatype"]
                    ],
                    "table2": [
                        ["column1", "datatype"],
                        ["column2", "datatype"],
                        ["column3", "datatype"]
                    ]
                }
            },
            "errors": [1000, 1003, 2000,2003]
        },
        "RenameDatabase": {
            "requestData": {
                "action": "RenameDatabase",
                "name": "Name of the database.",
                "password": "Password of the database",
                "folder": "Optional, Folder of the database",
                "folderPassword": "Password of the folder, if paassword if provided.",
                "newName": "New Name of the database."
            },
            "response": {
                "status": 2005,
                "name": "New Name of the database.",
                "oldName": "Old Name of the database."
            },
            "errors": [1000, 2003, 2000, 2003, 2004]
        },
        "DropDatabase": {
            "requestData": {
                "action": "DropDatabase",
                "name": "Name of the database",
                "password": "Password of the database",
                "folder": "Optional, Folder of the database",
                "folderPassword": "Password of the folder, if paassword if provided."
            },
            "response": 2006,
            "errors": [1000, 1003, 2000, 2003]
        },
        
        
        
        "CreateTable": {
            "requestData": {
                "action": "CreateTable",
                "database": "Name of the database",
                "password": "Password of the database",
                "folder": "Optional, Folder of the database",
                "folderPassword": "Password of the folder, if paassword if provided.",
                "name": "Name of the table.",
                "columns": [
                    ["column1", "VARCHAR"],
                    ["column2", "UNIQUE INT"],
                    ["column3", "datatype"]
                ]
            },
            "response": {
                "status": 3002,
                "name": "Name of the table.",
                "database": "Name of the database.",
                "folder": "Name of the folder.",
                "sql_status": "Status of the DB operation",
                "sql_error": "Error encountered in the DB operation"
            },
            "errors": [1000, 1003, 2000, 2003, 3001]
        },
        "DropTable": {
            "requestData": {
                "action": "DropTable",
                "database": "Name of the database.",
                "password": "Password of the database",
                "folder": "Optional, Folder of the database",
                "folderPassword": "Password of the folder, if paassword if provided.",
                "name": "Name of the table."
            },
            "response": {
                "status": 3006,
                "name": "Name of the table.",
                "database": "Name of the database.",
                "folder": "Name of the folder."
            },
            "errors": [1000, 1003, 2000, 2003, 3000]
        },
        
        
        
        "AddColumn": {
            "requestData": {
                "action": "AddColumn",
                "database": "Name of the database.",
                "password": "Password of the database",
                "folder": "Optional, Folder of the database",
                "folderPassword": "Password of the folder, if paassword if provided.",
                "table": "Name of the table.",
                "column": "Name of the column.",
                "datatype": "datatype of the column."
            },
            "response": 4002,
            "errors": [1000, 1003, 2000, 2003, 3000, 4001]
        },
        "#AlterColumn": {
            "requestData": {
                "action": "AlterColumn",
                "database": "Name of the database.",
                "password": "Password of the database",
                "folder": "Optional, Folder of the database",
                "folderPassword": "Password of the folder, if paassword if provided.",
                "table": "Name of the table.",
                "column": "Name of the column.",
                "datatype": "datatype of the column."
            },
            "response": 4005,
            "errors": [1000, 1003, 2000, 2003, 3000, 4000]
        },
        "#DropColumn": {
            "requestData": {
                "action": "DropColumn",
                "database": "Name of the database.",
                "password": "Password of the database",
                "folder": "Optional, Folder of the database",
                "folderPassword": "Password of the folder, if paassword if provided.",
                "table": "Name of the table.",
                "column": "Name of the column."
            },
            "response": 4006,
            "errors": [1000, 1003, 2000, 2003, 3000, 4000]
        },
        
        
        
        "Select": {
            "requestData": {
                "action": "Select",
                "database": "Name of the database.",
                "password": "Password of the database",
                "folder": "Optional, Folder of the database",
                "folderPassword": "Password of the folder, if password if provided.",
                "table": "Name of the table.",
                "columns": [
                    "column1",
                    "column2",
                    "column3"
                ],
                "where": [
                    [
                        "column1",
                        "=",
                        "value1"
                    ],
                    "AND",
                    [
                        "column2",
                        "=",
                        "value2"
                    ]
                ]
            },
            "response": {
                "status": 200,
                "message": "Success",
                "columns": [
                    "column1",
                    "column2",
                    "column3"
                ],
                "values": [
                    [
                        "row1_column1",
                        "row1_column2",
                        "row1_column3"
                    ],
                    [
                        "row2_column1",
                        "row2_column2",
                        "row2_column3"
                    ],
                    [
                        "row3_column1",
                        "row3_column2",
                        "row3_column3"
                    ]
                ]
            },
            "errors": [1000, 1003, 2000, 2003, 3000, 4001, 400]
        },
        "Insert": {
            "requestData": {
                "action": "Insert",
                "database": "Name of the database.",
                "password": "Password of the database",
                "folder": "Optional, Folder of the database",
                "folderPassword": "Password of the folder, if password if provided.",
                "table": "Name of the table.",
                "columns": [
                    "column1",
                    "column2",
                    "column3"
                ],
                "values": [
                    "column1",
                    "column2",
                    "column3"
                ],
                "multiValues": [
                    [
                        "row1_column1",
                        "row1_column2",
                        "row1_column3"
                    ],
                    [
                        "row2_column1",
                        "row2_column2",
                        "row2_column3"
                    ],
                    [
                        "row3_column1",
                        "row3_column2",
                        "row3_column3"
                    ]
                ]
            },
            "response": {
                "status": 200,
                "message": "Success"
            },
            "errors": [1000, 1003, 2000, 2003, 3000, 4001, 400, 401, 402]
        },
        "Update": {
            "requestData": {
                "action": "Update",
                "database": "Name of the database.",
                "password": "Password of the database",
                "folder": "Optional, Folder of the database",
                "folderPassword": "Password of the folder, if paassword if provided.",
                "table": "Name of the table.",
                "columns": [
                    "column1",
                    "column2",
                    "column3"
                ],
                "values": [
                    "column1",
                    "column2",
                    "column3"
                ],
                "where": [
                    [
                        "column1",
                        "=",
                        "value1"
                    ],
                    "AND",
                    [
                        "column2",
                        "=",
                        "value2"
                    ]
                ]
            },
            "response": 200,
            "errors": [1000, 1003, 2000, 2003, 3000, 4001, 400, 401, 402]
        },
        "Delete": {
            "requestData": {
                "action": "Delete",
                "database": "Name of the database.",
                "password": "Password of the database",
                "folder": "Optional, Folder of the database",
                "folderPassword": "Password of the folder, if paassword if provided.",
                "table": "Name of the table.",
                "where": [
                    [
                        "column1",
                        "=",
                        "value1"
                    ],
                    "AND",
                    [
                        "column2",
                        "=",
                        "value2"
                    ]
                ]
            },
            "response": 200,
            "errors": [1000, 1003, 2000, 2003, 3000, 4001, 400]
        },
        
        
        
        "SQL": {
            "requestData": {
                "action": "SQL",
                "database": "Name of the database.",
                "password": "Password of the database",
                "folder": "Optional, Folder of the database",
                "folderPassword": "Password of the folder, if paassword if provided.",
                "statement": "The SQL command to issue."
            },
            "response": {
                "status": 200,
                "result": "Data"
            },
            "errors": [400]
        }
    }
}
"""
