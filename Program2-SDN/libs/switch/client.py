#!/usr/bin/python3

import logging
import socket

from .actions import Actions

class Client_Connection(object):

    """
    """

    def __init__(self, connecting_host:str, connecting_port:int):
        """
        """
        self.logging = logging.getLogger(self.__class__.__name__)
        self.logging.debug("Init for client instance")
        # Verify args
        self.verify_args(connecting_host, connecting_port)
        # Start client connection
        self.client_connection(connecting_host, connecting_port)

    def verify_args(self, host:str, port:int):
        """
        Verify initialization arguments for client are valid

        :listening_range: hostname or IPV4 to establish a connection to
        :port: Port number to connect to

        :raise: ValueError when a value is not valid
        """
        # Verify host
        # TODO: validate on IPs and domain, currently just a string check
        if host:
            pass
        else:
            raise ValueError("Invalid Controller host: [{}]".format(host))
        # Verify port
        if isinstance(port, int):
            pass
        else:
            raise ValueError("Invalid Controller port: [{}]".format(port))
        return

    def client_connection(self, host:str, port:int):
        """
        Establishes connection to controller

        :listening_range: hostname or IPV4 to establish a connection to
        :port: Port number to connect to
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((host,port))
        except ConnectionRefusedError as refused:
            self.logging.exception("Unable to connect to controller host [{}]".format(host))
        except Exception as exception:
            self.logging.exception("Exception on connecting to controller", exc_info=exception)
        # Client connected, wait for greeting
        greeting = sock.recv(30)
        if greeting.decode('utf-8') == "-- CONNECTION ESTABLISHED --":
            print(greeting.decode("utf-8"))
        else:
            self.logging.error("Error with connection, aborting.")
            self.logging.error(greeting.decode("utf-8"))
            return
        # Start runner
        self.client_runner(sock)


    def client_runner(self, sock):
        """
        Client handler that handles user input

        :sock: Socket to send actions to the Controller on
        """
        actions = Actions()
        try:
            while True:
                action, arguments = actions.command()
                self.logging.debug("Running Action: [{}] with args [{}]".format(action, arguments))
                # TODO: send stuff
                if action == "LOGIN":
                    actions.login(sock, arguments.get("vertex_id"))
                elif action == "FORWARD":
                    actions.forward(sock, arguments.get("ip"))
                elif action == "ADD":
                    actions.add(sock, arguments.get("port"), arguments.get("ip"))
                elif action == "DELETE":
                    actions.delete(sock, arguments.get("port"))
                elif action == "EXIT":
                    actions.exit(sock)
                    break
        except KeyboardInterrupt as keeb_exception:
            self.logging.debug("\nKeyboard interuption detection, shutting down")
            actions.exit(sock)
            return
