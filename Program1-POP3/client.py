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
        self.client_init(hostname, port)

    def client_init(self, hostname: str, port: int):
        """
        Main Client init
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
        # Check for greeting
        # MAGIC_NUMBER: Exact Greeting Size expected
        greeting = sock.recv(23)
        if greeting.decode("utf-8") == "+OK POP3 server ready":
            print(greeting.decode("utf-8"))
        else:
            self.logging.error("Error with connection, aborting.")
            self.logging.error(greeting)
            return
        # Start interactions
        self.client_runner(sock)


    def client_runner(self, socket):
        """
        """
        while True:
            action = self.get_action()
            self.logging.debug("Running Action: [{}]".format(action))
            # Perform Action, and be annoyed by the lack of switch statements
            if action == "STAT":
                pass
            elif action == "LIST":
                pass
            elif action == "DELE":
                pass
            elif action == "TOP":
                pass
            elif action == "QUIT":
                # Send Msg and Close Conn
                # TODO: Send msg
                print("Closing Client")
                socket.close()
                break
                pass
            elif action == "LIST":
                pass
            else:
                # Shouldn't happen due to get_action verification
                self.logging.error("Error, unknown action specified")
            continue
        return

    def get_action(self):
        """
        Gets the action to perform

        :return: Action String to perform
        """
        # Defined by RFC 1939, only 5 request from ASSIGNMENT
        #   (5 are listed, but the number 6 is stated)
        # Note: Assignment says "DETE" not "DELE" mostly positive that's a typo.
        available_actions = ["STAT", "LIST", "DELE", "TOP", "QUIT"]
        # Eventually the user will provide correct input
        while True:
            # Get input, couldn't find official phrase for this in RFC
            action = input("Input Command: ").rstrip()
            for avail in available_actions:
                if avail == action:
                    self.logging.debug("Approved Action [{}]".format(action))
                    return action
        return None


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
