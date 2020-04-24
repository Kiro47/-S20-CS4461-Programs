#!/usr/bin/python3

import logging
import socket
import threading

from .utils import is_IPV4
from .actions import Actions

class Server(object):

    """
    Server class which handles incoming connections
    from Switches to the controller.
    """

    def __init__(self, listening_range:str, listener_port:int ):
        """
        """
        self.logging = logging.getLogger(self.__class__.__name__)
        self.logging.debug("Init for server listener")
        # Verify args
        self.verify_args(listening_range, listener_port) # Let exception rise up
        # Start server
        self.server_runner(listening_range, listener_port)

    def verify_args(self, listening_range:str, listener_port:int):
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
        return

    def server_runner(self, listening_range:str, listener_port:int):
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
                client_thread = threading.Thread(target=self.client_listener, args=(client_sock, client_addr))
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

    def client_listener(self, sock, host):
        """
        Client Listener/interactions

        :sock: Client socket
        :host: Hostname of the client
        """
        # Send connection established message
        sock.send(bytes("-- CONNECTION ESTABLISHED --", "utf-8"))
        action = Actions()
        data = ""

        while True:
            # Wait on recv data
            data += sock.recv(1024).decode("utf-8")
            if not data:
                break
            self.logging.debug("Host [{}], msg: [{}]".format(host, data.rstrip()))
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
                    # TODO: send back error on socket
                    continue
                # Perform actions
                action.command(vertex, cmd, port, ip)
