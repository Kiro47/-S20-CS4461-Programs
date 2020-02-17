#!/usr/bin/python3

import argparse
import logging
import os
import re
import socket

class Message(object):

    """
    Mail Message Object
    """

    headers = dict()
    message_contents = None

    def __init__(self, message: str):
        """
        Creates a new message object
        """
        self.logging = logging.getLogger(self.__class__.__name__)
        self.logging.debug("Parsing message [{}]".format(message))
        self.parse_message(message)
        return

    def parse_message(self, message: str):
        """
        Parses the message into the class object contents

        :message: String to parse into a message object
        """
        header_pattern = r"^[\w-]+:"
        current_header = ""
        for line in message.splitlines():
            if self.message_contents is not None:
                # Message parsing started:
                self.message_contents = self.message_contents + line
                continue
            else:
                # Look for headers
                if re.search(header_pattern, line):
                    # new header found
                    data = line.split(":", 1)
                    current_header = data[0]
                    header_value = data[1]
                    self.logging.debug("Parsing header[{}], content[{}]".format(
                        current_header, header_value))
                    # set
                    self.headers[current_header] = header_value
                    continue
                elif "\n" in line:
                    # Start message contents
                    self.message_contents = ""
                    continue
                else:
                    # Still parsing header data, aggregate
                    self.headers[current_header] = self.headers[current_header] + line
                    continue
            # All iters handled by continues
        return


class Mail_Repo(object):

    """
    Repository that stores and processes mail requests
    """

    repo_directory = ""
    mail_cache = dict()
    mail_count = 0

    def __init__(self, directory):
        """
        """
        # Set logging info
        self.logging = logging.getLogger(self.__class__.__name__)
        logging.debug("Init for Mail_Repo")
        # Folder that the mail will be stored and gathered from.
        self.repo_directory = directory
        if os.path.isdir(self.repo_directory):
            self.load_mail()
        elif os.path.exists(self.repo_directory):
            # Is a file, fail
            self.logging.error("Mail Directory is a file, fail Mail_Repo init")
            raise Exception("Mail Directory is a file!")
        else:
            # Create dir and set
            os.mkdir( directory, 0o0755)
        return

    def load_mail(self):
        """
        Loads the mail from the files to a cache

        :mail_count: Class var, used as a counter for mail in box
        TODO: implement details
        """
        for email_path in os.listdir(self.repo_directory):
            try:
                file_data = None
                # Load file into string
                with open(self.repo_directory + "/" + email_path, "r") as email:
                    file_data = email.read()
                # If file_data is something of use
                if file_data:
                    self.logging.debug("Loading message[{}]: [{}]".format(self.mail_count, file_data))
                    # Throw message into cache and increment mail counter
                    self.mail_cache[self.mail_count] = Message(file_data)
                    self.logging.debug("Msg Loaded[{}]: [{}]".format(self.mail_count,
                        str(self.mail_cache[self.mail_count])))
                    self.mail_count = self.mail_count + 1
                    continue
                else:
                    self.logging.error("Unable to load message[{}]".format(self.mail_count))
            except Exception as exception:
                self.logging.exception("Exception Loading mail [{}]".format(email_path))
        return


    def save_message(self, message: Message):
        """
        Saves message to mail repo
        :message: Message to save to disk
        """
        msg_loc = repo_directory + "/email" + str(self.mail_count + 1)
        if message:
            # Save to file
            try:
                with open(msg_loc, "w") as mail:
                    for header,value in message.headers:
                        self.logging.log("header[{}]=> [{}]".format(header,value))
                        mail.write("{}:{}".format(header,value))
            # Don't care to put in the time to be more narrow
            except Exception as exception:
                self.logging.exception("Exception saving message at [{}]".format(msg_loc))
            self.mail_count = self.mail_count + 1
        else:
            self.logging.error("Attempting to save empty Message object... Ignoring")
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
        pass

    def server_runner(self, port: int):
        """
        Main Server runner instance
        """
        sockets = list()
        # new socket setup
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((socket.gethostname(), port))
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
