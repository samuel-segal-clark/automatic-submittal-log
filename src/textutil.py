from functools import lru_cache

@lru_cache
def get_text(filepath: str, encoding: str | None='utf-8') -> str:
    output = ''
    with open(filepath, mode='r', encoding=encoding) as file:
        output = file.read()
    return output

@lru_cache
def get_lines(filepath: str, encoding: str | None='utf-8') -> list[str]:
    output = []
    with open(filepath, mode='r', encoding=encoding) as file:
        output = file.readlines()
    return output