#!/usr/bin/python3

import argparse
import logging
import re
import socket

from libs.Messages import Message

class Client_Connection(object):

    """
    Client connection that interacts with user and sends commands
    """

    def __init__(self, hostname: str, port: int):
        """
        Client instance

        :hostname: Hostname to connect to
        :port: Port on hostname to connect to
        """
        self.logging = logging.getLogger(self.__class__.__name__)
        self.logging.debug("Init Client Connection")
        if not hostname:
            self.logging.error("Hostname is invalid")
            return
        if not port:
            self.logging.error("Port is invalid")
            return
        self.client_runner(hostname, port)

    def client_runner(self, hostname: str, port: int):
        """
        Main Client Loop
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((hostname, port))
        except ConnectionRefusedError as refused:
            self.logging.error("Unable to connect to host [{}]".format(hostname))
        except Exception as exception:
            self.logging.exception("Exception on host connection")
            return
        # Client connected


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
    return

def form_cli_args():
    """
    Construct CLI arguments for server

    :returns: ArgParse object of all arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true",
            help="toggle debug mode")
    parser.add_argument("--host",
            help="Hostname to connect to")
    parser.add_argument("Port", type=int,
            help="Port number to connect to")
    return parser.parse_args()

def main():
    # Handle CLI Args
    args = form_cli_args()

    # Mode Check
    check_debug_mode(args.debug)

    host = None
    # Set mail repo
    if not args.host:
        logging.debug("Server_Host empty, set to localhost")
        host = "localhost"
    else:
        host = args.host
    # Start Server
    logging.info("Preparing to connec to [{}] on port [{}]".format(host, args.Port))
    Client_Connection(host, args.Port)

if __name__ == "__main__":
    main()
