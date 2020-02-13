#!/usr/bin/python3

import argparse
import logging
import os.path


class Mail_Repo(object):

    """
    Repository that stores and processes mail requests
    """

    repo_directory = ""

    def __init(self, directory):
        """
        """
        # Set logging info
        self.logging = logging.getLogger(self.__class__.__name__)
        logging.debug("Init for Mail_Repo")
        # Folder that the mail will be stored and gathered from.
        self.repo_directory = directory
        if os.path.isdir(self.repo_directory):
            load_mail()
        elif os.path.exists(self.repo_directory):
            # Is a file, fail
            pass

def check_debug_mode(debug):
    """
    Checks DEBUG flag for switching between log levels

    :debug: Variable to toggle debug or info
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Debugging enabled")
    else:
        logging.basicConfig(level=logging.INFO)

def form_cli_args():
    """
    Construct CLI arguments for server

    :returns: ArgParse object of all arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true",
            help="toggle debug mode")
    return parser.parse_args()

def main():
    # Handle CLI Args
    args = form_cli_args()
    directory = "./testdir" # REPLACEME
    # Handle Mail Repo
    mail_repo = Mail_Repo(directory)

if __name__ == "__main__":
    main()
