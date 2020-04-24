#!/usr/bin/python3

import logging
import re

from .utils import is_IPV4


class Actions(object):

    """
    """

    def __init__(self):
        """
        """
        self.logging = logging.getLogger(self.__class__.__name__)

    def validate_command(self, vertex, cmd:str, port:int, ip:str):
        """
        """
        self.logging.debug("Command parsing: vertex [{vertex}], cmd [{cmd}], port [{port}], ip [{ip}]".format(
            vertex=vertex, cmd=cmd, port=port, ip=ip
            ))
        # Check if cmd is valid
        cmd = cmd.upper()
        if cmd == "ADD" or cmd == "DELETE":
            pass
        else:
            raise ValueError("Invalid command value: {}".format(cmd))
        # Check port is valid
        if isinstance(port, int):
            pass
        else:
            raise ValueError("Invalid Port value: {}".format(port))
        # Check ip is valid
        if is_IPV4(ip):
            pass
        else:
            raise ValueError("Invalid IPv4 value: {}".format(ip))

    def command(self, vertex, cmd:str, port:int, ip:str):
        """
        """
        try:
            self.validate_command(vertex, cmd, port, ip)
        except ValueError as error:
            # TODO: Send pack to socket
            error_msg = str(error)
            self.logging.error(error_msg)
        # Do stuff
        pass

    def login(self, vertex):
        """
        """
        pass

    def add(self, vertex, port:int, ip:str):
        """
        """
        pass

    def delete(self, vertex, port:int):
        """
        """
        pass
