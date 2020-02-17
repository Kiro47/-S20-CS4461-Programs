#!/usr/bin/python3

import argparse
import logging
import os
import re

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
        logging.debug("Parsing message [{}]".format(message))
        parse_message(message)
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
                self.message_contents = self.message_contents.append(line)
                continue
            else:
                # Look for headers
                if re.search(header_pattern, line):
                    # new header found
                    data = line.split(":", 1)
                    current_header = data[0]
                    header_value = data[1]
                    logging.debug("Parsing header[{}], content[{}]".format(
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
                    self.headers[current_header] = self.headers[current_header].append(line)
                    continue
            # All iters handled by continues
        return


class Mail_Repo(object):

    """
    Repository that stores and processes mail requests
    """

    repo_directory = ""
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
            logging.error("Mail Directory is a file, fail Mail_Repo init")
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
        pass

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
                        logging.log("header[{}]=> [{}]".format(header,value))
                        mail.write("{}:{}".format(header,value))
            # Don't care to put in the time to be more narrow
            except Exception as exception:
                logging.exception("Exception saving message at [{}]".format(msg_loc))
            self.mail_count = self.mail_count + 1
        else:
            logging.error("Attempting to save empty Message object... Ignoring")
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
    return parser.parse_args()

def main():
    # Handle CLI Args
    args = form_cli_args()
    directory = "./testdir" # REPLACEME
    # Handle Mail Repo
    mail_repo = Mail_Repo(directory)

if __name__ == "__main__":
    main()
