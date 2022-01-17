from typing import Counter


with open("words.txt") as f:
    words = f.read().split()

def match(pattern, word) -> bool:
    pattern = pattern.split(" ")
    wrd = pattern[0]

    if len(pattern) > 1:
        inc = pattern[1]
    else:
        inc = False

    if len(pattern) > 2:
        exc = pattern[2]
    else:
        exc = False

    for l, lw in zip(wrd, word):
        if l != lw and l != "_":
            return False
    
    if inc:
        for l in inc:
            if l not in word:
                return False
    
    if exc:
        for l in exc:
            if l in word:
                return False
    
    return True


# words to start off a round (in order)
# OTHER, NAILS, DUCHY

while True:
    letters = [k for k, v in Counter("".join(words)).most_common()]

    print(", ".join(sorted(words, key=lambda w: sum([letters.index(l) for l in w] + [(len(list(w)) - len(set(w))) * 26]), reverse=True)))
    print(" ".join(letters))


    pattern = input()

    words = [w for w in words if match(pattern, w)]
