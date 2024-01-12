import sys, os
import os
import sys

# add plugin to local PATH
parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))

from src.plugin import UpsetGalgame

if __name__ == "__main__":
    UpsetGalgame()