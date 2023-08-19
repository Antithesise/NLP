from AutoCorrect import AutoCorrect, WagnerFischer, WORDS, MAX
from inspect import getfullargspec
from collections import Counter
from msvcrt import kbhit, getch
from typing import Callable
from time import time


AC = AutoCorrect()
WF = WagnerFischer()


class CLI:
    def __init__(self) -> None:
        self.cmds: dict[str, list[str]] = {}
        self.setupfuncs: dict[Callable, int] = {}

    def add_cmd(self, func: Callable) -> Callable:
        if func.__name__ in dir(self):
            raise NameError(f"Function {func} is inbuilt or has already been added.")

        self.__setattr__(func.__name__, func)
        self.cmds[func.__name__] = getfullargspec(func).kwonlyargs + getfullargspec(func).args

        return func

    def setup(self, lines: int) -> Callable:
        def wrapper(func: Callable) -> Callable:
            self.setupfuncs[func] = lines

            return func

        return wrapper

    def __setup(self) -> int:
        for f in self.setupfuncs.keys():
            f()

        return sum(self.setupfuncs.values())

    def __call__(self, flags: dict={}) -> None:
        """
        Register commands with `add_cmd`.

        Execute commands by starting the line with '$',\nthen the name of the command and any arguments,\nseperated by spaces (keyword argument supplied\nlike so: `-name Anithesise`).\n
        Use `tab` to complete autofill and the `up` and\n`down` arrow keys to navigate options. Execute\na paragraph by pressing `esc`\nPress `delete` to cancel the entire line
        """

        # flush stdin
        while kbhit():
            getch()

        maxoptions = flags.get("maxoptions", 5)
        method: AutoCorrect | WagnerFischer = {
            "w-f": WF, "default": AC
        }[flags.get("method", "default")]

        try:
            while True:
                lns: list[list[str]] = [] # lines

                while True: # lines
                    ln: list[str] = [] # line

                    option: int = 0 # index for autocomplete options

                    # arguments to display
                    argc = {c:list(a) for c, a in self.cmds.items()}

                    while True: # words
                        wd: str = "" # word

                        setuplns = self.__setup()

                        w = Counter(WORDS) # base autocomplete options

                        print(end="\x1b[?25l") # hide cursor

                        if ln == []:
                            w |= Counter({"$": (MAX + 5)}) # empty line
                        elif ln == ["$"]:
                            w = Counter() # no options when '$' is wating to be followed by a space
                        elif "".join(ln).lstrip() == "$ " and len([w.strip() for w in ln if w.strip()]) < 2:
                            w |= Counter(list(self.cmds.keys()) * (MAX + 5)) # '$', but no command
                        elif ln[0].strip() == "$" and [w.strip() for w in ln if w.strip() if w.strip() != "$"][0] in self.cmds.keys():
                            w |= Counter(argc.get([w.strip() for w in ln if w.strip()][1]) * (MAX + 5)) # command args

                        # set top maxoptions autocomplete options
                        possibilities = method.Candidates(wd, maxitems=maxoptions, options=w)

                        if ln != ["$"] and len(possibilities) != 0:
                            # make sure option is within range
                            option = min(option, len(possibilities) - 1)

                        # print possibilities
                        if possibilities:
                            for i, o in enumerate(possibilities + ([""] * max(0, maxoptions + 1 - len(possibilities)))):
                                print(f"\r\x1b[2K{' ' * len(''.join(ln))}" + ("\x1b[7m" * (option == i and len(possibilities) != 0)) + f"{o}\x1b[0m" + f"{' ' * (max([len(p) for p in possibilities]) - len(o) + 4)}\x1b[7m tab \x1b[0m" * (option == i and len(possibilities) != 0))
                        else:
                            print(end="\r\x1b[2K ...\n" + "\r\x1b[2K\n" * 5)

                        print(end="\x1b[A\r" * 7)

                        while True: # chars
                            if l := [sn for sn, q in enumerate(ln + [wd]) if bool(q.strip()) and q.strip() != "$"]:
                                # print line so far if it is a cmd
                                print(end="\x1b[2K\r" + "".join(["\x1b[33m" * (n == l[0] and n != 0) + w + "\x1b[0m" * (n == l[0]) for n, w in enumerate(ln + [wd])]))
                            else:
                                # print line so far if it is not a cmd
                                print(end="\x1b[2K\r" + "".join(ln + [wd]))

                            while not kbhit():
                                # blinking underscore
                                print(end=("_" if round(time() * 2) % 2 else " ") + "\x1b[D")

                            print(" \x1b[D") # clear blinking underscore

                            ch: str = getch().decode("utf-8") # set ch to input

                            if ch in ["\x00", "\xe0"]: # special keys
                                if kbhit():
                                    code = getch().decode("utf-8")

                                    if code == "H": # up arrow
                                        option -= 1
                                        option %= len(possibilities)
                                    elif code == "P": # down arrow
                                        option += 1
                                        option %= len(possibilities)
                                    elif code == "S": # 'del' (not backspace)
                                        wd = ""
                                        ln = []

                            if ch == "\t": # tab
                                if len(ln) > 0:
                                    if ln[0].strip() == "$" and [w.strip() for w in ln if w.strip() if w.strip() != "$"]:
                                        if [w.strip() for w in ln if w.strip() if w.strip() != "$"][0] in self.cmds.keys():
                                            if possibilities[option] in argc[[w.strip() for w in ln if w.strip() if w.strip() != "$"][0]] and ln[-1].strip() != "-":
                                                # if option is argument for the cmd then add the '-'
                                                ln.append("-")

                                wd = possibilities[option] + " " * possibilities[option].isalnum() # set word to the option
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
                                else: # try to delete when there is nothing to delete
                                    print(end="\a")

                            print(end=f"\x1b[{setuplns + 1}A")

                            setuplns = self.__setup()

                            print(end="\n"*bool(setuplns))

                            w = Counter(WORDS) # base autocomplete options

                            if ln == []:
                                # empty line
                                w |= Counter({"$": (MAX + 5)})
                            elif ln == ["$"]:
                                # no options when '$' is wating to be followed by a space
                                w = Counter()
                            elif "".join(ln).lstrip() == "$ " and len([w.strip() for w in ln if w.strip()]) < 2:
                                # '$', but no command
                                w |= Counter(list(self.cmds.keys()) * (MAX + 5))
                            elif ln[0].strip() == "$" and [w.strip() for w in ln if w.strip() if w.strip() != "$"][0] in self.cmds.keys():
                                # command args
                                w |= Counter(argc.get([w.strip() for w in ln if w.strip()][1]) * (MAX + 5))

                            if ln != ["$"] and len(possibilities) != 0:
                                # make sure option is within range
                                option = min(option, len(possibilities) - 1)

                            # set top maxoptions autocomplete options
                            possibilities = method.Candidates(wd, maxitems=maxoptions, options=w)

                            if (not ch.isalnum()) and ch not in  ["\b", "\x00", "\xe0"]:
                                break

                            # print possibilities
                            if possibilities:
                                for i, o in enumerate(possibilities + ([""] * max(0, maxoptions + 1 - len(possibilities)))):
                                    print(f"\r\x1b[2K{' ' * len(''.join(ln))}" + ("\x1b[7m" * (option == i and len(possibilities) != 0)) + f"{o}\x1b[0m" + f"{' ' * (max([len(p) for p in possibilities]) - len(o) + 4)}\x1b[7m tab \x1b[0m" * (option == i and len(possibilities) != 0))
                            else:
                                print(end="\r\x1b[2K ...\n" + "\r\x1b[2K\n" * 5)

                            print(end="\x1b[A\r" * 7)

                        if len(ln) > 0:
                            if ln[0].strip() == "$" and ln[-1] == "-":
                                if [w.strip() for w in ln if w.strip()][1] in argc:
                                    argc[[w.strip() for w in ln if w.strip()][1]].remove(wd.strip())

                        if wd:
                            ln.append(wd) # add word to line

                        if ch in ["\r", "\x1b"]: # enter or return
                            break
                        elif ch == "\t" and wd[-1] != " ":
                            # autocomplete add trailing space
                            ln.append(" ")

                    lns.append(ln) # add line to lines

                    if ch == "\x1b": # escape
                        print(end="\r\x1b[2K\n" * (maxoptions + 1) + "\x1b[A\r" * (maxoptions + 2) + "\x1b[2K\r")
                        break

                for line in lns:
                    if not "".join(line).strip(): # if line is blank
                        continue
                    elif line[0].strip() != "$": # if line is just the '$'
                        continue
                    elif len(line) < 2: # if line doesn't have a cmd
                        continue
                    elif not [w.strip() for w in line[1:] if w.strip()]: # if line is just whitespace
                        continue

                    # get name of cmd
                    cmd = [w.strip() for w in line[1:] if w.strip() and w.strip() != "$"][0]

                    if cmd not in self.cmds:
                        continue

                    cmdargs: list[str] = []
                    cmdkwargs: dict[str, str] = {}

                    if len([w for w in line if w.strip()]) > 2: # arguments?
                        p = True # pass

                        aa = [[], False] # argument accumalator for string parsing

                        sd = ["'", "\""] # declare strings

                        for i, a in enumerate(line): # compile arguments
                            if p:
                                p = a.strip() != cmd
                                continue

                            # parse strings
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

                        cmdargs = [a for a in aa[0] if a.strip()] # clean arguments

                    i = 0
                    while i < len(cmdargs): # compile keyword arguments
                        if cmdargs[i] == "-":
                            cmdkwargs[cmdargs[i + 1]] = cmdargs[i + 2]

                            for _ in range(3):
                                cmdargs.pop(i)
                        else:
                            i += 1

                    try:
                        self.__getattribute__(cmd)(*cmdargs, **cmdkwargs) # call func
                    except Exception as e:
                        print(e) # debugging

                print()

        except KeyboardInterrupt:
            # clear maxoptions + 1 lines below then move cursor up maxoptions lines then show cursor
            print(end="\r\x1b[2K\n" * (maxoptions + 1) + "\x1b[A\r" * maxoptions + "\x1b[?25h")

            return
        except EOFError:
            # clear maxoptions + 1 lines below then move cursor up maxoptions lines then show cursor
            print(end="\r\x1b[2K\n" * (maxoptions + 1) + "\x1b[A\r" * maxoptions + "\x1b[?25h")

            return
        except Exception as e:
            # clear maxoptions + 1 lines below then move cursor up maxoptions lines then show cursor
            print(end="\r\x1b[2K\n" * (maxoptions + 1) + "\x1b[A\r" * maxoptions + "\x1b[?25h")

            raise e
