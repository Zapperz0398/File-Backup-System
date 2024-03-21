import os
import sqlite3


def establish_database_connection(database_name):
    """
    Establishes a connection to the database.

    Parameters:
    - database_name: Name of the database to connect to
    
    """

    database = sqlite3.connect(database_name)
    database_cursor = database.cursor()

    return database, database_cursor


def map_root_file_system(root_dir: str):
    """
    Maps the entire file system from the root directory.

    Parameters:
    root_dir: The root directory to map

    Returns: file_map (list)
    
    """

    file_system_map = {"Directories": ["C:\\Backup\\"], "Files": []}

    for dirpath, dirname, filename in os.walk(root_dir):
        if "C:\\" in dirpath:
            dirpath = dirpath.removeprefix("C:\\")
            dirpath = r"C:\Backups" + "\\" + dirpath + "\\"
        else:
            print("Error - The program does not support file choosing yet")
        
        file_system_map["Directories"] += [dirpath]

        for file in filename:
            filepath = r"C:\Backups" + "\\" + dirpath + file
            file_system_map["Files"] += [filepath]


def make_directories(file_map):
    for path in file_map:
        os.mkdir(path)


# database, cursor = establish_database_connection("database-map.db")
map_root_file_system("C:\PDM")