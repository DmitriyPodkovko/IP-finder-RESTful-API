import re

from config.regex_patterns import IPV4_PATTERN, PORT_PATTERN


def ip_checker(ip: str) -> bool:
    """The func check if ip is valid

    param ip: str
    :return: bool
    """
    if not re.match(IPV4_PATTERN, ip):
        return False
    return True


def port_checker(port: int) -> bool:
    """The func check if port is valid

    param port: int
    :return: bool
    """
    if not (
            re.match(
                PORT_PATTERN, str(port) or not (0 <= port <= 65535))):
        return False
    if port < 0 or port > 2 ** 16:
        return False
    return True
