# Database Server (Inspired by MongoDB)
It's a small database server that allows uses of the JSON API to manage databases.


## HTTP request specifications
The specifications is fully written in the [server_request_schema.json](src/server_request_schema.py).

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
.

## ENVs
- For the `client`:
    >  set the Server variable in the client_config.env for the server url of the database server 
- For the `server`:
    > - set the DatabaseFolder variable in the server_config.env for the absolute path of the directory the the databases will be stored in.
    > - set the IdleTime variable in the server_config.env for max time a database connection can be active if there are no requests on it again.
    > - set the Port variable in the server_config.env for the server port for the database server 


## Examples
Example requests are located in the [start_client.py](start_client.py) file. Uncomment the lines needed to test each request, or use the [FRequest](https://github.com/fabiobento512/FRequest) software to make the request for speedy response (as its written in C++).
