
# System Modules
import re
import logging

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

