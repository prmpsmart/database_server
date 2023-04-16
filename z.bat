@echo off
del database_server.zip
del prmp_sql.zip

PRMP_ZipPath.exe C:\Users\Administrator\Desktop\GITHUB_PROJECTS\database_server

PRMP_ZipPath.exe C:\Users\Administrator\Desktop\GITHUB_PROJECTS\PRMP_SQL\prmp_sql

move ..\database_server.zip .
move C:\Users\Administrator\Desktop\GITHUB_PROJECTS\PRMP_SQL\prmp_sql.zip .
