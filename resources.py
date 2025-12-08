# paths.py
import os
import sys

def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works in:
    - normal 'python main.py'
    - PyInstaller onefile exe
    """
    if hasattr(sys, "_MEIPASS"): 
        base_path = sys._MEIPASS
    else: 
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)
