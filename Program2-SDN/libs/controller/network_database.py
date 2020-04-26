#!/usr/bin/python3

import logging

from ..shared.packets import Adjacency_Matrix_Packet

class Network_State:

    """
    Network Data (singleton)
    """

    # there's so many ways to store the data, but just abusing this packet seemed so much easier
    adjacency_packet = None

    def __call__(self):
        return self
    # storage for the instance reference
    #__instance = None

#    class __impl:
#        """
#        binding for singleton implementation
#        """
#
#        def single(self):
#            return id(self)

    def __init__(self):
        """
        """
        # Check whether we already have an instance
        #if Network_State.__instance is None:
            # Create and remember instance
            #Network_State.__instance = Network_State.__impl()
        self.logging = logging.getLogger(self.__class__.__name__)

        # Store instance reference as the only member in the handle
#        self.__dict__['_Singleton__instance'] = Network_State.__instance

#    def __getattr__(self, attr):
#        """
#        Delegate access to implementation
#        """
#        return getattr(self.__instance, attr)
#
#    def __setattr__(self, attr, value):
#        """
#        Delegate access to implementation
#        """
#        return setattr(self.__instance, attr, value)

    def initialize(self, packet:Adjacency_Matrix_Packet):
        """
        """
        self.logging.info("Initializing first matrix: \n[\n{}]".format(packet))
        self.adjacency_packet = packet

    def login(self, vertex_id:int):
        """
        """
        pass

    def update_port(self, vertex:int, port:int, ip:str):
        """
        """
        packet = self.adjacency_packet
        vertex = int(vertex)
        # Update packet
        ipVertex = None
        for host_data in packet.host_data:
            if host_data and host_data.ip == ip:
                ipVertex = int(host_data.vertex_id)
                self.logging.debug("Vertex[{}] found for IP[{}]".format(ipVertex, ip))

        self.logging.debug("Packet: [{}]".format(packet.host_data[vertex]))
        connections = packet.host_data[vertex].connections
        self.logging.debug("Connections: [{}]".format(connections))
        for index, val in enumerate(connections):
            connections[index] = val.strip()
        # Because ports start at 1
        if ip == "0.0.0.0":
            connections[ipVertex ] = 0
        else:
            connections[ipVertex ] = port
        self.logging.debug("New Connections: [{}]".format(connections))
        packet.host_data[vertex].connections = connections
        self.logging.debug("New packet: [\n{}]".format(packet))
        self.adjacency_packet = packet



