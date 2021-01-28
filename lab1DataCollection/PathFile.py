import os
from sys import platform

try:
    # Windows
    script_dir = os.path.dirname(__file__)
    if platform == "win32":
        READFILE_CSV = script_dir + "\..\\Storage\\CSV\\"

    else:
        READFILE_CSV = script_dir + "/../Storage/CSV/"


except ImportError as e:
    print('Error:')
    raise e
