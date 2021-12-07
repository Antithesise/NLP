"""
https://www.agiliq.com/assets/code/markovgen.py
"""

from random import randint, choice
from TextTools import words


def MarkovDict(length: int) -> dict[tuple[str], str]:
    mdict = {}

    for i in range(len(words) - length):
        key = tuple(words[i+j] for j in range(length))

        if key in mdict:
            mdict[key].append(words[i + length])
        else:
            mdict[key] = [words[i + length]]
    
    return mdict

def RandText(sentences: int=15, randomness: float=0.8) -> str:
    """
    Generate random text for a given number of sentences.

    Args:
        sentences (int, optional): Number of sentences to generate. Defaults to 15.
        randomness (float, optional): How random the text is (0.0-1.0). Defaults to 0.8.

    Returns:
        str: The resulting generated text
    """

    cache = MarkovDict(11 - int(randomness * 10))

    seed = randint(0, len(words) - (11 - int(randomness * 10)))
    while not (words[seed-1][-1].endswith(tuple(".?!")) and words[seed][0].isupper() and words[seed][0].isalpha() and words[seed-1][-2] != "."):
        seed -= 1

    wlist = [words[seed+i] for i in range(11 - int(randomness * 10))]

    gen_words = []
    i = 0

    while i < sentences:
        gen_words.append(wlist[0])
        if wlist[0].endswith(tuple(".?!")) and not wlist[0].endswith(".."):
            i += 1

        wlist = [*wlist[1:], choice(cache[tuple(wlist)])]

    return " ".join(gen_words)


if __name__ == "__main__":
    print(RandText(int(input("Sentences: ") or 5), float(input("Randomness (0.0-1.0): ") or 0.6)))