import os
import sqlite3


def establish_database_connection(database_name):
    """
    Establishes a connection to the database.

    Parameters:
    - database_name: Name of the database to connect to
    """

    if not os.path.exists(database_name):
        with open(database_name, "x") as _:
            pass

        database = sqlite3.connect(database_name)
        database_cursor = database.cursor()

        database_cursor.execute("""CREATE TABLE Directories (
                                name TEXT PRIMARY KEY,
                                path TEXT)
        """)

        database_cursor.execute("""CREATE TABLE Files (
                                name TEXT PRIMARY KEY,
                                path TEXT,
                                byte_size int,
                                created TEXT,
                                last_modified TEXT)
        """)
    else:
        database = sqlite3.connect(database_name)
        database_cursor = database.cursor()
        
        table = database_cursor.execute("""SELECT name FROM sqlite_master
                                        WHERE type = 'table'
                                        AND name = 'Directories'""")
        
        if table.fetchone() is None:
            database_cursor.execute("""CREATE TABLE Directories (
                                    name TEXT PRIMARY KEY,
                                    path TEXT)
            """)

        table = database_cursor.execute("""SELECT name FROM sqlite_master
                                        WHERE type = 'table'
                                        AND name = 'Files'""")
        
        if table.fetchone() is None:
            database_cursor.execute("""CREATE TABLE Files (
                                name TEXT PRIMARY KEY,
                                path TEXT,
                                byte_size int,
                                created TEXT,
                                last_modified TEXT)
            """)

    return database, database_cursor


def map_root_file_system(root_dir: str):
    """
    Maps the entire file system from the root directory.

    Parameters:
    root_dir: The root directory to map

    Returns: file_map (list)
    """

    file_system_map = {"Directories": ["C:\\Backup\\"], "Files": {}}

    for dirpath, dirname, filename in os.walk(root_dir):
        original_dirpath = dirpath

        if "C:\\" in dirpath:
            dirpath = dirpath.removeprefix("C:\\")
            dirpath = r"C:\Backups" + "\\" + dirpath + "\\"
        else:
            print("Error - The program does not support file choosing yet")
        
        file_system_map["Directories"] += [dirpath]

        for file in filename:
            filepath = original_dirpath + "\\" + file    
            creation_time = os.path.getctime(filepath)
            last_modified = os.path.getmtime(filepath)
            file_size = os.path.getsize(filepath)

            file_system_map["Files"][filepath] = {}
            file_system_map["Files"][filepath]["creation_time"] = creation_time
            file_system_map["Files"][filepath]["last_modified"] = last_modified
            file_system_map["Files"][filepath]["byte_size"] = file_size


def make_directories(file_map):
    for path in file_map:
        os.mkdir(path)


database, cursor = establish_database_connection("database-map.db")
map_root_file_system("C:\PDM")