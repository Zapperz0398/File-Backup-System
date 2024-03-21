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
        

        # Current issue right here is that there is no folder 'C:\Backups' in the initial startup. Using try except does not solve the problem

def make_directories(file_map):
    for path in file_map:
        os.mkdir(path)


map_root_file_system("C:\PDM")