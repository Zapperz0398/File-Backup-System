"""This file is the main file for running all resources & functions to backup files"""

import os
from dotenv import load_dotenv

import local_database


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
				file_system_map["Directories"].append(directory_data)
			elif os.path.isfile(path):
				file_id += 1

				file_metadata = os.stat(path)
				file_last_modified_time = file_metadata.st_mtime
				file_size = file_metadata.st_size

				file_data = {
						    "ID": file_id, 
						    "path": path, 
						    "last_modified": file_last_modified_time,
						    "size": file_size}
				file_system_map["Files"].append(file_data)

	return file_system_map


def create_root_filesystem_copy(root_path):
	"""
	Creates an exact copy of the root file path

	Parameters:
	- root_path: The root/parent directory to copy
	"""


load_dotenv(".env")
ROOT = os.getenv("ROOT_DIR")

local_database.establish_database_connection()
ROOT_FILE_MAP = map_root_file_system(ROOT)

local_database.add_data_to_database(ROOT_FILE_MAP)
