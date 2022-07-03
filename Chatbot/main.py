from re import split


class SENTENCE(list):
    def __repr__(self) -> str:
        return "SENTENCE( %s )" % " ".join([repr(w) for w in self.copy()])
class NOUN(str):
    def __repr__(self) -> str:
        return super().__repr__().removeprefix("'").removeprefix("\"").removesuffix("'").removesuffix("\"") + " (n)"
class ADJ(str):
    def __repr__(self) -> str:
        return super().__repr__().removeprefix("'").removeprefix("\"").removesuffix("'").removesuffix("\"") + " (adj)"
class ADV(str):
    def __repr__(self) -> str:
        return super().__repr__().removeprefix("'").removeprefix("\"").removesuffix("'").removesuffix("\"") + " (adv)"
class VERB(str):
    def __repr__(self) -> str:
        return super().__repr__().removeprefix("'").removeprefix("\"").removesuffix("'").removesuffix("\"") + " (v)"
class AUX(str):
    def __repr__(self) -> str:
        return super().__repr__().removeprefix("'").removeprefix("\"").removesuffix("'").removesuffix("\"") + " (aux)"
class DET(str):
    def __repr__(self) -> str:
        return super().__repr__().removeprefix("'").removeprefix("\"").removesuffix("'").removesuffix("\"") + " (d)"
class PRON(str):
    def __repr__(self) -> str:
        return super().__repr__().removeprefix("'").removeprefix("\"").removesuffix("'").removesuffix("\"") + " (pn)"
class PREP(str):
    def __repr__(self) -> str:
        return super().__repr__().removeprefix("'").removeprefix("\"").removesuffix("'").removesuffix("\"") + " (pre)"
class INT(str):
    def __repr__(self) -> str:
        return super().__repr__().removeprefix("'").removeprefix("\"").removesuffix("'").removesuffix("\"") + " (int)"
class CONJ(str):
    def __repr__(self) -> str:
        return super().__repr__().removeprefix("'").removeprefix("\"").removesuffix("'").removesuffix("\"") + " (cj)"
class PUNC(str):
    def __repr__(self) -> str:
        return super().__repr__().removeprefix("'").removeprefix("\"").removesuffix("'").removesuffix("\"")

class Parse:
    determiners = [
        "the",
        "a",
        "an",
        "this",
        "that",
        "these",
        "those",
        "my",
        "your",
        "his",
        "her",
        "its",
        "our",
        "us",
        "we",
        "them",
        "their",
        "other",
        "another",
        "such",
        "what",
        "whatever",
        "which",
        "whichever",
        "rather",
        "quite",
        "last",
        "next",
        "certain",
    ]
    quantifiers_distributives = [
        "few",
        "fewer",
        "fewest",
        "little",
        "less",
        "least",
        "much",
        "many",
        "more",
        "most",
        "lot",
        "lots",
        "most",
        "some",
        "any",
        "enough",
        "all",
        "both",
        "half",
        "either",
        "neither",
        "each",
        "every",
        "several",
        "few",
    ]
    adjective_suffixes = [
        "able",
        "ible",
        "al",
        "ful",
        "ian",
        "ive",
        "less",
        "like",
        "ly",
        "ous",
        "free",
    ]
    verb_suffixes = [
        "ed",
        "en",
        "er",
        "es",
        "ing",
        "ize",
        "ise",
    ]
    prepositions = [
        "a",
        "aboard",
        "about",
        "above",
        "abreast",
        "abroad",
        "absent",
        "across",
        "adrift",
        "aft",
        "after",
        "against",
        "ahead",
        "aloft",
        "along",
        "alongside",
        "although",
        "amid",
        "amidst",
        "among",
        "amongst",
        "anti",
        "apart",
        "apropos",
        "around",
        "as",
        "ashore",
        "aside",
        "aslant",
        "astride",
        "at",
        "atop",
        "away",
        "back",
        "bar",
        "barring",
        "because",
        "before",
        "beforehand",
        "behind",
        "below",
        "beneath",
        "beside",
        "besides",
        "between",
        "beyond",
        "but",
        "by",
        "circa",
        "come",
        "concerning",
        "considering",
        "contra",
        "counting",
        "despite",
        "down",
        "downhill",
        "downstage",
        "downstairs",
        "downstream",
        "downwind",
        "during",
        "east",
        "effective",
        "ere",
        "except",
        "excepting",
        "excluding",
        "failing",
        "following",
        "for",
        "forth",
        "from",
        "given",
        "granted",
        "hence",
        "henceforth",
        "here",
        "hereby",
        "herein",
        "hereof",
        "hereto",
        "herewith",
        "home",
        "if",
        "in",
        "including",
        "indoors",
        "inside",
        "into",
        "less",
        "lest",
        "like",
        "mid",
        "midst",
        "minus",
        "modulo",
        "near",
        "neath",
        "next",
        "north",
        "northeast",
        "northwest",
        "notwithstanding",
        "now",
        "of",
        "off",
        "offshore",
        "on",
        "once",
        "onto",
        "opposite",
        "out",
        "outdoors",
        "outside",
        "over",
        "overboard",
        "overhead",
        "overland",
        "overseas",
        "pace",
        "past",
        "pending",
        "per",
        "plus",
        "post",
        "pre",
        "pro",
        "provided",
        "providing",
        "qua",
        "re",
        "regarding",
        "respecting",
        "round",
        "sans",
        "save",
        "saving",
        "seeing",
        "short",
        "since",
        "so",
        "south",
        "southeast",
        "southwest",
        "sub",
        "supposing",
        "than",
        "then",
        "thence",
        "thenceforth",
        "there",
        "thereby",
        "therein",
        "thereof",
        "thereto",
        "therewith",
        "though",
        "through",
        "throughout",
        "till",
        "times",
        "to",
        "together",
        "toward",
        "towards",
        "under",
        "underfoot",
        "underground",
        "underneath",
        "unless",
        "unlike",
        "until",
        "up",
        "uphill",
        "upon",
        "upstage",
        "upstairs",
        "upstream",
        "upwind",
        "versus",
        "via",
        "vice",
        "wanting",
        "west",
        "when",
        "whence",
        "whenever",
        "where",
        "whereas",
        "whereby",
        "wherein",
        "whereto",
        "wherever",
        "wherewith",
        "while",
        "whilst",
        "with",
        "within",
        "without"]
    pronouns = [
        "all",
        "another",
        "any",
        "anybody",
        "anyone",
        "anything",
        "as",
        "aught",
        "both",
        "each",
        "eachother",
        "either",
        "enough",
        "everybody",
        "everyone",
        "everything",
        "few",
        "he",
        "her",
        "hers",
        "herself",
        "him",
        "himself",
        "his",
        "i",
        "it",
        "its",
        "itself",
        "many",
        "me",
        "mine",
        "most",
        "my",
        "myself",
        "naught",
        "neither",
        "noone",
        "nobody",
        "none",
        "nothing",
        "nought",
        "one",
        "oneanother",
        "other",
        "others",
        "ought",
        "our",
        "ours",
        "ourself",
        "ourselves",
        "several",
        "she",
        "some",
        "somebody",
        "someone",
        "something",
        "somewhat",
        "such",
        "suchlike",
        "that",
        "thee",
        "their",
        "theirs",
        "theirself",
        "theirselves",
        "them",
        "themself",
        "themselves",
        "there",
        "these",
        "they",
        "thine",
        "this",
        "those",
        "thou",
        "thy",
        "thyself",
        "us",
        "we",
        "what",
        "whatever",
        "whatnot",
        "whatsoever",
        "whence",
        "where",
        "whereby",
        "wherefrom",
        "wherein",
        "whereinto",
        "whereof",
        "whereon",
        "wherever",
        "wheresoever",
        "whereto",
        "whereunto",
        "wherewith",
        "wherewithal",
        "whether",
        "which",
        "whichever",
        "whichsoever",
        "who",
        "whoever",
        "whom",
        "whomever",
        "whomso",
        "whomsoever",
        "whose",
        "whosever",
        "whosesoever",
        "whoso",
        "whosoever",
        "ye",
        "yon",
        "yonder",
        "you",
        "your",
        "yours",
        "yourself",
        "yourselves"
    ]
    punctuation = ",.;:?!"

    def __init__(self, sentence: str) -> None:
        self.sentence = [w for w in split(r" |(?=[,.;:?!])", sentence.lower().replace("each other", "eachother").replace("no one", "noone").replace("one another", "oneanother")) if w]
        self.out = SENTENCE()
    
    def add(self, WClass: NOUN | ADJ | ADV | VERB | AUX | DET | PRON | PREP | INT | CONJ | PUNC) -> None:
        if WClass == NOUN and self.sentence[0] in self.pronouns:
            WClass = PRON

        self.out.append(WClass(self.sentence.pop(0)))

    def __call__(self) -> list:
        while any(self.sentence[0].endswith(s) for s in self.adjective_suffixes) or self.sentence[0] in self.prepositions or self.sentence[0].endswith("ward") or self.sentence[0].endswith("wards"):
            if self.sentence[1] not in self.punctuation:
                while not self.sentence[0] in self.punctuation:
                    if self.sentence[0] in self.determiners or self.sentence[0] in self.quantifiers_distributives or self.sentence[1] in self.quantifiers_distributives:
                        self.add(DET)

                    elif self.sentence[0] in self.prepositions or self.sentence[0].endswith("ward") or self.sentence[0].endswith("wards"):
                        self.add(PREP)
                    
                    elif self.sentence[1] in self.punctuation or self.sentence[0].endswith("'s") or self.sentence[0].endswith("s'"):
                        self.add(NOUN)

                    else:
                        self.add(ADJ)
                        
            else:
                self.add(ADV)
            
            self.add(PUNC)

        if any(self.sentence[0].endswith(s) and self.sentence[0] not in (self.quantifiers_distributives + self.determiners) for s in self.verb_suffixes) or self.sentence[0].endswith("n't"):
            while any(self.sentence[1].endswith(s) and self.sentence[1] not in (self.quantifiers_distributives + self.determiners) for s in self.verb_suffixes) or self.sentence[0].endswith("n't"):
                self.add(AUX)

            self.add(VERB)

        while True:
            if self.sentence[0] in self.punctuation:
                self.add(PUNC)

            elif self.sentence[0] in self.determiners or self.sentence[0] in self.quantifiers_distributives or self.sentence[1] in self.quantifiers_distributives:
                self.add(DET)

            elif self.sentence[0] in self.prepositions or self.sentence[0].endswith("ward") or self.sentence[0].endswith("wards"):
                self.add(PREP)

            elif any(self.sentence[0].endswith(s) and self.sentence[0] != s for s in self.adjective_suffixes):
                if any(self.sentence[1].endswith(s) and self.sentence[0] != s and self.sentence[1] not in (self.quantifiers_distributives + self.determiners) for s in self.verb_suffixes) or self.sentence[1].endswith("n't"):
                    self.add(ADV)

                    while any(self.sentence[1].endswith(s) and self.sentence[1] not in (self.quantifiers_distributives + self.determiners) for s in self.verb_suffixes) or self.sentence[0].endswith("n't"):
                        self.add(AUX)

                    self.add(VERB)

                else:
                    self.add(ADJ)
            
            elif self.sentence[0].endswith("'s") or self.sentence[0].endswith("s'"):
                self.add(NOUN)

            else:
                break

        self.add(NOUN)

        while len(self.sentence) > 1:
            if self.sentence[0] in self.punctuation:
                self.add(PUNC)

            elif any(self.sentence[0].endswith(s) and self.sentence[0] != s and self.sentence[0] not in (self.quantifiers_distributives + self.determiners) for s in self.adjective_suffixes):
                self.add(ADV)

            elif any(self.sentence[1].endswith(s) for s in self.verb_suffixes) or self.sentence[0].endswith("n't"):
                self.add(AUX)

            else:
                break

            if not self.sentence:
                return self.out

        self.add(VERB)

        if self.sentence:
            if self.sentence[0] == "to":
                self.add(AUX)
                self.add(VERB)

        while len(self.sentence) > 1:
            if self.sentence[0] in self.punctuation:
                self.add(PUNC)

            elif self.sentence[0] in self.determiners or self.sentence[0] in self.quantifiers_distributives or self.sentence[1] in self.quantifiers_distributives:
                self.add(DET)

            elif self.sentence[0] in self.prepositions or self.sentence[0].endswith("ward") or self.sentence[0].endswith("wards"):
                self.add(PREP)

            elif any(self.sentence[0].endswith(s) and self.sentence[0] != s for s in self.adjective_suffixes):
                if any(self.sentence[1].endswith(s) and self.sentence[0] != s and self.sentence[1] not in (self.quantifiers_distributives + self.determiners) for s in self.verb_suffixes) or self.sentence[1].endswith("n't"):
                    self.add(ADV)

                    while any(self.sentence[1].endswith(s) and self.sentence[1] not in (self.quantifiers_distributives + self.determiners) for s in self.verb_suffixes) or self.sentence[0].endswith("n't"):
                        self.add(AUX)

                    self.add(VERB)

                else:
                    self.add(ADJ)

            elif any(self.sentence[0].endswith(s) and self.sentence[0] != s for s in self.verb_suffixes) and not (self.sentence[1] in self.prepositions or self.sentence[1].endswith("ward") or self.sentence[1].endswith("wards")):
                self.add(ADJ)

            else:
                break

        while self.sentence:
            if self.sentence[0] in self.punctuation:
                self.add(PUNC)

            elif any(self.sentence[0].endswith(s) for s in self.adjective_suffixes):
                self.add(ADJ)

            elif self.sentence[0] in self.prepositions or self.sentence[0].endswith("ward") or self.sentence[0].endswith("wards"):
                self.add(PREP)
            
            elif self.sentence[0] in self.determiners or self.sentence[0] in self.quantifiers_distributives:
                self.add(DET)

            else:
                self.add(NOUN)
    
        return self.out

while True:
    p = Parse(input("> "))

    try:
        print(p())
    except Exception as e:
        print("Error:", e)
        print("Last state recorded:", p.out)