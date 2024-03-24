import os
import sqlite3


def establish_database_connection(database_name):
    """
    Establishes a connection to the database. Creates a database file if none exists with necessary tables

    Parameters:
    - database_name: Name of the database to connect to
    """

    if not os.path.exists(database_name):
        with open(database_name, "x") as _:
            pass

        database = sqlite3.connect(database_name)
        database_cursor = database.cursor()

        create_database_tables(database_cursor)
    else:
        database = sqlite3.connect(database_name)
        database_cursor = database.cursor()

        if not database_table_exists(database_cursor, "Directories"):
            database_cursor.execute("""CREATE TABLE Directories (
                                        name TEXT PRIMARY KEY,
                                        path TEXT)
            """)

        if not database_table_exists(database_cursor, "Files"):
            database_cursor.execute("""CREATE TABLE Files (
                                name TEXT PRIMARY KEY,
                                path TEXT,
                                byte_size int,
                                created TEXT,
                                last_modified TEXT)
            """)

    return database, database_cursor  # Update returns


def database_table_exists(database_cursor, table_name):
    """
    Checks to see if a table exists in a database using a databases cursor object

    Parameters:
    - databasae_cursor: The cursor the database is associated with
    - table_name: The name of the table to check if it exists

    Returns: bool
    """

    table = database_cursor.execute(f"""SELECT name FROM sqlite_master
                                        WHERE type = 'table'
                                        AND name = '{table_name}'""")

    if table.fetchone is None:
        return False
    else:
        return True


def create_database_tables(database_cursor):
    """
    Creates the tables for the applications database

    Parameters:
    - database_cursor: The cursor the database is associated with
    
    Returns: None
    """
    
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


def map_root_file_system(root_dir: str):
    """
    Maps the entire file system from the chosen directory.

    Parameters:
    root_dir: The root directory to map

    Returns: file_map (list)
    """

    file_system_map = {"Directories": [], "Files": {}}

    for dirpath, dirname, filename in os.walk(root_dir):
        file_system_map["Directories"] += [dirpath]

        for file in filename:
            filepath = dirpath + "\\" + file
            creation_time = os.path.getctime(filepath)
            last_modified = os.path.getmtime(filepath)
            file_size = os.path.getsize(filepath)

            file_system_map["Files"][filepath] = {}
            file_system_map["Files"][filepath]["creation_time"] = creation_time
            file_system_map["Files"][filepath]["last_modified"] = last_modified
            file_system_map["Files"][filepath]["byte_size"] = file_size
            
def make_directories(file_map):  # Update syntax
    for path in file_map:
        os.mkdir(path)


database, cursor = establish_database_connection("database-map.db")
map_root_file_system("C:\PDM")