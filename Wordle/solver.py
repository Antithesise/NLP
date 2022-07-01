from typing import Counter


with open("words.txt") as f:
    words = f.read().split()

def match(k: str, c: list[str], r: str, word: str) -> bool:
    if any([l != lw and l.strip("0") for l, lw in zip(k.zfill(5), word)]):
        return False

    if any([lw in l for l, lw in zip(c, word)]):
        return False

    if any([l not in word for l in "".join(c) if l.strip("0")]):
        return False

    if any([l in word for l in r]):
        return False
    
    return True


# words to start off a round (in order)
# OTHER, NAILS, DUCHY

while True:
    letters = [k for k, v in Counter("".join(words)).most_common()]

    print(", ".join(sorted(words, key=lambda w: sum([letters.index(l) for l in w] + [(len(list(w)) - len(set(w))) * 26]), reverse=True)))
    print(" ".join(letters))

    x = input().split(";")
    k = x[0]
    c = x[1].split(",")
    r = x[-1]

    words = [w for w in words if match(k, c, r, w)]
