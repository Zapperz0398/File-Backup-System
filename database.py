"""This file contains all the functions related to local database interaction & minipulation"""

import os
import sqlite3

DATABASE_NAME = "database-map.db"

def open_local_database_connection():
	"""
	Opens a local database connection
	"""

	database = sqlite3.connect(DATABASE_NAME)

	return database


def close_database_connection(database):
	"""
	Closes a local database connection
	"""
	database.close()


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
										path TEXT)
			""")

		if not database_table_exists(database_cursor, "Files"):
			database_cursor.execute("""CREATE TABLE Files (
										ID int PRIMARY KEY,
										path TEXT,
										last_modified TEXT,
										byte_size int)
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
								path TEXT)
	""")

	database_cursor.execute("""CREATE TABLE Files (
								ID int PRIMARY KEY,
								path TEXT,
								last_modified TEXT,
								byte_size int)
	""")


def add_data_to_database(database, data):
	"""
	Adds a mapped file-system data set to a local database
	
	Parameters:
	- database: A local database connection object
	- data: A mapped file-system data set
	
	Returns: None
	"""

	database_cursor = database.cursor()

	for data_set in data["Directories"]:
		directory_id = data_set["ID"]
		directory_path = data_set["path"]

		db_query = """INSERT INTO 'Directories' (ID, path)
			VALUES (?, ?)"""
		database_cursor.execute(db_query, (directory_id, directory_path))
		database.commit()

	for data_set in data["Files"]:
		file_id = data_set["ID"]
		file_path = data_set["path"]
		file_last_modified_time = data_set["last_modified"]
		file_size = data_set["size"]

		db_query = """INSERT INTO 'Files' (ID, path, last_modified, byte_size)
			VALUES (?, ?, ?, ?)"""
		database_cursor.execute(db_query, (file_id, file_path, file_last_modified_time, file_size))
		database.commit()

	database.close()
