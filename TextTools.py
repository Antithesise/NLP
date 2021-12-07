"""
https://stackoverflow.com/a/15861773/15081390
https://stackoverflow.com/a/266162/15081390
"""

from collections import Counter
from string import punctuation

with open("big.txt") as f:
        words = f.read().split()


def wrd(text: str) -> list[str]: # split a paragraph into words
    """
    Split a paragraph to a list of words, ommiting puntuation and whitespace.

    Args:
        text (str): The text to split

    Returns:
        list[str]: The resulting words in order
    """

    return list(text.translate(str.maketrans("", "", punctuation)).split())


def suffixes(words: list[str], minl: int=2, maxl: int | None=None, no: int=100) -> list[str]:
    """
    Find the suffixes of a list of words.

    Args:
        words (list[str]): Words to find suffixes for.
        minl (int, optional): Minimum length of suffixes to search for. Defaults to 2.
        maxl (int, optional): Maximum length of suffixes to search for. Defaults to None.
        no (int, optional): Numebr of unique suffixes to return (default returns top 100 most common suffixes). Defaults to 100.

    Returns:
        list[str]: The resulting list of suffixes
    """
    sufs = Counter()

    words = list(set(words))

    for lvl in range(minl, maxl + 1):
        for w in words:
            if lvl < len(w):
                s = w[-lvl:]

                sufs[s] = sufs.get(s, 0) + 1

    return [k for k, v in sufs.most_common(no) if v > 1]

def gridify(text: str, w: int, padding: str | None=None) -> list[list[str]]:
    g = []

    for i in range(0, len(text), w):
        if i + w <= len(text):
            g += [list(text[i:i+w])]
        else:
            g += [list((text + padding * w)[i:i+w])]
    
    return g