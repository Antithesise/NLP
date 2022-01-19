from typing import Counter
from random import choice
from msvcrt import getch
from time import sleep
from os import system


with open("words.txt") as f:
    words = f.read().split()

with open("valid.txt") as f:
    valid = f.read().split()

absurds = sorted(words, key=lambda w: sum([Counter("".join(words))[l] for l in w] + [(len(list(w)) - len(set(w))) * 26]))

green = "\x1b[48;2;83;141;78m"
yellow = "\x1b[48;2;181;159;59m"
grey = "\x1b[48;2;58;58;60m"

games = 0
won = 0
streak = 0
mstreak = 0
dist = [0, 0, 0, 0, 0, 0]


def match(k, c, r, word) -> bool:
    if any([l != lw and l for l, lw in zip(k, word)]):
        return False

    if any([lw in l for l, lw in zip(c, word)]):
        return False

    if any([l not in word for l in "".join(c)]):
        return False

    if any([l in word for l in r]):
        return False
    
    return True


while True:
    system("cls")

    games += 1
    word = choice(words)
    pos = [[""] * 5, [""] * 5, []] # keep, change, remove
    n = 0

    system("cls")

    while True:
        guess = ""

        while True:
            msg = ""
    
            ch = getch().decode("utf-8").lower()

            if not ch:
                continue
            elif ch == "\r" and len(guess) == 5:
                if guess in valid + words:
                    break
                else:
                    msg = "   (Not on wordlist)\x1b[20D"
            elif ch == "\x08":
                guess = guess[:-1]
            elif ch in ["\x00", "\xe0"]:
                getch()
                pass
            elif len(guess) == 5:
                pass
            else:
                guess += ch
            
            print(end=f"\x1b[2K\r{''.join([f' {l} ' for l in guess])}{msg}", flush=True)

        print(end="\x1b[?25l\r")
        for i, l in enumerate(guess):
            print(end=f"{(grey if l not in word else (green if l == word[i] else yellow))} {l} \x1b[0m", flush=True)
            sleep(0.25)

        print("\x1b[?25h")

        n += 1

        if guess == word:
            print(f"You win!")
            won += 1
            streak += 1
            mstreak = max(streak, mstreak)
            dist[n - 1] += 1

            print("STATISTICS")
            print(f"Played {games} Win % {round(100 * won / games)} Current Streak {streak} Max Streak {mstreak}")
            print("GUESS DISTRIBUTION")
            for v, a in enumerate(dist):
                print(f"{v + 1} {grey}{'   ' * a} {a} \x1b[0m")

            print("[Press ENTER to Continue]")
            getch()

            break
        elif n == 6:
            print(f"You lose. The answer was {word}")
            streak = 0

            print("STATISTICS")
            print(f"Played {games} Win % {round(100 * won / games)} Current Streak {streak} Max Streak {mstreak}")
            print("GUESS DISTRIBUTION")
            for v, a in enumerate(dist):
                print(f"{v + 1} {grey}{' ' * a} {a} \x1b[0m")

            print("[Press ENTER to Continue]")
            getch()

            break

        for i, l in enumerate(guess):
            if l not in word:
                pos[-1] += l
            elif l == word[i]:
                pos[0][i] == l
            else:
                pos[1][i] += l

        absurds = [w for w in absurds if match(*pos, w)]

        word = absurds[0]