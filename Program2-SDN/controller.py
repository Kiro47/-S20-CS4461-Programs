#!/usr/bin/python3

import argparse
import logging
import threading

from libs.shared.utils import check_debug_mode, is_file_path
from libs.shared.packets import Adjacency_Matrix_Utils
from libs.controller.actions import Actions
from libs.controller.server import Server

def form_cli_args():
    """
    Construct CLI arguments for server

    :returns: ArgParse object of all arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true",
            help="toggle debug mode")
    # TODO: Add CIDR support for below two
    parser.add_argument("--listening_range", type=str,
            help="IP to allow connections from (defaults to 'localhost')")
    parser.add_argument("--router_host", type=str,
            help="Host to connect to routing program (defaults to 'localhost')")

    parser.add_argument("RoutingPort", type=int,
            help="Port to connect to routing program")
    parser.add_argument("ListenerPort", type=int,
            help="Port to listen to incoming connections from switches")
    parser.add_argument("InitialMatrix", type=is_file_path,
            help="File containing initial adjacency matirx data")
    return parser.parse_args()

def start_server(listening_range:str, listener_port:int, adj_filepath:str, router_host:str, routing_port:int):
    """
    Wrapper to start switch listening server
    """
    Server(listening_range, listener_port, adj_filepath, router_host, routing_port)

def main():
    # Handle CLI Args
    args = form_cli_args()

    # Mode Check
    check_debug_mode(args.debug)

    host = None
    # Set default args
    listening_range = "localhost"
    if not args.listening_range:
        logging.debug("'--listening_range' empty, set to localhost")
    else:
        listening_range = args.listening_range

    router_host = "localhost"
    if not args.router_host:
        logging.debug("'--router_host' empty, set to localhost")
    else:
        router_host = args.router_host
    # Start Logs
    logging.info("Preparing to connect to router at [{}] on port [{}]".format(
        router_host, args.RoutingPort))
    logging.info("Preparing switch listener for [{}] on port [{}]".format(
        listening_range, args.ListenerPort))
    logging.info("Loading with inital rules from [{}].".format(
        args.InitialMatrix))
    # Start things
    start_server(listening_range, args.ListenerPort, args.InitialMatrix, router_host, args.RoutingPort)

if __name__ == "__main__":
    main()
