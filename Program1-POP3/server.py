#!/usr/bin/python3

# System Modules
import argparse
import logging
import os
import re
import socket
import threading

# Project Imports
from libs.Messages import Message
from libs.server.Mail_Repo import Mail_Repo

class Server(object):

    """
    Server loop instance
    """

    mail_repo = None

    def __init__(self, mail_repo: Mail_Repo, port: int):
        """
        Server instnace

        :mail_repo: Mail repo object
        :port: Port to start on
        """
        # Set logging info
        self.logging = logging.getLogger(self.__class__.__name__)
        logging.debug("Init for Server Listener")
        if mail_repo:
            self.mail_repo = mail_repo
        else:
            logging.error("Mail Repo instance does not exit!")
            return
        self.server_runner(port)

    def client_listener(self, sock, hostname: str):
        """
        Client Listener/interactions

        :sock: Client Socket
        :hostname: Hostname of client
        """
        # Greet and begin
        sock.send(bytes("+OK POP3 server ready","utf-8"))

    def server_runner(self, port: int):
        """
        Main Server runner instance
        """
        sockets = list()
        # new socket setup
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", port))
        sock.listen(10)

        try:
            while True:
                client_sock, client_addr = sock.accept()
                logging.info("Accepting connection from [{}]".format(client_addr))
                sockets.append(client_sock)
                client_thread = threading.Thread(target=self.client_listener, args=(client_sock, client_addr))
                client_thread.start()
        except KeyboardInterrupt as keeb_exception:
            self.logging.info("Shutting down server")
            return
        except Exception as exception:
            self.logging.exception("Exception during main listener loop")
        # Close all client sockets and main socket
        for active_socket in sockets:
            if active_socket:
                active_socket.close()
        sock.close()
        return


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
    parser.add_argument("Port", type=int,
            help="Port number to start on")
    parser.add_argument("Mail_Directory",
            help="Directory to load and store mail from")
    return parser.parse_args()

def main():
    # Handle CLI Args
    args = form_cli_args()

    # Mode Check
    check_debug_mode(args.debug)

    # Set mail repo
    if args.Mail_Directory:
        directory = args.Mail_Directory
    else:
        # This shouldn't ever happen
        logging.error("Mail Directory not found")
        return
    # Handle Mail Repo
    mail_repo = Mail_Repo(directory)
    # Start Server
    logging.info("Starting Server on port: {}".format(args.Port))
    Server(mail_repo, args.Port)

if __name__ == "__main__":
    main()
