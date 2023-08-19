from collections import UserList

from typing import Literal, Type


class WORDCLASS(str):
    wordclass: str = ""
    shortwc: str = ""

    def __repr__(self) -> str:
        return (f"<{self.wordclass} {str(self)}>" if self.wordclass and self.wordclass != "punc" else str(self))

class NOUN(WORDCLASS):
    wordclass = "n"
    shortwc = "n"

class ADJ(WORDCLASS):
    wordclass = "adj"
    shortwc = "j"

class ADV(WORDCLASS):
    wordclass = "adv"
    shortwc = "z"

class VERB(WORDCLASS):
    wordclass = "v"
    shortwc = "v"

class AUX(WORDCLASS):
    wordclass = "aux"
    shortwc = "x"

class DET(WORDCLASS):
    wordclass = "d"
    shortwc = "d"

class PRON(WORDCLASS):
    wordclass = "pn"
    shortwc = "y"

class PREP(WORDCLASS):
    wordclass = "prep"
    shortwc = "p"

class INT(WORDCLASS):
    wordclass = "int"
    shortwc = "i"

class CONJ(WORDCLASS):
    wordclass = "conj"
    shortwc = "c"

class PUNC(WORDCLASS):
    wordclass = "punc"
    shortwc = "."

class QUOTE(WORDCLASS):
    wordclass = "q"
    shortwc = "q"

class FLAT_SENTENCE(UserList[Type[WORDCLASS]]):
    sentenceclass: Literal["S", "Q", "F"] | None = None

    def __repr__(self) -> str:
        return " ".join([repr(w) for w in self.data[:]])

class NODE(UserList[Type["NODE"] | Type[WORDCLASS]]):
    wordclass: str = ""
    shortwc: str = ""

    def __repr__(self) -> str:
        return f"<{self.wordclass} {''.join([repr(w) for w in self.data[:]])}>"

class SENTENCE(NODE):
    shortwc = "s"

class DECLERATIVE(SENTENCE):
    wordclass = "decl"

class INTERROGATIVE(SENTENCE):
    wordclass = "qstn"

class FRAGMENT(SENTENCE):
    wordclass = "frag"

class DET_PHRASE(NODE):
    wordclass = "detp"
    shortwc = "t"

class ADJ_PHRASE(NODE):
    wordclass = "adjp"
    shortwc = "g"

class NOUN_PHRASE(NODE):
    wordclass = "nounp"
    shortwc = "l"

class VERB_PHRASE(NODE):
    wordclass = "verbp"
    shortwc = "h"

class COMP_PHRASE(NODE):
    wordclass = "compp"
    shortwc = "k"