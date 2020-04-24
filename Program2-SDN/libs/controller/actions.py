#!/usr/bin/python3

import logging
import re
import socket

from .utils import is_IPV4


class Actions(object):

    """
    """

    def __init__(self):
        """
        """
        self.logging = logging.getLogger(self.__class__.__name__)

    def validate_command(self, vertex:int, cmd:str, port:int, ip:str):
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
        # Check vertex is valid
        if isinstance(int(vertex), int):
            pass
        else:
            raise ValueError("Invalid vertex value: {}".format(port))


    def command(self, sock:socket, vertex:int, cmd:str, port:int, ip:str):
        """
        """
        try:
            self.validate_command(vertex, cmd, port, ip)
        except ValueError as error:
            error_msg = str(error)
            self.logging.error(error_msg)
            self.send_data(sock, "ERROR, {}".format(error_msg))
            return
        # Do commands
        if cmd == "ADD":
            if ip == "0.0.0.0" and port == 0:
                # Login Auth
                self.login(sock, vertex)
            else:
                # Assume add command
                # If they request something dumb like 0.0.0.0 w/ port -21
                # we're going to assume they know what they're doing
                self.add(sock, vertex, port, ip)
        elif cmd == "DELETE":
            # Assume they actually know what they're doing
            self.delete(sock, vertex, port)
        elif cmd == "EXIT":
            self.exit(sock, vertex)
        return


    def send_data(self, sock:socket, data:str):
        """
        Sends data to socket with proper start/end headers

        :sock: Socket to send data on
        :data: Data string to send (pre bytes())
        """
        data_start = "-- DATA START --"
        data_end = "-- DATA END --"
        data_packet = data_start + data + data_end
        sock.send(bytes(data_packet,"utf-8"))


    def login(self, sock:socket, vertex:int):
        """
        Login function from a switch to this controller

        :sock: Socket from the switch connection
        :vertex: Vertex_ID of the switch
        """
        # TODO: get data from adjacency matrix
        data = "TEST LOGIN"  # Temp until the above is fiured out
        self.logging.info("Received login from: [{addr}] on port [{port}] with vertex_id [{vertex}]".format(
            addr=sock.getpeername()[0], port=sock.getsockname()[1], vertex=vertex
            ))
        self.send_data(sock, data)


    def add(self, sock:socket, vertex:int, port:int, ip:str):
        """
        """
        data = "TEST ADD"
        self.send_data(sock, data)


    def delete(self, sock:socket, vertex:int, port:int):
        """
        """
        data = "TEST DELETE"
        self.send_data(sock, data)

    def exit(self, sock:socket, vertex:int):
        """
        Closes socket and exits client thread

        :sock: Socket to clean up
        :vertex: Vertex ID that is closing
        """
        self.logging.debug("Closing socket for vertex: {}".format(vertex))
        sock.close()
        exit(0)
