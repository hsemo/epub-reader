#!/usr/bin/env python3

import sys
import os

from viewer import Viewer

help_text = """Usage: python3 main.py <path_to_epub_file.epub>
"""
if len(sys.argv) <= 1:
    print(help_text)
    sys.exit(0)

file_path = sys.argv[1]

v = Viewer(file_path)
v.view()
