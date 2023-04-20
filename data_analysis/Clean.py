import re

remove_chars= ["b'","\\n","*","]","[","\"","'",","]


def clean(input : str):
    """
    Removes characters that look like bytes, auxiliary characters, hyperlinks.
    :param input: text
    :return: string without non-word-relevant characters.
    """
    cleaned = input.replace("\n", "").replace("\r", "")
    for char in remove_chars:
        cleaned = cleaned.replace(char,"")
    regex = r'\bhttps?://\S+'
    cleaned = re.sub(regex, '', cleaned)
    regex = r'\bhttp?://\S+'
    cleaned = re.sub(regex, '', cleaned)
    regex = r'__.*?__'
    cleaned = re.sub(regex, '', cleaned)
    regex = r'\\x.{2}'
    cleaned = re.sub(regex, '', cleaned)
    return cleaned


