from AutoCorrect import AutoCorrect, WORDS, MAX
from inspect import getfullargspec
from collections import Counter
from msvcrt import kbhit, getch
from typing import Callable
from time import time

AC = AutoCorrect()

class CLI:
    def __blank(self, *args, **kwargs) -> None:
        pass

    def __init__(self) -> None:
        self.cmds: dict[str, list[str]] = {}


    def add_cmd(self, func: Callable) -> Callable:
        self.__setattr__(func.__name__, func)
        self.cmds[func.__name__] = getfullargspec(func).kwonlyargs + getfullargspec(func).args

        return func

    def __call__(self) -> None:
        # flush stdin
        while kbhit():
            getch()

        try:
            while True:
                lns: list[list[str]] = []

                while True: # lines
                    ln: list[str] = []

                    option: int = 0

                    argc = {c:list(a) for c, a in self.cmds.items()}

                    while True: # words
                        wd: str = ""

                        w = Counter(WORDS)

                        print(end="\x1b[?25l")

                        if ln == []:
                            w |= Counter({"$": (MAX + 5)})
                        elif ln == ["$"]:
                            w = Counter()
                        elif "".join(ln).lstrip() == "$ " and len([w.strip() for w in ln if w.strip()]) < 2:
                            w |= Counter(list(self.cmds.keys()) * (MAX + 5))
                        elif ln[0].strip() == "$" and [w.strip() for w in ln if w.strip() if w.strip() != "$"][0] in self.cmds.keys():
                            w |= Counter(argc.get([w.strip() for w in ln if w.strip()][1]) * (MAX + 5))

                        possibilities = AC.Candidates(wd, maxitems=5, options=w)

                        if ln != ["$"] and len(possibilities) != 0:
                            option = min(option, len(possibilities) - 1)

                        if possibilities:
                            for i, o in enumerate(possibilities + ([""] * max(0, 6 - len(possibilities)))):
                                print(f"\r\x1b[2K{' ' * len(''.join(ln))}" + ("\x1b[7m" * (option == i and len(possibilities) != 0)) + f"{o}\x1b[0m" + f"{' ' * (max([len(p) for p in possibilities]) - len(o) + 4)}\x1b[7m tab \x1b[0m" * (option == i and len(possibilities) != 0))
                        else:
                            print("\r\x1b[2K ...")

                            for i in range(5):
                                print("\r\x1b[2K")

                        for i in range(7):
                            print(end="\x1b[A\r")

                        while True: # chars
                            if l := [sn for sn, q in enumerate(ln + [wd]) if bool(q.strip()) and q.strip() != "$"]:
                                print(end="\x1b[2K\r" + "".join(["\x1b[33m" * (n == l[0] and n != 0) + w + "\x1b[0m" * (n == l[0]) for n, w in enumerate(ln + [wd])]))
                            else:
                                print(end="\x1b[2K\r" + "".join(ln + [wd]))


                            while not kbhit():
                                print(end=("_" if round(time() * 2) % 2 else " ") + "\x1b[D")

                            ch: str = getch().decode("utf-8")

                            if ch in ["\x00", "\xe0"]:
                                if kbhit():
                                    code = getch().decode("utf-8")

                                    if code == "H":
                                        option -= 1
                                        option %= len(possibilities)
                                    elif code == "P":
                                        option += 1
                                        option %= len(possibilities)
                                    elif code == "S":
                                        wd = ""
                                        ln = []

                            print(" \x1b[D")

                            if ch == "\t":
                                if len(ln) > 0:
                                    if ln[0].strip() == "$" and ln[-1].strip() != "$" and [w.strip() for w in ln if w.strip() if w.strip() != "$"]:
                                        if [w.strip() for w in ln if w.strip() if w.strip() != "$"][0] in self.cmds.keys():
                                            if possibilities[option] in argc[[w.strip() for w in ln if w.strip() if w.strip() != "$"][0]] and ln[-1].strip() != "-":
                                                ln.append("-")

                                wd = possibilities[option] + " " * possibilities[option].isalnum()
                                break
                            elif ch in ["\r", "\x1b"]:
                                print(end="\n" * (ch == "\r" or "".join(ln).strip() != ""))
                                break

                            if ch not in ["\b", "\x00", "\xe0"]:
                                wd += ch

                            if ch == "\b":
                                if len(wd) > 0: # delete last char of word
                                    wd = wd[:-1]
                                elif len(ln) > 0: # delete last char of previous word
                                    wd = ln[-1][:-1]
                                    ln = ln[:-1]
                                elif len(lns) > 0: # delete last char of previous line
                                    ln = lns[-1]
                                    wd = ln[-1]
                                    ln = ln[:-1]
                                    lns = lns[:-1]
                                    print(end=" \r\x1b[1A")
                                elif wd == "":
                                    pass
                                else: # try to delete when there is nothing to delete
                                    print(end="\a")

                            w = Counter(WORDS)

                            if ln == []:
                                w |= Counter({"$": (MAX + 5)})
                            elif ln == ["$"]:
                                w = Counter()
                            elif "".join(ln).lstrip() == "$ " and len([w.strip() for w in ln if w.strip()]) < 2:
                                w |= Counter(list(self.cmds.keys()) * (MAX + 5))
                            elif ln[0].strip() == "$" and [w.strip() for w in ln if w.strip() if w.strip() != "$"][0] in self.cmds.keys():
                                w |= Counter(argc.get([w.strip() for w in ln if w.strip()][1]) * (MAX + 5))

                            if ln != ["$"] and len(possibilities) != 0:
                                option = min(option, len(possibilities) - 1)

                            possibilities = AC.Candidates(wd, maxitems=5, options=w)

                            if (not ch.isalnum()) and ch not in  ["\b", "\x00", "\xe0"]:
                                break

                            if possibilities:
                                for i, o in enumerate(possibilities + ([""] * max(0, 6 - len(possibilities)))):
                                    print(f"\r\x1b[2K{' ' * len(''.join(ln))}" + ("\x1b[7m" * (option == i and len(possibilities) != 0)) + f"{o}\x1b[0m" + f"{' ' * (max([len(p) for p in possibilities]) - len(o) + 4)}\x1b[7m tab \x1b[0m" * (option == i and len(possibilities) != 0))
                            else:
                                print("\r\x1b[2K ...")

                                for i in range(5):
                                    print("\r\x1b[2K")

                            for i in range(7):
                                print(end="\x1b[A\r")

                        if len(ln) > 0:
                            if ln[0].strip() == "$" and ln[-1] == "-":
                                if [w.strip() for w in ln if w.strip()][1] in argc:
                                    argc[[w.strip() for w in ln if w.strip()][1]].remove(wd.strip())

                        if wd:
                            ln.append(wd)
                        
                        if ch in ["\r", "\x1b"]:
                            break
                        elif ch == "\t" and wd[-1] != " ":
                            ln.append(" ")

                    lns.append(ln)

                    if ch == "\x1b":
                        print(end="\r\x1b[2K\n" * 6 + "\x1b[A\r" * 7 + "\x1b[2K\r")
                        break

                for line in lns:
                    if not "".join(line).strip():
                        continue
                    elif line[0].strip() != "$":
                        continue
                    elif len(line) < 2:
                        continue
                    elif not [w.strip() for w in line[1:] if w.strip()]:
                        continue

                    cmd = [w.strip() for w in line[1:] if w.strip() and w.strip() != "$"][0]

                    cmdargs: list[str] = []
                    cmdkwargs: dict[str, str] = {}

                    if len([w for w in line if w.strip()]) > 2:
                        p = True

                        aa = [[], False]

                        sd = ["'", "\""]

                        for i, a in enumerate(line):
                            if p:
                                p = a.strip() != cmd
                                continue

                            if len(a.lstrip()) and not aa[1]:
                                if a.lstrip()[0] in sd:
                                    if len(a.lstrip()) > 1:
                                        aa[0].append(a.lstrip()[1:])
                                    else:
                                        aa[0].append("")

                                    aa[1] = True

                                    sd = [a.lstrip()[0]]

                                    continue
                            if len(a.rstrip()) and aa[1]:
                                if a.rstrip()[-1] in sd:
                                    if len(a.rstrip()) > 1:
                                        aa[0][-1] += a.lstrip()[:-1]

                                    aa[1] = False

                                    sd = ["'", "\""]

                                    continue
                            if aa[1]:
                                aa[0][-1] += a
                            else:
                                aa[0].append(a.strip())
                        
                        cmdargs = [a for a in aa[0] if a.strip()]

                    i = 0
                    while i < len(cmdargs):
                        if cmdargs[i] == "-":
                            cmdkwargs[cmdargs[i + 1]] = cmdargs[i + 2]

                            for _ in range(3):
                                cmdargs.pop(i)
                        else:
                            i += 1

                    try:
                        if cmd in [sf for sf in dir(self) if callable(self.__getattribute__(sf)) and sf[0] != "_"]:
                            f = self.__getattribute__(cmd)
                        else:
                            f = self.__blank

                        f(*cmdargs, **cmdkwargs)
                    except Exception as e:
                        print(e) # debugging
                
                print()
        
        except KeyboardInterrupt:
            for i in range(6):
                print("\r\x1b[2K")

            for i in range(5):
                print(end="\x1b[A\r")

            return print(end="\x1b[?25h")
        except EOFError:
            for i in range(6):
                print("\r\x1b[2K")

            for i in range(5):
                print(end="\x1b[A\r")

            return print(end="\x1b[?25h")
        except Exception as e:
            for i in range(6):
                print("\r\x1b[2K")

            for i in range(5):
                print(end="\x1b[A\r")

            print(end="\x1b[?25h")

            raise e
