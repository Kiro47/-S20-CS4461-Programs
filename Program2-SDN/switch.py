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
    # TODO: Add CIDR support for below
    parser.add_argument("--controller_host", type=str,
            help="Host to connect to routing program (defaults to 'localhost')")

    parser.add_argument("ControllerPort", type=int,
            help="Port to listen to incoming connections from switches")
    return parser.parse_args()

def main():
    # Handle CLI Args
    args = form_cli_args()

    # Mode Check
    check_debug_mode(args.debug)

    host = None
    # Set default args
    if not args.controller_host:
        logging.debug("'--controller_host' empty, set to localhost")
        controller_host = "localhost"
    else:
        controller_host = args.controller_host
    # Start Logs
    logging.info("Connecting to controller at [{}] on port [{}]".format(
        controller_host, args.ControllerPort))
    # Start things

if __name__ == "__main__":
    main()
