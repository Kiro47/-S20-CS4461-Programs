#!/usr/bin/python3

from os import path
import logging

def is_file_path(filepath: str):
    """
    Determines if a given path leads to an existing file

    :path: Filepath string to check for file

    :return: True is filepath has an existing file, false otherwise.
    """
    if path.isfile(filepath):
        return filepath
    raise FileNotFoundError("File [{}] does not exist!".format(filepath))


def check_debug_mode(debug: bool):
    """
    Checks DEBUG flag for switching between log levels

    :debug: Variable to toggle debug or info
    """
    if debug:
        logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s %(levelname)s:%(name)s:%(funcName)s:%(message)s'
                )
        logging.debug("Debugging enabled")
    else:
        logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s %(levelname)s:%(name)s:%(message)s'
                )
    return

