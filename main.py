"""This file is the main file for running all resources & functions to backup files"""

import os
import sqlite3
from dotenv import load_dotenv


def establish_database_connection(database_name):
	"""
	Establishes a connection to the database.
	Creates a database file if none exists with required tables

	Parameters:
	- database_name: Name of the database to connect to
	"""

	if not os.path.exists(database_name):
		with open(database_name, "x", encoding = "utf-8") as _:
			pass

		database = sqlite3.connect(database_name)
		database_cursor = database.cursor()

		create_database_tables(database_cursor)
	else:
		database = sqlite3.connect(database_name)
		database_cursor = database.cursor()

		if not database_table_exists(database_cursor, "Directories"):
			database_cursor.execute("""CREATE TABLE Directories (
										ID int PRIMARY KEY,
										name Text,
										path TEXT)
			""")

		if not database_table_exists(database_cursor, "Files"):
			database_cursor.execute("""CREATE TABLE Files (
								ID int PRIMARY KEY,
								name TEXT,
								path TEXT,
								byte_size int,
								created TEXT,
								last_modified TEXT)
			""")

	return database


def database_table_exists(database_cursor, table_name):
	"""
	Checks if a table exists in a database using a databases cursor object

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
								ID int PRIMARY KEY,
								name Text,
								path TEXT)
	""")

	database_cursor.execute("""CREATE TABLE Files (
								ID int PRIMARY KEY,
								name TEXT,
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

	os.system(f"find {root_dir} > filemap.txt")

	file_system_map = {"Directories": [], "Files": []}
	directory_id = 0
	file_id = 0

	with open("filemap.txt", "r", encoding = "utf-8") as file:
		for line in file:
			path = line.strip()

			if os.path.isdir(path):
				directory_id += 1

				directory_data = {"ID": directory_id, "path": path}
				file_system_map["Directories"] += directory_data
			elif os.path.isfile(path):
				file_id += 1

				file_metadata = os.stat(path)
				file_last_modified_time = file_metadata.st_mtime
				file_size = file_metadata.st_size

				file_data = {"ID": file_id, "path": path, "last_modfied": file_last_modified_time, "size": file_size}
				file_system_map["Files"] += file_data

	return file_system_map


load_dotenv(".env")
ROOT = os.getenv("ROOT_DIR")

DATABASE = establish_database_connection("database-map.db")
map_root_file_system(ROOT)
