@echo off
del database_server.zip

PRMP_ZipPath.exe C:\Users\Administrator\Desktop\GITHUB_PROJECTS\database_server
move ..\database_server.zip .

@REM del prmp_sql.zip
@REM PRMP_ZipPath.exe C:\Users\Administrator\Desktop\GITHUB_PROJECTS\PRMP_SQL\prmp_sql
@REM move C:\Users\Administrator\Desktop\GITHUB_PROJECTS\PRMP_SQL\prmp_sql.zip .
