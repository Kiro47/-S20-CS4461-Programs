#!/usr/bin/python3

import logging

from ..shared.packets import Adjacency_Matrix_Packet, Host_Data, Forwarding_Packet_Table
from .graph import Node, Graph

class Matrix_Data:

    """
    Matrix Data (singleton)
    """


    # storage for the instance reference
    __instance = None

    class __impl:
        """
        binding for singleton implementation
        """

    def __init__(self):
        """
        """
        # Check whether we already have an instance
        if Matrix_Data.__instance is None:
            # Create and remember instance
            Matrix_Data.__instance = Matrix_Data.__impl()
            self.logging = logging.getLogger(self.__class__.__name__)

        # Store instance reference as the only member in the handle
        self.__dict__['_Singleton__instance'] = Matrix_Data.__instance

    def __getattr__(self, attr):
        """
        Delegate access to implementation
        """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """
        Delegate access to implementation
        """
        return setattr(self.__instance, attr, value)

    def initialize(self, packet:Adjacency_Matrix_Packet):
        """
        """
        self.logging.info("Initializing first matrix: \n[\n{}]".format(packet))

    def get_forwarding(self, source_vertex:int, packet:Adjacency_Matrix_Packet):
        """
        """
        self.logging.info("Getting forwarding table for vertex[{}]".format(source_vertex))
        # Setup nodes
        nodes = dict()
        ports = list() # key as node val, value as tuple(dest,port)
        for index, host_data in enumerate(packet.host_data):
            nodes[host_data.vertex_id] = Node(host_data.vertex_id, host_data.ip)
            self.logging.debug("Registed new node: [{}] at index [{}]".format(nodes[host_data.vertex_id],
                host_data.vertex_id))
        # Instance new graph
        graph = Graph.create_from_nodes(list(nodes.values()))
        # Bind connections
        for host_data in packet.host_data:
            # Iterate over connections
            self.logging.debug("Connections for host[{}]: [{}]".format(host_data.vertex_id, host_data.connections))
            for index, connection in enumerate(host_data.connections):
                # If validly connected
                if int(connection):
                    src_node = nodes.get(host_data.vertex_id)
                    dest_node = nodes.get(str(index))
                    graph.connect(src_node, dest_node)
                    ports.append((host_data.vertex_id, dest_node, connection))
                    self.logging.debug("Connected [{}] to [{}] on port [{}]".format(host_data.vertex_id,
                        index, connection))
                    continue
            #
        # All connected
        # Get info and build forwarding table
        # For every node
#        for src_node in nodes.values():
            # Get all shorted paths to each node
        src_node = nodes.get(str(packet.source_vertex))
        fwd_packet = Forwarding_Packet_Table()
        self.logging.info("Paths for vertex[{}]".format(src_node.data))
        for hops, path in graph.dijkstra(src_node):
            if hops == 0:
                # Self pointing
                fwd_packet.add_rule(src_node.ip, 0)
                continue
            if hops < 0:
                # Not reachable
                fwd_packet.add_rule(path[-1].ip, -1)
                pass
            else:
                dest_node = path[-1].data
                fwd_node = path[1].data
                for vertex_id, port_dest_node, port_dest_val  in ports:
                    if str(path[0].data) == str(vertex_id) and str(port_dest_node.data) == str(fwd_node):
                        fwd_port = port_dest_val
                self.logging.debug(("For vertex [{src_vertex}] to get to vertex[{dest_node}] send to "
                    + "vertex[{fwd_node}] on port[{fwd_port}]").format(src_vertex=src_node.data, dest_node=dest_node,
                        fwd_node=fwd_node, fwd_port=fwd_port ))
                # Add rule to fwd table
                fwd_packet.add_rule(path[-1].ip, fwd_port)
        self.logging.debug("Forwarding packet for vertex[{}]: {}".format(packet.source_vertex, str(fwd_packet)))
        return fwd_packet
