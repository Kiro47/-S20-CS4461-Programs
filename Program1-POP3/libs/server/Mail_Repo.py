# System Imports
import os
import logging

# Local Imports
from libs.Messages import Message

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
                    #self.logging.debug("Loading message[{}]: [{}]".format(self.mail_count, file_data))
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

