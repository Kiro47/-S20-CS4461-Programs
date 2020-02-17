#!/usr/bin/python3

import argparse
import logging
import os
import re
import socket

from libs.Messages import Message


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
    parser.add_argument("Server_Host",
            help="Hostname to connect to")
    parser.add_argument("Port", type=int,
            help="Port number to connect to")
    return parser.parse_args()

def main():
    # Handle CLI Args
    args = form_cli_args()

    # Mode Check
    check_debug_mode(args.debug)

    # Set mail repo
    if args.Mail_Directory:
        directory = args.Server_Host
    else:
        # This shouldn't ever happen
        logging.error("Server_Host empty")
        return
    # Start Server
    logging.info("Preparing to connecto to [{}] on port [{}]".format(args.Server_Host, args.Port))
    Server(mail_repo, args.Port)

if __name__ == "__main__":
    main()
