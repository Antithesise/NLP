from os import get_terminal_size
from re import Match, search, sub

from lexer import Lexer
from enums import *

from typing import Type


class Syntax:
    def __init__(self, debug: bool=False) -> None:
        self.debug = debug
        self.start = 0
        self.end = 0

    def group(self, pattern: str, repl: Type[NODE]) -> None:
        def replfunc(m: Match):
            self.start = m.start(0)
            self.end = self.start + len(m.group(0))

            return repl.shortwc

        while search(pattern, self.rep):
            self.rep = sub(pattern, replfunc, self.rep, 1)

            new = repl(list(self.out[self.start:self.end]))

            for i in range(self.end - self.start - 1):
                self.out.pop(self.start)

            self.out[self.start] = new

    def __call__(self, sentence: FLAT_SENTENCE) -> Type[SENTENCE]:
        self.sentence = sentence
        self.out = {"S": DECLERATIVE, "Q": INTERROGATIVE, "F": FRAGMENT}[str(self.sentence.sentenceclass)](self.sentence)
        self.rep = "".join(w.shortwc for w in self.sentence)

        # Rewrite rules
        # {x} = repeated 1+ times
        # [x] = repeated 0+ times
        # <x> = single
        # @X = constraint

        # {DET} => <DET PHRASE>
        self.group(r"d+", DET_PHRASE)

        # {ADJ} => <ADJ PHRASE>
        self.group(r"j+", ADJ_PHRASE)

        # [DET PHRASE] [ADJ_PHRASE] {NOUN or PRONOUN} => <NOUN PHRASE>
        self.group(r"t*g*[ny]+", NOUN_PHRASE)

        # {<NOUN PHRASE> <PREP or CONJ>} [NOUN PHRASE!] => <NOUN PHRASE>
        self.group(r"(?:l[pc])+l?", NOUN_PHRASE)

        # {VERB or AUX VERB or ADVERB or PREP} => <VERB PHRASE>
        self.group(r"[vxzp]+", VERB_PHRASE)

        # @!START {<VERB PHRASE> [NOUN PHRASE or ADJ PHRASE]} => <COMP PHRASE>
        self.group(r"(?!\A)(?:h[lg]*)+", COMP_PHRASE)

        if self.debug:
            print(self.rep)

        return self.out

if __name__ == "__main__":
    lexer = Lexer(debug=False)
    syntax = Syntax(debug=True)

    with open("tests.txt") as f:
        for l in (tests := f.read().strip().split("\n")):
            phrase, correct = l.split("|")

            try:
                print("\n > ", phrase.strip())
                print(end="\n" * syntax.debug)

                print("\n   ", syntax(lexer(phrase)), f"({lexer.out.sentenceclass})")
            except Exception as e:
                print("\n    \x1b[31mError:", e, end="\x1b[0m\n")
                print("    Last state recorded:", syntax.out)

    print(f"\nTesting complete.\n\n{'*' * get_terminal_size().columns}\n\nEntering Interactive Mode. Press Ctrl+C to exit...")

    while True:
        try:
            print("\n   \x1b[33m", syntax(lexer(input("\n >  "))), f"({lexer.out.sentenceclass})\x1b[0m")

        except KeyboardInterrupt:
            print("\x1b[0m\x1b[2K\rExiting...\n")

            break

        except EOFError:
            print("\x1b[0m\x1b[2K\rExiting...\n")

            break

        except Exception as e:
            print("\n    \x1b[31mError:", e, end="\x1b[0m\n")