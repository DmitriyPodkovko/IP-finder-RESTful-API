from config.mobile_operators import OPERATORS
from helpers.replacer import only_isalpha


def checker(operator: str) -> bool:
    """The func check if operator in OPERATORS: dict

    param operator: str
    :return: bool
    """
    op = only_isalpha(str_=operator.upper())

    def subkey_checker(_: str):
        """The func check substring '_' in key of OPERATORS: dict

        :param _: str
        :return: bool
        """
        if not any([_ in key for key in OPERATORS.keys()]):
            return False
        return True

    if subkey_checker(_=op) is not False:
        return True
    return False
