#!/usr/bin/python3

import logging
import re

from .utils import is_IPV4


class Actions(object):

    """
    """

    vertex_id = "None" # Default override at set_vertex_id()

    def __init__(self):
        """
        """
        self.logging = logging.getLogger(self.__class__.__name__)


    def set_vertex_id(self, vertex_id):
        """
        Sets the vertex ID for the client

        :vertex_id: New Vertex ID

        :raise: ValueError if vertex_id does not exist
        """
        if vertex_id:
            self.vertex_id = vertex_id
        else:
            raise ValueError("Invalid vertex_id: {}".format(vertex_id))


    def validate_command(self, action, arguments):
        """
        Validates arguments and presents a notification is there is an error.

        :action: Action to handle
        :arguments: Unparsed arguments to validate

        :return: dict() with potential values (depending on action): 'vertex_id', 'port', 'ip'
                 returns None if there was an issue with validation
        """
        self.logging.debug("Validating Action: Action[{}] with Args[{}]".format(action, arguments))
        args_dict = dict()
        syntax = "Invalid Syntax"
        self.logging.debug("Args: [{}]".format(arguments))
        if arguments:
            arguments = arguments.strip().split(" ")
            for index in range(0, len(arguments) -1):
                arguments[index] = arguments[index].strip()
        try:
            if action == "LOGIN":
                syntax = "LOGIN <VertexID>"
                if len(arguments) == 1:
                    if isinstance(int(arguments[0]), int):
                        args_dict["vertex_id"] = int(arguments[0])
                        return args_dict
            elif action == "FORWARD":
                syntax = "FORWARD <IPV4>"
                if len(arguments) == 1:
                   if is_IPV4(arguments[0]):
                       args_dict["ip"] = arguments[0]
                       return args_dict
            elif action == "ADD":
                syntax = "ADD <PORT> <IPV4>"
                if len(arguments) == 2:
                    if isinstance(int(arguments[0]), int):
                        if is_IPV4(arguments[1]):
                            args_dict["port"] = int(arguments[0])
                            args_dict["ip"] = arguments[1]
                            return args_dict
            elif action == "DELETE":
                syntax = "DELETE <PORT>"
                if len(arguments) == 1:
                    if isinstance(int(arguments[0]), int):
                        args_dict["port"] = int(arguments[0])
                        return args_dict
            elif action == "EXIT":
                # Don't really care about extra args here, just close out
                return args_dict
            else:
                # Shouldn't happen
                self.logging.error("Unable to validate action: Action[{}]".format(action))
                return None
            # Cascading bailout, any non 'return True' statements end up here
            self.logging.debug("Bad validation: Action[{}] with Args[{}]".format(action, arguments))
            print(syntax)
            return None
        except ValueError as value_error:
            self.logging.debug("Value Error for: Action[{}] Arguments[{}]".format(
                action, arguments))
            print(syntax)
            return None
        except Exception as exception:
            self.logging.exception("Error with validating: Action[{}] Arguments[{}]".format(
                action, arguments), exc_info=exception)
            return None

    def command(self):
        """
        Gets user command and verifies commands into usable compontents

        :return: Tuple(action, arguments), where action is the main action,
                 with a dict() of associated arguments (see validate_command() )
        """
        try:
            # Check if cmd is valid
            available_actions = ["LOGIN", "FORWARD", "ADD", "DELETE", "EXIT"]
            while True:
                # Get input
                user_input = input("<Vertex[{}]>: ".format(self.vertex_id)).rstrip().split(" ", 1)
                # Build commmand
                action = user_input[0].rstrip().upper()
                arguments = user_input[1] if len(user_input) > 1 else None
                # Check for valid actions
                for action_item in available_actions:
                    if action_item == action:
                        self.logging.debug("Approved action [{}] with args: [{}]".format(
                            action, arguments))
                        parsed_args = self.validate_command(action, arguments)
                        if parsed_args == None: # == None, due to empty dicts evaluating to false
                            return (action, arguments)
                        else:
                            continue
            return None
        except Exception as exception:
            self.logging.exception("Error with validating: Action[{}] Arguments[{}]".format(
                action, arguments), exc_info=exception)
            return None


    def login(self, vertex):
        """
        """
        pass

    def add(self, vertex, port:int, ip:str):
        """
        """
        pass

    def delete(self, vertex, port:int):
        """
        """
        pass
