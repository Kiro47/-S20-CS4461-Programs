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

class Actions(object):

    """
    """

    socket = None

    def __init__(self, socket):
        """
        """
        self.logging = logging.getLogger(self.__class__.__name__)
        self.socket = socket

    def list(self, mail_repo, argument):
        """
        """
        if argument:
            pass
        else:
            # Get size of all mail
            mail_size = 0
            for uid,mail in mail_repo.mail_cache.items():
                mail_size += mail.msg_size
            # Signal received
            self.socket.send(bytes(
                "+OK {count} messages ({size} octets)\r\n".format(
                    count=mail_repo.mail_count,size=mail_size),"utf-8"))
            # Build Rest of Response
            for uid,mail in mail_repo.mail_cache.items():
                self.socket.send(bytes(
                    "S: {uid} {size}\r\n".format(uid=uid,
                        size=mail.msg_size),"utf-8"))
        # Terminate
        self.socket.send(bytes("\r\n.\r\n","utf-8"))


    def stat(self, mail_repo):
        """
        """
        # Get size of all mail
        mail_size = 0
        for uid,mail in mail_repo.mail_cache.items():
            mail_size += mail.msg_size
        # Signal received
        self.socket.send(bytes(
            "+OK {count} {size} \r\n".format(
                count=mail_repo.mail_count,size=mail_size),"utf-8"))
        # Terminate
        self.socket.send(bytes("\r\n.\r\n","utf-8"))

    def top(self, mail_repo, argument):
        """
        """
        self.logging.debug("Top ARGS: [{}]".format(argument))
        msg_num = None
        lines = None
        # Arg parsing
        if not argument:
            self.socket.send(bytes("-ERR No arguments provided","utf-8"))
            self.socket.send(bytes("\r\n.\r\n","utf-8"))
            return
        arguments = argument.split(" ")
        if len(arguments) > 2:
            self.socket.send(bytes("-ERR Too many arguments provided","utf-8"))
            self.socket.send(bytes("\r\n.\r\n","utf-8"))
            return
        try:
            msg_num = int(arguments[0])
            lines = int(arguments[1])
            if msg_num < 0 or lines < 0:
                # quick hack to jump to except
                raise Exception
        except:
            self.socket.send(bytes("-ERR Invalid message number or line number specified","utf-8"))
            self.socket.send(bytes("\r\n.\r\n","utf-8"))
            return
        # Time to actually do stuff
        email = mail_repo.mail_cache[msg_num]
        if not email:
            self.socket.send(bytes("-ERR Mail ID specified does not exist","utf-8"))
            self.socket.send(bytes("\r\n.\r\n","utf-8"))
            return
        # Now write the message
        self.socket.send(bytes("+OK\r\n","utf-8"))
        # Headers
        for header_key,header_value in email.headers.items():
            self.socket.send(bytes("{header}: {value}\n".format(
                header=header_key, value=header_value),"utf-8"))
        # Msg Contents:
        self.socket.send(bytes("\r\n","utf-8"))
        line_counter = 1
        for line in email.message_contents.split("\n"):
            self.logging.debug("Line[{}] content[{}]".format(line_counter, line))
            # Hit line cap
            if line_counter > lines:
                break
            else:
                self.socket.send(bytes(line + "\n\r","utf-8"))
                line_counter += 1
        self.socket.send(bytes("\r\n.\r\n","utf-8"))
        return


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

        action = Actions(sock)
        data = ""
        while True:
            # Wait on recv
            data += sock.recv(1024).decode("utf-8")
            if not data:
                break
            self.logging.debug("Host [{}] msg: [{}]".format(hostname,data.rstrip()))
            data = data.rstrip().split(" ",1)
            command = data[0].upper()
            argument = data[1].lstrip() if (len(data) > 1) else None
            # Process commands
            if command == "STAT":
                action.stat(self.mail_repo)
                self.logging.debug("Finsihed STAT cmd")
            elif command == "LIST":
                action.list(self.mail_repo, argument)
                self.logging.debug("Finished LIST cmd")
            elif command == "DELE":
                pass
            elif command == "TOP":
                action.top(self.mail_repo, argument)
                self.logging.debug("Finished TOP cmd")
            elif command == "QUIT":
                # Send Msg and Close Conn
                # TODO: Send msg
                self.logging.info("Request closing connection from [{}]".format(hostname))
                sock.send(bytes("+OK\r\n","utf-8"))
                sock.close()
                self.logging.info("Connected from [{}] closed.".format(hostname))
                break
            else:
                # Shouldn't happen due to get_action verification
                self.logging.error("Error, unknown action specified")
            data = ""


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
