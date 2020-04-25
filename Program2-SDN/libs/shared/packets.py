#!/usr/bin/env

import logging

from .utils import is_file_path

class Adjacency_Matrix_Packet(object):

    """
    """


    def __init__(self):
        """
        """
        pass


class Adjacency_Matrix_Utils(object):

    """
    """

    class Context(Enum):
        NUM_HOSTS = 1
        HOST_IDEN = 2
        HOST_CONN = 3

    def __init__(self, app:str):
        """
        """
        self.logger = logging.getLogger(app + ":" + self.__class__.__name__)


    def parse_packet(self, file_path:str):
        """
        Parses data from a file into an Adjacency_Matrix_Packet

        :file_path: File to parse from

        :return: Adjacency_Matrix_Packet from parsed data
        """
        if not file_path:
            self.logger.error("File path empty")
            return None
        if not is_file_path(file_path):
            self.logger.error("File [{}] does not exist!".format(file_path))
            return None

        self.logger.debug("Parsing packet from file: [{}]".format(data))

        # splitlines method handles pesky LF vs CRLF issues
        hosts = None # overwritten by int
        curHost = 0
        context = Context.NUM_HOSTS
        adj_matrix = None

        # Parse file
        with open(file_path, "r") as data_file:
            for line in data_file.readline():
                self.logger.debug("Parsing line: [{}]".format(line))
                if not line:
                    #empty line
                    continue
                line = line.strip() # Strip extranous whitespace
                if context == Context.NUM_HOSTS:
                    pass
                elif context == Context.HOST_IDEN:
                    pass
                elif context == Context.HOST_CONN:
                    pass
                else:
                    self.logger.error("Error during parsing, context error")
                    return None
        self.logger.debug("Return adj_matrix [{}]".format(adj_matrix))
        return adj_matrix


    def parse_packet(self, data:str):
        """
        Parses a data string into an Adjacency_Matrix_Packet

        :data: Data string to parse from

        :return: Adjacency_Matrix_Packet from parsed data
        """
        if not data:
            self.logger.error("Packet data empty")
            return None
        self.logger.debug("Parsing packet from data: [{}]".format(data))

        # splitlines method handles pesky LF vs CRLF issues
        hosts = None # overwritten by int
        curHost = 0
        context = Context.NUM_HOSTS
        adj_matrix = None

        for line in data.splitlines():
            # Parse line
            self.logger.debug("Parsing line: [{}]".format(line))
            if not line:
                # empty line
                continue
            line = line.strip() # Strip extranous whitespace
            if isinstance(line, int):
                self.logger.debug("Number of hosts: [{}]".format(line))
                hosts = int(line)
                context = Context.HOST_IDEN # Move to next parsing segment
                continue
            else:
                # Literally all other lines
                if context == Context.HOST_IDEN:
                    data = line.split("=",2)
                    self.logger.debug("Context [{}], Data[{}]".format(contex, data))
                    if data and len(data) == 2:
                        vertex_id = data[0].strip()
                        ip = data[0].strip()
                        self.logger.debug("Found entry <Vertex>[{}] => <IP>[{}]".format(vertex_id, ip))
                        # TODO: Pack into adj_matrix
                        continue
                    else:
                        self.logger.error("More data provided than expected")
                        return None
                elif context == Context.HOST_CONN:
                    data = line.split(",")
                    self.logger.debug("Context [{}], Data[{}]".format(contex, data))
                    if data and len(data) == hosts:
                        # Strip out whitespace
                        for index, value in enumerate(data):
                            data[index] = value.strip()
                        # TODO: Pack data into adj_matrix
                        continue
                    else:
                        self.logger.error("More data provided than expected")
                        return None
                else:
                    self.logger.error("Error during parsing, context error")
                    return None
        self.logger.debug("Return adj_matrix [{}]".format(adj_matrix))
        return adj_matrix

class Forwarding_Packet_Table(object):

    """
    """

    def __init__(self):
        """
        """
        pass


class Forwarding_Packet_Utils(object):

    """
    """

    def __init__(self, app:str):
        """
        """
        self.logger = logging.getLogger(app + ":" + self.__class__.__name__)
