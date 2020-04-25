#!/usr/bin/python3

import logging
import socket
import threading

from ..shared.utils import is_IPV4, is_file_path
from ..shared.data_transfer import send_greeting, recv_greeting, send_data, recv_data
from ..shared.packets import Adjacency_Matrix_Utils
from .actions import Actions

class Server(object):

    """
    Server class which handles incoming connections
    from Switches to the controller.
    """

    def __init__(self, listening_range:str, listener_port:int, adj_matrix_file:str, router_host:str, routing_port:int):
        """
        """
        self.logging = logging.getLogger(self.__class__.__name__)
        self.logging.debug("Init for server listener")
        # Verify args
        self.verify_args(listening_range, listener_port, adj_matrix_file) # Let exception rise up
        # Load initial routing
        self.initialize_routing(adj_matrix_file, router_host, routing_port)
        # Start server
        self.server_runner(listening_range, listener_port, router_host, routing_port)

    def initialize_routing(self, adj_matrix_file:str, router_host:str, router_port:int):
        """
        """
        # Build initial tables
        adj_utils = Adjacency_Matrix_Utils("Server")
        packet = adj_utils.parse_initial_packet(adj_matrix_file)
        #adj_utils.parse_packet("0, " + str(packet)) # testing for packet parser
        # Connect to router
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
        self.logging.info("Connected to router, uploading initial adjacency matrix")
        send_data("Controller", sock, str(packet))
        # Wait on forwarding table packet
        forwarding_packet = recv_data("Controller", sock)


    def verify_args(self, listening_range:str, listener_port:int, adj_matrix_file:str):
        """
        Verify initialization arguments for the server are valid

        :listening_range: IPV4 to listen to connections from
        :listener_port: Port number to listen to connections from

        :raise: ValueError when a value is not valid
        """
        # Verify listening_range
        if listening_range == "localhost" or is_IPV4(listening_range):
            pass
        else:
            raise ValueError("Invalid listening range: [{}]".format(listening_range))
        # Verify listener_port
        if isinstance(listener_port, int):
            pass
        else:
            raise ValueError("Invalid listener port: [{}]".format(listener_port))
        if is_file_path(adj_matrix_file):
            pass
        else:
            raise ValueError("Invalid adj matrix file: [{}]".format(listener_port))
        return

    def server_runner(self, listening_range:str, listener_port:int, router_host:str, routing_port:int):
        """
        Controller Switch Listener instance

        :listening_range: IPV4 to listen to traffic from
        :listener_port: Port to listen to traffic on
        """
        self.logging.info("Starting server listener for {listening_range} on port {listener_port}".format(
            listening_range=listening_range, listener_port=listener_port))
        sockets = list()
        # New sockets
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((listening_range, listener_port))
        sock.listen(20)

        # Listening loop
        try:
            while True:
                client_sock, client_addr = sock.accept()
                self.logging.info("Accepting connection from [{}]".format(client_addr))
                sockets.append(client_sock)
                client_thread = threading.Thread(target=self.client_listener, args=(client_sock, client_addr,
                    router_host, routing_port))
                client_thread.start()
        except KeyboardInterrupt as keeb_exception:
            self.logging.info("Shutting down server")
            # Close all sockets and clean up
            self.logging.debug("Closing sockets...")
            for active_socket in sockets:

                if active_socket:
                    active_socket.close()
            sock.close()
            return
        except Exception as exception:
            self.logging.exception("Exception during main listener loop")
            # Close all sockets and clean up
            self.logging.debug("Closing sockets...")
            for active_socket in sockets:
                if active_socket:
                    active_socket.close()
            sock.close()
            return
        return

    def client_listener(self, sock:socket, host:str, router_host:str, routing_port:int):
        """
        Client Listener/interactions

        :sock: Client socket
        :host: Hostname of the client
        """
        # Send connection established message
        send_greeting("Server", sock)
        action = Actions(router_host, routing_port)
        data = ""

        while True:
            # Wait on recv data
            data += sock.recv(1024).decode("utf-8")
            if not data:
                break
            self.logging.debug("Host [{}], msg: [{}]".format(host, data))
            data = data.rstrip().split(",", 4)
            if len(data) != 4:
                # Send back error message
                pass
            else:
                try:
                    vertex = data[0].strip()
                    cmd = data[1].strip()
                    port = int(data[2].strip())
                    addr = data[3].strip()
                except ValueError as valError:
                    self.logging.exception("Exception parsing command: [{}]".format(str(data)),
                            exc_info=valError)
                    data = ""
                    # TODO: send back error on socket
                    continue
                # Perform actions
                action.command(sock, vertex, cmd, port, addr)
                data = ""
