#!/usr/bin/python3

import argparse
import logging

from libs.shared.utils import check_debug_mode, is_file_path
from libs.routing.server import RoutingServer

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
    parser.add_argument("--controller_host", type=str,
            help="Host to connect to routing program (defaults to 'localhost')")

    parser.add_argument("ListenerPort", type=int,
            help="Port to listen to incoming connections from switches")
    return parser.parse_args()

def start_server(listening_range:str, listening_port:int):
    """
    Wrapper to start controller listening server
    """
    RoutingServer(listening_range, listening_port)

def main():
    # Handle CLI Args
    args = form_cli_args()

    # Mode Check
    check_debug_mode(args.debug)

    host = None
    # Set default args
    if not args.listening_range:
        logging.debug("'--listening_range' empty, set to localhost")
        listening_range = "localhost"
    else:
        listening_range = args.listening_range

    if not args.controller_host:
        logging.debug("'--controller_host' empty, set to localhost")
        controller_host = "localhost"
    else:
        controller_host = args.controller_host
    # Start Logs
    logging.info("Preparing switch listener for [{}] on port [{}]".format(
        listening_range, args.ListenerPort))
    # Start things
    start_server(listening_range, args.ListenerPort)

if __name__ == "__main__":
    main()
