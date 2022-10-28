#!/usr/bin/env python3

import os


# for changing current working directory temporarily:
class changeDir:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.abspath(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
