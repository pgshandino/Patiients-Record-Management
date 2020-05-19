


import sys
from cx_Freeze import setup, Executable

# replaces commandline arg 'build'
sys.argv.append("build")

# change the filename to your program file --->
filename = "main.py"

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = 'Hospital Records Management System',
    version = '1.0.0',
    description = "A hospital patients record management system.",
    executables = [Executable(filename, base=base)])