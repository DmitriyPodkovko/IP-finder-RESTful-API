import re

IPV4_PATTERN = re.compile(
    r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:\.|$)){4}$")

PORT_PATTERN = re.compile(r"^\d{1,5}$")
