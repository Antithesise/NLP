from TextTools import wrd, suffixes, gridify
from collections import Counter
from MarkovText import RandText
from random import shuffle
from re import search
from os import system

with open("big.txt") as f:
    big = f.read().strip().replace("    ", "").replace("  ", " ")


text = input("Paste/type cipher here (leave blank for empty): ")
if not text.strip(): # create random substitution cipher
    new = [chr(l) for l in range(97, 123)]
    shuffle(new)
    new = dict(zip([chr(l) for l in range(97, 123)], new))

    text = "".join([new.get(l.lower(), l) if l.islower() else new.get(l.lower(), l).upper() for l in list(RandText())])

text = text.strip().replace("    ", "").replace("  ", " ")
deciphered = text
grid = []

letters = Counter([i.lower() for i in text if i.isalpha()])
common = [k for k, v in letters.most_common()]

cs = suffixes([w.lower() for w in wrd(text) if w.isalpha()], maxl=3)
if cs:
    es = suffixes([w.lower() for w in wrd(big) if w.isalpha()], len(min(cs, key=len)), len(max(cs, key=len)), no=len(cs))

for l in range(97, 123):
    if chr(l) not in letters:
        letters[chr(l)] = 0

caeser = False
reverse = False
shift = 0

mode = input("Substituition [S], Transposition [T] or Both [B]? ").strip()[0].lower()
start = True

if mode in "bs":
    sub = {chr(l): "?" for l in range(97, 123)}
    old = sub
else:
    sub = {chr(l): chr(l) for l in range(97, 123)}
    old = sub


while mode == "b" or start:
    while mode in "bs":
        system("cls")

        if not (caeser or reverse):
            old = sub
        else:
            sub = {chr(l + 97): chr(122 - ((l + shift) % 26) if reverse else ((l + shift) % 26) + 97) for l in range(26)}

        deciphered = "".join([(sub.get(l.lower(), l) if l.islower() else sub.get(l.lower(), l).upper()).replace("?", "_" if l != "?" else "?") for l in text])

        print("Common letters (English):\n" + "e t a o n i s r h d l c u m f w p g y b v k x j q z", "\n")
        print("Common letters (Cipher):\n" + " ".join(common), "\n")
        print("Common letters (Deciphered):\n" + " ".join([sub.get(l, l) for l in common]), "\n")

        if cs:
            print("Common suffixes (English):\n" + " ".join(es), "\n")
            print("Common suffixes (Cipher):\n" + " ".join(cs), "\n")

        print(f"Cipher{' (' * (caeser or reverse)}{'caeser' * caeser}{' + ' * caeser * reverse}{'Reverse' * reverse}{' mode)' * (caeser or reverse)}:")
        print(" ".join(sub.keys()))
        print("↓ " * len(sub))
        print(" ".join(sub.values()), "\n")

        print("Ciphered:\n" + text, "\n")
        print("Deciphered:\n" + deciphered, "\n")

        if reverse and not caeser:
            print("Please deactive Reverse mode or activate caeser Cipher mode continue")
        i = input("> ").lower().strip()

        if not i: # exit
            exit()
        elif i == ":": # enter/exit caeser cipher mode
            caeser = not caeser

            if not caeser:
                sub = old
        elif i == "!": # enter/exit reverse mode
            reverse = not reverse

            if not reverse:
                sub = old
            else:
                sub = {chr(l): chr(122 - l) for l in range(97, 123)}
        elif i == "#" and mode == "b": # enter transposition cipher mode (exit substituition cipher loop)
            break
        elif i == "?": # search w/ regex
            system("cls")

            print("Deciphered:\n" + deciphered, "\n")

            while (x := input("r/")):
                try:
                    r = search(x, deciphered)
                except:
                    r = search(r"ERROR", "ERROR")

                system("cls")

                print("Deciphered:\n" + deciphered, "\n")
                print("Results:\n" + ", ".join(f"{m} ({m.start})" for m in r), "\n")
        elif caeser:
            shift += (i != "-") * 2 - 1
        elif reverse:
            continue
        elif i == "-": # reset all
            sub = {chr(l): "?" for l in range(97, 123)}
        elif " " not in i: # reset
            for c in i:
                sub[c] = "?"
        else: # substitute
            k, v = i.split(" ")[:2]

            for c, d in zip(k, v):
                if c in sub:
                    sub[c] = d

    deciphered = "".join([(sub.get(l.lower(), l) if l.islower() else sub.get(l.lower(), l).upper()).replace("?", "_" if l != "?" else "?") for l in text])

    while mode in "bt":
        system("cls")

        if mode == "b":
            if not (caeser or reverse):
                old = sub
            else:
                sub = {chr(l + 97): chr(122 - ((l + shift) % 26) if reverse else ((l + shift) % 26) + 97) for l in range(26)}

        print(f"Cipher{' (' * (caeser or reverse)}{'caeser' * caeser}{' + ' * caeser * reverse}{'Reverse' * reverse}{' mode)' * (caeser or reverse)}:")
        print(" ".join(sub.keys()))
        print("↓ " * len(sub))
        print(" ".join(sub.values()), "\n")

        print("Ciphered:\n" + "".join(deciphered.split()), "\n")
        if grid:
            print("Deciphered (grid):\n" + "\n".join(["  ".join(row) for row in grid]), "\n")
            print("Deciphered (text):\n" + "".join([
                "".join([
                    grid[r][c] for r in range(len(grid))
                ]) for c in range(len(grid[0]))
            ]), "\n")

        i = input("> ").lower().strip()

        if not i: # exit
            exit()
        elif i == "#" and mode == "b": # enter substituition cipher mode (exit transposition cipher loop)
            break
        elif i == "?":
            system("cls")

            d = "".join(
                "".join(
                    grid[r][c] for r in range(len(grid))
                ) for c in range(len(grid[0]))
            )

            print("Deciphered:\n" + d, "\n")

            while (x := input("r/")):
                try:
                    r = search(x, deciphered)
                except:
                    r = search(r"ERROR", "ERROR")

                system("cls")

                print("Deciphered:\n" + d, "\n")
                print("Result:\n" + f"{r.group()} ({r.start()})", "\n")
        else: # arrange grid
            w = int(i)

            grid = gridify("".join(deciphered.split()), w or 1, "_")

    start = False