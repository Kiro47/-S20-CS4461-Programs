#!/usr/bin/python3

import re

ipv4_regex = re.compile("^(\d{1,3}[.]){3}\d{1,3}$")

def is_IPV4(ip_string:str):
    """
    """
    return ipv4_regex.match(ip_string)

