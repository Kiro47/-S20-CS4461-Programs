#!/usr/bin/python3

import argparse
import logging

from libs.shared.utils import check_debug_mode, is_file_path

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

    if not args.router_host:
        logging.debug("'--router_host' empty, set to localhost")
        router_host = "localhost"
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

if __name__ == "__main__":
    main()
