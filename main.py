import os

def map_root_file_system(root_dir : str):
    """
    Maps the entire file system from the root directory.
    
    """

    file_system_map = {}

    for dirpath, dirname, filename in os.walk(root_dir):
        if "C:\\" in dirpath:
            dirpath = dirpath.removeprefix("C:\\")
            dirpath = r"C:\Backups" + "\\" + dirpath + "\\"
        else:
            print("Error choosing file destination - the program does not support file choosing yet")
            
        os.mkdir(dirpath)

map_root_file_system("C:\PDM")