#!/usr/bin/python3

import logging
import re
import socket

from ..shared.utils import is_IPV4
from ..shared.data_transfer import recv_data, send_data, recv_greeting
from ..shared.packets import Adjacency_Matrix_Packet, Adjacency_Matrix_Utils
from ..controller.network_database import Network_State

class Actions(object):

    """
    """

    router_sock = None
    network_state = None

    def __init__(self, router_host:str, router_port:int, network_state:Network_State):
        """
        """
        self.logging = logging.getLogger(self.__class__.__name__)
        self.logging.debug("Initializing actions")
        self.network_state = network_state
        self.adj_utils = Adjacency_Matrix_Utils("Controller")
        self.connect_routing(router_host, router_port)

    def connect_routing(self, router_host:str, router_port:int):
        """
        Creates and attaches a socket to routing server
        Establishes self.router_sock as connection

        :router_host: Hostname/IP of the router server
        :router_port: Port number to connect to
        """
        self.logging.info("Connecting to router at [{}] on [{}]".format(router_host, router_port))
        if self.router_sock:
            return
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((router_host, router_port))
        except ConnectionRefusedError as refused:
            self.logging.exception("Unable to connect to routing host [{}]".format(host))
        except Exception as exception:
            self.logging.exception("Exception on connecting to router", exc_info=exception)
        # Client connected, wait for greeting
        if not recv_greeting("Controller", sock):
            return
        # Set socket
        self.logging.info("Connected to router, socked set")
        self.router_sock = sock

    def validate_command(self, vertex:int, cmd:str, port:int, ip:str):
        """
        """
        self.logging.debug("Command parsing: vertex [{vertex}], cmd [{cmd}], port [{port}], ip [{ip}]".format(
            vertex=vertex, cmd=cmd, port=port, ip=ip
            ))
        # Check if cmd is valid
        cmd = cmd.upper()
        if cmd == "ADD" or cmd == "DELETE" or cmd == "EXIT":
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
        Wrapper for ..shared.data_transer send_data

        :sock: Socket to send data on
        :data: Data string to send (pre bytes())
        """
        send_data("Controller", sock, data)

    def login(self, sock:socket, vertex:int):
        """
        Login function from a switch to this controller

        :sock: Socket from the switch connection
        :vertex: Vertex_ID of the switch
        """
        self.logging.info("Received login from: [{addr}] on port [{port}] with vertex_id [{vertex}]".format(
            addr=sock.getpeername()[0], port=sock.getsockname()[1], vertex=vertex
            ))
        self.logging.debug("Packet [{}]".format(self.network_state.adjacency_packet))
        self.logging.info("Getting info for vertex[{}] at [{}]:[{}] for login".format(vertex, sock.getpeername()[0],
            sock.getsockname()[1]))
        send_data("Controller", self.router_sock, (f"{vertex}, " + str(self.network_state.adjacency_packet)))
        data = recv_data("Controller", self.router_sock)
        self.logging.info("Sending forwarding packet from login to vertex[{}] at [{}]:[{}]".format(vertex,
            sock.getpeername()[0], sock.getsockname()[1]))
        self.send_data(sock, data)


    def add(self, sock:socket, vertex:int, port:int, ip:str):
        """
        """
        self.logging.info("Adding connection  for vertex[{}] at [{}]:[{}] : [{}]:[{}]".format(vertex,
            sock.getpeername()[0], sock.getsockname()[1], ip, port))
        self.network_state.update_port(vertex, port, ip)
        send_data("Controller", self.router_sock, (f"{vertex}, " + str(self.network_state.adjacency_packet)))
        data = recv_data("Controller", self.router_sock)
        self.send_data(sock, data)
        self.logging.info("Connection added")


    def delete(self, sock:socket, vertex:int, port:int):
        """
        """
        self.logging.info("Removing connection for vertex[{}] at [{}]:[{}] : Vertex[{}]:Port[{}]".format(vertex,
            sock.getpeername()[0], sock.getsockname()[1], vertex, port))
        self.network_state.update_port(vertex, port, "0.0.0.0")
        self.send_data(self.router_sock, (f"{vertex}, " + str(self.network_state.adjacency_packet)))
        data = recv_data("Controller", self.router_sock)
        self.logging.info("Connection Removed")
        self.send_data(sock, data)

    def exit(self, sock:socket, vertex:int):
        """
        Closes socket and exits client thread

        :sock: Socket to clean up
        :vertex: Vertex ID that is closing
        """
        self.logging.info("Vertex[{vertex}] session from {addr} on port {port} closed".format(
            vertex=vertex, addr=sock.getpeername()[0], port=sock.getsockname()[1]
            ))
        self.logging.debug("Closing socket for vertex: {}".format(vertex))
        sock.close()
        self.send_data(self.router_sock, "EXIT")
        self.router_sock.close()
        exit(0)
