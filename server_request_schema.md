# Operations of Database Server

## HTTP request specifications
The specifications is fully written in the [server_request_schema.json](./server_request_schema.json).

> *where* parameter is in this format:
>
> (column, operator, value)
> ``` sql
> WHERE ((column1 = 'value1') AND (column2 = > 'value2'))
> -- can then be written as 
> -- "where" : [
> --             [ "column1", "=", "value1" ],
> --             "AND",
> --             [ "column2", "=", "value2" ]
> --          ]
> ```

Supported actions are listed below:

- FolderExists
    > Query if a folder name is available to use.
- CreateFolder
    > This create a folder in the server.
- GetFolder
    > This gets a folder details on the server
- RenameFolder
    > This renames a folder on the server
- DeleteFolder
    > This removes a folder and its databases on the server.
- DatabaseExists
    > Query if a database name is available to use.
- CreateDatabase
    > This create a new database on the server.
- GetDatabase
    > This gives the details of the database.
- RenameDatabase
    > This renames a database on the server.
- DropDatabase
    > This deletes a database from the server.
- CreateTable
    > This creates a new table in a database on the server.
- DropTable
    > This deletes a table in a database on the server.
- #RenameTable
    > Not implemented yet.
    > This renames a table in a database on the server.
- AddColumn
    > This add a column in a table in a database on the server.
- #AlterColumn
    > This alter the datatype of a column in a table in a database on the server.
- #DropColumn
    > This drops a column in a table in a database on the server.
- Delete
    > This delete data in a table in a database on the server.    
- Select
    > This queries a database on the server.
    > Columns should be empty to select all columns.
- Insert
    > This adds data in a table in a database on the server.
    > Columns should be empty to insert into all columns.
- Update
    > This update data in a table in a database on the server.
    > Columns should be empty to update all columns.
- SQL
    > This executes SQL statements or commands on a database on the server. Incase of a complex operation, its better to provide a SQL statements to be used.






## Idle Time
If a database is operated on, it waits for 5 minutes, if no other operations are made on it again, the server closes the database.
