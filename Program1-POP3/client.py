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
            action, arguments = self.get_action()
            self.logging.debug("Running Action: [{}]".format(action))
            # Perform Action, and be annoyed by the lack of switch statements
            if action == "STAT":
                socket.send(bytes("STAT\r\n","utf-8"))
            elif action == "LIST":
                if arguments:
                    socket.send(bytes("LIST {}\r\n".format(arguments),"utf-8"))
                else:
                    socket.send(bytes("LIST\r\n".format(arguments),"utf-8"))
            elif action == "DELE":
                if arguments:
                    socket.send(bytes("DELE {}\r\n".format(arguments),"utf-8"))
                else:
                    print("C: Incorrect Usage, Valid: DELE <message_number>")
                    continue
            elif action == "TOP":
                if arguments:
                    socket.send(bytes("TOP {}\r\n".format(arguments),"utf-8"))
                else:
                    print("C: Incorrect Usage, Valid: TOP <message_number> <lines>")
                    continue
            elif action == "QUIT":
                # Send Msg and Close Conn
                # TODO: Send msg
                print("Closing Client")
                socket.send(bytes("QUIT\r\n","utf-8"))
                response = socket.recv(5).decode("utf-8")
                if response == "+OK\r\n":
                    print("Successfully Disconnected")
                else:
                    print("Questionablly Disconnected")
                socket.close()
                exit(1)
                break
            else:
                # Shouldn't happen due to get_action verification
                self.logging.error("Error, unknown action specified")
                continue
            # Process response
            response = socket.recv(1024).decode("utf-8")
            while response[-5:] != "\r\n.\r\n":
                self.logging.debug("Waiting for more input...")
                response += socket.recv(1024).decode("utf-8")
            print(response[:-5])

            continue
        return

    def get_action(self):
        """
        Gets the action to perform

        :return: Tuple(action,arguments) Action to perform and associated arguments
        """
        # Defined by RFC 1939, only 5 request from ASSIGNMENT
        #   (5 are listed, but the number 6 is stated)
        # Note: Assignment says "DETE" not "DELE" mostly positive that's a typo.
        available_actions = ["STAT", "LIST", "DELE", "TOP", "QUIT"]
        # Eventually the user will provide correct input
        while True:
            # Get input, couldn't find official phrase for this in RFC
            user_input = input("C: ").rstrip().split(" ",1)
            # Build CMD + Args
            action = user_input[0].rstrip()
            arguments = user_input[1] if len(user_input) > 1 else None
            for avail in available_actions:
                if avail == action:
                    self.logging.debug("Approved Action [{}]".format(action))
                    return (action, arguments)
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
