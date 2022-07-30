from re import split, sub


class SENTENCE(list):
    def __repr__(self) -> str:
        return " ".join([repr(w) for w in self.copy()])
class WORDCLASS(str):
    wordclass: str = ""

    def __repr__(self) -> str:
        return super().__repr__().removeprefix("'").removeprefix("\"").removesuffix("'").removesuffix("\"") + f" ({self.wordclass})" * (self.wordclass and self.wordclass != "punc")
class NOUN(WORDCLASS):
    wordclass = "n"
class ADJ(WORDCLASS):
    wordclass = "adj"
class ADV(WORDCLASS):
    wordclass = "adv"
class VERB(WORDCLASS):
    wordclass = "v"
class AUX(WORDCLASS):
    wordclass = "aux"
class DET(WORDCLASS):
    wordclass = "d"
class PRON(WORDCLASS):
    wordclass = "pn"
class PREP(WORDCLASS):
    wordclass = "pre"
class INT(WORDCLASS):
    wordclass = "int"
class CONJ(WORDCLASS):
    wordclass = "conj"
class PUNC(WORDCLASS):
    wordclass = "punc"


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
        "al",
        "ant",
        "ary",
        "ent",
        "free",
        "ful",
        "full",
        "ian",
        "ible",
        "ile",
        "ish",
        "ive",
        "less",
        "like",
        "ous",
        "y",
    ]
    auxiliary_verbs = [
        "to",
        "will",
        "would"
    ]
    verb_suffixes = [
        "ed",
        "en",
        "er",
        "es",
        "ng",
        "ize",
        "ise",
    ]
    conjunctions = [
        "and",
        "but",
        "for",
        "nor",
        "or",
        "so"
        "yet",
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
    adverbs = [
        "also",
        "too"
    ]
    punctuation = ",.;:?!"

    substitute = {
        r"one another": "oneanother",
        r"each other": "eachother",
        r"no one": "noone"
    }

    def __init__(self, sentence: str) -> None:
        sentence = sentence.lower()

        for k, v in self.substitute.items():
            sentence = sub(k, v, sentence)

        self.sentence = [w for w in split(r" |(?=[,.;:?!])", sentence) if w]
        self.out: SENTENCE[WORDCLASS] = SENTENCE()
    
    def add(self, WClass: WORDCLASS) -> None:
        self.out.append(WClass(self.sentence.pop(0)))

    def __call__(self) -> list:
        if "," in self.sentence:
            while (any(self.sentence[0].endswith(s) for s in self.adjective_suffixes) or self.sentence[0] in self.prepositions or self.sentence[0].endswith("ward") or self.sentence[0].endswith("wards")) and self.sentence[0] not in (self.pronouns + self.determiners + self.quantifiers_distributives):
                if self.sentence[1] != ",":
                    while self.sentence[0] != ",":
                        if (self.sentence[0] in (self.determiners + self.quantifiers_distributives) or self.sentence[1] in self.quantifiers_distributives) and self.sentence[1] != ",":
                            self.add(DET)
                        
                        elif self.sentence[0] in self.pronouns:
                            self.add(PRON)
                        
                        elif self.sentence[0] in self.adverbs:
                            self.add(ADV)

                        elif self.sentence[0] in self.prepositions or self.sentence[0].endswith("ward") or self.sentence[0].endswith("wards"):
                            self.add(PREP)
                        
                        elif self.sentence[0] in self.conjunctions:
                            self.add(CONJ)
                        
                        elif self.sentence[1] in (list(self.punctuation) + self.conjunctions) or self.sentence[0].endswith("'s") or self.sentence[0].endswith("s'"):
                            self.add(NOUN)

                        else:
                            self.add(ADJ)
                            
                else:
                    self.add(ADV)
                
                self.add(PUNC)

            if (any(self.sentence[1].endswith(s) and self.sentence[1] != s for s in self.verb_suffixes) and self.sentence[1] not in (self.quantifiers_distributives + self.determiners)) or ("'" in self.sentence[0] and self.sentence[0].split("'")[-1] != "s"):
                while (any(self.sentence[1].endswith(s) and self.sentence[1] != s for s in self.verb_suffixes) and self.sentence[1] not in (self.quantifiers_distributives + self.determiners)) or ("'" in self.sentence[0] and self.sentence[0].split("'")[-1] != "s") or self.sentence[0] in self.auxiliary_verbs:
                    self.add(AUX)

                self.add(VERB)

                if self.sentence:
                    while self.sentence[0] in self.auxiliary_verbs and isinstance(self.out[-1]):
                        self.add(AUX)

                        if len(self.sentence) > 1:
                            if self.sentence[1] in self.auxiliary_verbs:
                                self.add(VERB)

        while len([w for w in self.sentence if w not in self.punctuation]) > 1:
            if self.sentence[0] in self.punctuation:
                self.add(PUNC)

            elif (self.sentence[0] in (self.determiners + self.quantifiers_distributives) or self.sentence[1] in self.quantifiers_distributives) and self.sentence[1] not in self.punctuation:
                self.add(DET)
            
            elif self.sentence[0] in self.adverbs:
                self.add(ADV)

            elif self.sentence[0] in self.prepositions or self.sentence[0].endswith("ward") or self.sentence[0].endswith("wards"):
                self.add(PREP)

            elif self.sentence[0] in self.conjunctions:
                self.add(CONJ)

            elif any(self.sentence[0].endswith(s) and self.sentence[0] != s for s in self.adjective_suffixes):
                if (any(self.sentence[1].endswith(s) and self.sentence[1] != s for s in self.verb_suffixes) and self.sentence[1] not in (self.quantifiers_distributives + self.determiners)) or ("'" in self.sentence[0] and self.sentence[0].split("'")[-1] != "s"):
                    self.add(ADV)

                    while (any(self.sentence[1].endswith(s) and self.sentence[1] != s for s in self.verb_suffixes) and self.sentence[1] not in (self.quantifiers_distributives + self.determiners)) or ("'" in self.sentence[0] and self.sentence[0].split("'")[-1] != "s") or self.sentence[0] in self.auxiliary_verbs:
                        self.add(AUX)

                    self.add(VERB)

                    if self.sentence:
                        while self.sentence[0] in self.auxiliary_verbs and isinstance(self.out[-1]):
                            self.add(AUX)

                            if len(self.sentence) > 1:
                                if self.sentence[1] in self.auxiliary_verbs:
                                    self.add(VERB)

                else:
                    self.add(ADJ)

            elif self.sentence[0].endswith("'s") or self.sentence[0].endswith("s'"):
                self.add(NOUN)

            else:
                break

        if len([w for w in (self.sentence + self.out) if w not in self.punctuation]) == 1:
            self.add(INT)
        elif self.sentence[0] in self.pronouns:
            self.add(PRON)
        else:
            self.add(NOUN)

        while len(self.sentence) > 1:
            if self.sentence[0] in self.punctuation:
                self.add(PUNC)

            elif any(self.sentence[0].endswith(s) and self.sentence[0] != s and self.sentence[0] not in (self.quantifiers_distributives + self.determiners) for s in self.adjective_suffixes) or self.sentence[0] in self.adverbs:
                self.add(ADV)

            elif (any(self.sentence[1].endswith(s) and self.sentence[1] != s for s in self.verb_suffixes) and self.sentence[1] not in (self.quantifiers_distributives + self.determiners + self.pronouns)) or ("'" in self.sentence[0] and self.sentence[0].split("'")[-1] != "s") or self.sentence[0] in self.auxiliary_verbs:
                self.add(AUX)

            else:
                break

        if not self.sentence:
            return self.out
        else:
            while self.sentence[0] in self.punctuation:
                self.add(PUNC)

                if not self.sentence:
                    return self.out

        self.add(VERB)

        if self.sentence[0] in self.adverbs:
            self.add(ADV)

        if self.sentence:
            while self.sentence[0] in self.auxiliary_verbs and isinstance(self.out[-1], VERB):
                self.add(AUX)

                if self.sentence:
                    if all([any(w.endswith(s) for s in self.verb_suffixes) for w in self.sentence if w not in self.punctuation]):
                        self.add(VERB)
                    elif len(self.sentence) > 1:
                        if self.sentence[1] in self.auxiliary_verbs:
                            self.add(VERB)
                else:
                    return self.out

        while len(self.sentence) > 1:
            if (self.sentence[0] in (self.determiners + self.quantifiers_distributives) or self.sentence[1] in self.quantifiers_distributives) and self.sentence[1] not in self.punctuation:
                self.add(DET)

            elif self.sentence[0] in self.pronouns:
                self.add(PRON)

            elif self.sentence[0] in self.prepositions or self.sentence[0].endswith("ward") or self.sentence[0].endswith("wards"):
                self.add(PREP)
            
            elif self.sentence[0] in self.conjunctions:
                self.add(CONJ)

            elif any(self.sentence[0].endswith(s) and self.sentence[0] != s for s in self.adjective_suffixes) and self.out[-1] not in self.determiners:
                if (any(self.sentence[1].endswith(s) and self.sentence[1] != s for s in self.verb_suffixes) and self.sentence[1] not in (self.quantifiers_distributives + self.determiners)) or ("'" in self.sentence[0] and self.sentence[0].split("'")[-1] != "s"):
                    self.add(ADV)

                    while (any(self.sentence[1].endswith(s) and self.sentence[1] != s for s in self.verb_suffixes) and self.sentence[1] not in (self.quantifiers_distributives + self.determiners)) or ("'" in self.sentence[0] and self.sentence[0].split("'")[-1] != "s") or self.sentence[0] in self.auxiliary_verbs:
                        self.add(AUX)

                        if len(self.sentence) == 1:
                            break

                    self.add(VERB)

                    if self.sentence:
                        while self.sentence[0] in self.auxiliary_verbs and isinstance(self.out[-1], VERB):
                            self.add(AUX)

                            if len(self.sentence) > 1:
                                if self.sentence[1] in self.auxiliary_verbs:
                                    self.add(VERB)

                else:
                    self.add(ADJ)

            elif (any(self.sentence[0].endswith(s) and self.sentence[0] != s for s in self.verb_suffixes) and self.sentence[0] not in (self.quantifiers_distributives + self.determiners)) and not (self.sentence[1] in self.prepositions or self.sentence[1].endswith("ward") or self.sentence[1].endswith("wards")) and self.out[-1] not in self.determiners:
                self.add(ADJ)

            else:
                break

        while self.sentence:
            if self.sentence[0] in self.punctuation:
                self.add(PUNC)

                if not self.sentence:
                    break

                if len(self.sentence) > 1:
                    if self.sentence[1] not in self.punctuation:
                        while self.sentence[0] not in self.punctuation:
                            if self.sentence[1] in self.quantifiers_distributives and self.sentence[1] not in self.punctuation:
                                self.add(DET)

                            elif self.sentence[0] in (self.determiners + self.quantifiers_distributives) and len([w for w in self.sentence if w not in self.punctuation]) > 1:
                                self.add(DET)

                            elif self.sentence[0] in self.pronouns:
                                self.add(PRON)

                            elif self.sentence[0] in self.prepositions or self.sentence[0].endswith("ward") or self.sentence[0].endswith("wards"):
                                self.add(PREP)
                            
                            elif self.sentence[0] in self.conjunctions:
                                self.add(CONJ)
                            
                            elif self.sentence[1] in (list(self.punctuation) + self.conjunctions) or self.sentence[0].endswith("'s") or self.sentence[0].endswith("s'"):
                                self.add(NOUN)

                            else:
                                self.add(ADJ)

                            if len(self.sentence) < 2:
                                break

                self.add(ADV)

            elif self.sentence[0] in (self.determiners + self.quantifiers_distributives) and len([w for w in self.sentence if w not in self.punctuation]) > 1:
                self.add(DET)
            
            elif self.sentence[0] in self.pronouns:
                self.add(PRON)

            elif self.sentence[0] in self.adverbs:
                self.add(ADV)

            elif any(self.sentence[0].endswith(s) for s in self.adjective_suffixes):
                self.add(ADJ)

            elif self.sentence[0] in self.prepositions or self.sentence[0].endswith("ward") or self.sentence[0].endswith("wards"):
                self.add(PREP)
            
            elif self.sentence[0] in self.conjunctions:
                self.add(CONJ)

            else:
                self.add(NOUN)
        
        return self.out


if __name__ == "__main__":
    incorrect = 0

    print("\nRunning tests...")

    with open("tests.txt") as f:
        for l in (tests := f.read().strip().split("\n")):
            phrase, correct = l.split("|")

            p = Parse(phrase)

            flag = False

            try:
                print("\n > ", phrase.strip())
                print(end="\n    ")

                for w, c in zip(p(), correct.split()):
                    print(end=f"\x1b[3{(w.wordclass == c) + 1}m" * (w.wordclass != "punc") + f"{repr(w)}\x1b[0m ")

                    flag = flag or w.wordclass != c

                print()
            except Exception as e:
                print("\n    Error:", e)
                print("    Last state recorded:", p.out)

                flag = True
            
            incorrect += flag

    print(f"\nTesting complete: {len(tests) - incorrect}/{len(tests)} correct.\n\n************************************************************\n\nEntering Interactive Mode...")

    while True:
        p = Parse(input("\n >  "))

        try:
            print("\n   \x1b[33m", p(), end="\x1b[0m\n")
        except Exception as e:
            print("\n    \x1b[31mError:", e, end="\x1b[0m\n")
            print("    Last state recorded:", p.out)
