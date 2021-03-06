#!/usr/bin/python3

import socket
import logging

def send_data(app:str, sock:socket, data:str):
    """
    Sends data to socket with proper start/end headers

    :app: Which application is sending the data
    :sock: Socket to send data on
    :data: Data string to send (pre bytes())
    """
    logger = logging.getLogger(app)
    data_start = "-- DATA START --"
    data_end = "-- DATA END --"
    data_packet = data_start + data + data_end
    logger.debug("Sending data: [\n{}\n]".format(data_packet))
    sock.send(bytes(data_packet,"utf-8"))

def recv_data(app:str, sock:socket):
    """
    Get response from socket with proper start/end headers

    :app: Which application is receiving the data
    :sock: Socket to pull data from

    :return: String of data received
    """
    logger = logging.getLogger(app)
    data = ""
    data_start = "-- DATA START --"
    data_end = "-- DATA END --"

    data_header = sock.recv(16)
    if data_header.decode("utf-8") == data_start:
        logger.debug("Getting response: [{}]".format(data_header.decode("utf-8")))
    else:
        logger.error("Error with get response, aborting")
        logger.error("data_header: [{}]".format(data_header.decode("utf-8")))
        return None

    while True:
        data += sock.recv(1024).decode("utf-8")
        if data.endswith(data_end):
            # Strip "data_end" from data
            data = data[:-len(data_end)]
            logger.debug("Data received: [{}]".format(data))
            return data
        else:
            logger.debug("Incomplete data received so far: [{]]".format(data))
    return None


def send_greeting(app:str, sock:socket):
    """
    Send greeting message for initial connection

    :app: Which application is sending the data
    :sock: Socket to send greeting on
    """
    sock.send(bytes("-- CONNECTION ESTABLISHED --", "utf-8"))

def recv_greeting(app:str, sock:socket):
    """

    :app: Which application is receiving the data
    :sock: Socket to receive the greeting on

    :return: Boolean, True if valid greeting, false otherwise
    """
    logger = logging.getLogger(app)
    greeting = sock.recv(28)
    if greeting.decode('utf-8') == "-- CONNECTION ESTABLISHED --":
        logger.debug("Connection established with host [{host}] on port [{port}]".format(
            host=sock.getpeername()[0], port=sock.getsockname()[1]))
        print(greeting.decode("utf-8"))
        return True
    else:
        logger.error("Error with connection, aborting.")
        logger.error(greeting.decode("utf-8"))
        return False


