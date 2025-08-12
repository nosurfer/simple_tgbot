import re

def escape_markdown(content: str) -> str:
    """
    Escapes Markdown characters in a string of Markdown.

    Credits to: simonsmh

    :param content: The string of Markdown to escape.
    :type content: :obj:`str`

    :return: The escaped string.
    :rtype: :obj:`str`
    """
    
    parse = re.sub(r"([_*\[\]()~`>\#\+\-=|\.!\{\}\\])", r"\\\1", content)
    reparse = re.sub(r"\\\\([_*\[\]()~`>\#\+\-=|\.!\{\}\\])", r"\1", parse)
    return reparse

