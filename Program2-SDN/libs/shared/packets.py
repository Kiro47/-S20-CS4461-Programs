#!/usr/bin/env

import logging
from enum import Enum

from .utils import is_file_path

class Host_Data(object):

    """
    """

    def __init__(self, vertex_id:int, ip:str, connections):
        """
        """
        self.vertex_id = vertex_id
        self.ip = ip
        self.connections = connections

    def set_connections(self, connections):
        """
        """
        self.connections = connections

    def set_ip(self, ip):
        """
        """
        self.ip = ip

class Adjacency_Matrix_Packet(object):

    """
    """

    source_vertex = None
    num_vertices = None
    host_data = None


    def __init__(self, vertex:int, host_data):
        """
        """
        self.source_vertex = vertex
        self.host_data = host_data
        self.num_vertices = len(self.host_data)

    def __str__(self):
        """
        String class override, forms into parsable packet
        """
        data = ""
        # Header
        if self.source_vertex == None:
            data += "{num_vertices}\n\n".format(num_vertices=self.num_vertices)
        else:
            data += "{source_vertex}, {num_vertices}\n\n".format(
                    source_vertex=self.source_vertex, num_vertices=self.num_vertices)
        # Hosts list
        for host in self.host_data:
            data += "{vertex_id} = {ip}\n\n".format(vertex_id=host.vertex_id, ip=host.ip)
        # Weird padding (techically useless, but sure)
        data += "\n\n"
        for host in self.host_data:
            for connection in host.connections:
                data += "{connection}, ".format(connection=connection)
            data = data.rstrip()
            data = data.rstrip(",")
            data += "\n\n"
        return data


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


    def parse_initial_packet(self, file_path:str):
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

        self.logger.debug("Parsing packet from file: [{}]".format(file_path))

        # splitlines method handles pesky LF vs CRLF issues
        hosts = None # overwritten by int
        host_set = list()
        curHost = 0
        context = self.Context.NUM_HOSTS
        adj_matrix = None
        # Parse file
        with open(file_path, "r") as data_file:
            for line in data_file.readlines():
                self.logger.debug("Parsing line: [{}]".format(line))
                if not line or not line.strip():
                    #empty line
                    self.logger.debug("Passing empty line")
                    continue
                line = line.strip() # Strip extranous whitespace
                if context == self.Context.NUM_HOSTS:
                    data = line.split(",")
                    self.logger.debug("Parsing NUM_HOST: data[{}]".format(data))
                    if data and len(data) == 1:
                        hosts = int(data[0].strip()) if isinstance(int(data[0].strip()), int) else None
                        self.logger.debug("Parsed: num_vertices[{}]".format
                                (hosts))
                        context = self.Context.HOST_IDEN
                        continue
                if context == self.Context.HOST_IDEN:
                    data = line.split("=",2)
                    self.logger.debug("Context [{}], Data[{}]".format(context, data))
                    if data and len(data) == 2:
                        vertex_id = data[0].strip()
                        ip = data[1].strip()
                        self.logger.debug("Found entry <Vertex>[{}] => <IP>[{}]".format(vertex_id, ip))
                        host_set.append(Host_Data(vertex_id, ip, None))
                        curHost += 1
                        if curHost == hosts:
                            context = self.Context.HOST_CONN
                            curHost = 0
                        continue
                    else:
                        self.logger.error("More data provided than expected")
                        return None
                elif context == self.Context.HOST_CONN:
                    data = line.split(",")
                    self.logger.debug("Context [{}], Data[{}]".format(context, data))
                    if data and len(data) == hosts:
                        # Strip out whitespace
                        for index, value in enumerate(data):
                            data[index] = value.strip()
                        host_set[curHost].set_connections(data)
                        curHost += 1
                        continue
                    else:
                        self.logger.error("More data provided than expected")
                        return None
                else:
                    self.logger.error("Error during parsing, context error")
                    return None
        self.logger.debug("host_set: [{}]".format(host_set))
        adj_matrix = Adjacency_Matrix_Packet(None, host_set)
        self.logger.debug("Returning adj_matrix [\n{}]".format(adj_matrix))
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
        source_vertex_id = None
        host_set = list()
        curHost = 0
        context = self.Context.NUM_HOSTS
        adj_matrix = None
        # Parse string to packet
        for line in data.splitlines():
            # Parse line
            self.logger.debug("Parsing line: [{}]".format(line))
            if not line or not line.strip():
                # empty line
                self.logger.debug("Passing empty line")
                continue
            line = line.strip() # Strip extranous whitespace
            if context == self.Context.NUM_HOSTS:
                data = line.split(",")
                self.logger.debug("Parsing NUM_HOST: data[{}]".format(data))
                if data and len(data) == 2:
                    source_vertex_id = int(data[0].strip()) if isinstance(int(data[0].strip()), int) else None
                    hosts = int(data[1].strip()) if isinstance(int(data[1].strip()), int) else None
                    self.logger.debug("source_vertex:[{source_vertex}], vertices[{vertices}]".format(
                        source_vertex=source_vertex_id, vertices=hosts))
                    context = self.Context.HOST_IDEN
                    continue
                if data and len(data) == 1:
                    # Initialization
                    hosts = int(data[0].strip()) if isinstance(int(data[0].strip()), int) else None
                    self.logger.debug("Initial packet: vertices[{vertices}]".format(vertices=hosts))
                    context = self.Context.HOST_IDEN
                    continue
            elif context == self.Context.HOST_IDEN:
                data = line.split("=",2)
                self.logger.debug("Context [{}], Data[{}]".format(context, data))
                if data and len(data) == 2:
                    vertex_id = data[0].strip()
                    ip = data[1].strip()
                    self.logger.debug("Found entry <Vertex>[{}] => <IP>[{}]".format(vertex_id, ip))
                    host_set.append(Host_Data(vertex_id, ip, None))
                    curHost += 1
                    if curHost == hosts:
                        context = self.Context.HOST_CONN
                        curHost = 0
                    continue
                else:
                    self.logger.error("More data provided than expected")
                    return None
            elif context == self.Context.HOST_CONN:
                data = line.split(",")
                self.logger.debug("Context [{}], Data[{}]".format(context, data))
                if data and len(data) == hosts:
                    # Strip out whitespace
                    for index, value in enumerate(data):
                        data[index] = value.strip()
                    host_set[curHost].set_connections(data)
                    curHost += 1
                    continue
                else:
                    self.logger.error("More data provided than expected")
                    return None
            else:
                self.logger.error("Error during parsing, context error")
                return None
        self.logger.debug("host_set: [{}]".format(host_set))
        adj_matrix = Adjacency_Matrix_Packet(source_vertex_id ,host_set)
        self.logger.debug("Return adj_matrix [\n{}]".format(adj_matrix))
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
