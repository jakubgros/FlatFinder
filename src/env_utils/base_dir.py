import sys
import os

_sys_executable_path = os.path.dirname(sys.executable)
_sys_executable_path = os.path.normpath(_sys_executable_path)
_sys_executable_path = _sys_executable_path.split(os.sep)

if "/".join(_sys_executable_path[-3:]) != 'FlatFinder/venv/Scripts':
    raise Exception("FlatFinder/venv/Scripts venv has to be activated")

base_dir = os.sep.join(_sys_executable_path[:-2])
