def only_isalpha(str_: str) -> str:
    """The func return only alpha symbols from str"""
    return "".join(s for s in str_ if s.isalpha())
