#!/usr/bin/python3


class Node(object):

    """
    """

    def __init__(self, data:str, ip:str, indexloc = None):
        """
        """
        self.data = data
        self.ip = ip
        self.index = indexloc

class Graph(object):

    """
    """

    @classmethod
    def create_from_nodes(self, nodes):
        return Graph(len(nodes), len(nodes), nodes)


    def __init__(self, row, col, nodes = None):
        # set up an adjacency matrix
        self.adjacency_matrix = [[0] * col for _ in range(row)]
        self.nodes = nodes
        for i in range(len(self.nodes)):
            self.nodes[i].index = i


    def connect_dir(self, src_node:Node, dest_node:Node, weight:int = 1):
        """
        Connects src_node to dest_node with a value of weight

        :src_node: Node to be connected from
        :dest_node: Node to be to connected to
        :weight: Value to jump between the nodes
        """
        src_node, dest_node = self.get_index_from_node(src_node), self.get_index_from_node(dest_node)
        self.adjacency_matrix[src_node][dest_node] = weight

    def connect(self, src_node, dest_node, weight = 1):
        """
        Wrapper to connect two nodes together

        :src_node: Source Node
        :dest_node: Destination Node
        :weight: Weight of connection (Default:1)
        """
        self.connect_dir(src_node, dest_node, weight)
        self.connect_dir(dest_node, src_node, weight)

    def connections_from(self, node):
        """
        Get node row of nonzeros, similar to connections_to

        :node: Node to get connections from

        :return: Returns tuple of connections (node, weight)
        """
        node = self.get_index_from_node(node)
        return [(self.nodes[col_num], self.adjacency_matrix[node][col_num]) for col_num in range(len(self.adjacency_matrix[node])) if self.adjacency_matrix[node][col_num] != 0]


    def connections_to(self, node):
        """
        Maps a matrix to columns of the node

        Non-zero elements go to row index
        Only runs on none-zero connections

        :node: Node to map connections of

        :return: Array of tuples of mapping (node, weight)
        """
      node = self.get_index_from_node(node)
      column = [row[node] for row in self.adjacency_matrix]
      return [(self.nodes[row_num], column[row_num]) for row_num in range(len(column)) if column[row_num] != 0]


    def print_adjacency_matrix(self):
        """
        Debug method, prints adjacency_matrix
        """
        for row in self.adjacency_matrix:
            print(row)

    def node(self, index):
        """
        Gets node at index

        :index: Index to access
        """
        return self.nodes[index]


    def remove_conn(self, src_node, dest_node):
        """
        Wrapper for removing the connections between two nodes

        :src_node: Source Node
        :dest_node: Destination Node
        """
        self.remove_conn_dir(src_node, dest_node)
        self.remove_conn_dir(dest_node, src_node)


    def remove_conn_dir(self, src_node, dest_node):
        """
        Remove connection from src_node to dest_nodes

        :src_node: Source Node
        :dest_node: Destination Node
        """
        src_node, dest_node = self.get_index_from_node(src_node), self.get_index_from_node(dest_node)
        self.adjacency_matrix[src_node][dest_node] = 0

    def can_traverse_dir(self, src_node, dest_node):
        """
        Check if two nodes can be accesed from each other

        :src_node: Source Node
        :dest_node: Destination Node

        :return: Boolea, true if accessible, false otherwise
        """
        src_node, dest_node = self.get_index_from_node(src_node), self.get_index_from_node(dest_node)
        return self.adjacency_matrix[src_node][dest_node] != 0

    def has_conn(self, src_node, dest_node):
        """
        Check if two nodes are directly connected

        :src_node: Source node
        :dest_node: Destination Node

        :return: Boolean, true if connected, false otherwise
        """
        return self.can_traverse_dir(src_node, dest_node) or self.can_traverse_dir(dest_node, src_node)

    def add_node(self,node):
        """
        Adds node to graph

        :node: Node to add
        """
        self.nodes.append(node)
        node.index = len(self.nodes) - 1
        for row in self.adjacency_matrix:
            row.append(0)
        self.adjacency_matrix.append([0] * (len(self.adjacency_matrix) + 1))

    def get_weight(self, n1:Node, n2:Node):
        """
        Get weighted distance between two attached nodes

        :n1: First Node
        :n2: Second Node

        :return: Returns int value of weight
        """
        src_node, dest_node = self.get_index_from_node(n1), self.get_index_from_node(n2)
        return self.adjacency_matrix[src_node][dest_node]

    # Allows either node OR node indices to be passed into
    def get_index_from_node(self, node):
        """
        Anonymous value swapping between node and node indexes

        :node: Node object to get index of, or index to get Node of

        :return: Node of index, or index of Node depending on input
        """
        if not isinstance(node, Node) and not isinstance(node, int):
            raise ValueError("node must be an integer or a Node object")
        if isinstance(node, int):
            return node
        else:
            return node.index

    def dijkstra(self, node:Node):
         # Get index of node (or maintain int passed in)
         nodenum = self.get_index_from_node(node)
         # Make an array keeping track of distance from node to any node
         # in self.nodes. Initialize to infinity for all nodes but the
         # starting node, keep track of "path" which relates to distance.
         # Index 0 = distance, index 1 = node hops
         dist = [None] * len(self.nodes)
         for i in range(len(dist)):
             dist[i] = [float("inf")]
             dist[i].append([self.nodes[nodenum]])

         dist[nodenum][0] = 0
         # Queue of all nodes in the graph
         # Note the integers in the queue correspond to indices of node
         # locations in the self.nodes array
         queue = [i for i in range(len(self.nodes))]
         # Set of numbers seen so far
         seen = set()
         while len(queue) > 0:
             # Get node in queue that has not yet been seen
             # that has smallest distance to starting node
             min_dist = float("inf")
             min_node = None
             for n in queue:
                 if dist[n][0] < min_dist and n not in seen:
                     min_dist = dist[n][0]
                     min_node = n

             # Add min distance node to seen, remove from queue
             queue.remove(min_node)
             seen.add(min_node)
             # Get all next hops
             connections = self.connections_from(min_node)
             # For each connection, update its path and total distance from
             # starting node if the total distance is less than the current distance
             # in dist array
             for (node, weight) in connections:
                 tot_dist = weight + min_dist
                 if tot_dist < dist[node.index][0]:
                     dist[node.index][0] = tot_dist
                     dist[node.index][1] = list(dist[min_node][1])
                     dist[node.index][1].append(node)
         return dist
