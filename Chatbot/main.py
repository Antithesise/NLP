from re import split


class SENTENCE(list):
    def __repr__(self) -> str:
        return "SENTENCE(%s)" % " ".join([repr(w) for w in self.copy()])
class NOUN(str):
    def __repr__(self) -> str:
        return super().__repr__().strip("'\"") + " (n)"
class ADJ(str):
    def __repr__(self) -> str:
        return super().__repr__().strip("'\"") + " (adj)"
class ADV(str):
    def __repr__(self) -> str:
        return super().__repr__().strip("'\"") + " (adv)"
class VERB(str):
    def __repr__(self) -> str:
        return super().__repr__().strip("'\"") + " (v)"
class AUX(str):
    def __repr__(self) -> str:
        return super().__repr__().strip("'\"") + " (aux)"
class DET(str):
    def __repr__(self) -> str:
        return super().__repr__().strip("'\"") + " (d)"
class PRON(str):
    def __repr__(self) -> str:
        return super().__repr__().strip("'\"") + " (pn)"
class PREP(str):
    def __repr__(self) -> str:
        return super().__repr__().strip("'\"") + " (pre)"
class INT(str):
    def __repr__(self) -> str:
        return super().__repr__().strip("'\"") + " (int)"
class CONJ(str):
    def __repr__(self) -> str:
        return super().__repr__().strip("'\"") + " (cj)"

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

    def __init__(self, sentence: str) -> None:
        self.sentence = [w for w in split(r" ", sentence.lower()) if w]
        self.out = SENTENCE()

    def __call__(self) -> list:
        while any(self.sentence[0].endswith(s) for s in self.adjective_suffixes):
            self.out.append(ADV(self.sentence.pop(0)))

        while True:
            if self.sentence[0] in self.determiners:
                self.out.append(DET(self.sentence.pop(0)))

            elif self.sentence[0] in self.quantifiers_distributives:
                self.out.append(DET(self.sentence.pop(0)))

            elif self.sentence[1] in self.quantifiers_distributives:
                self.out.append(DET(self.sentence.pop(0)))

            elif self.sentence[0] in self.prepositions or self.sentence[0].endswith("ward") or self.sentence[0].endswith("wards"):
                self.out.append(PREP(self.sentence.pop(0)))

            elif any(self.sentence[0].endswith(s) for s in self.adjective_suffixes):
                if any(self.sentence[1].endswith(s) and self.sentence[1] not in (self.quantifiers_distributives + self.determiners) for s in self.verb_suffixes):
                    self.out.append(ADV(self.sentence.pop(0)))
                
                    while any(self.sentence[1].endswith(s) and self.sentence[1] not in (self.quantifiers_distributives + self.determiners) for s in self.verb_suffixes):
                        self.out.append(AUX(self.sentence.pop(0)))
                    
                    self.out.append(VERB(self.sentence.pop(0)))
                
                else:
                    self.out.append(ADJ(self.sentence.pop(0)))

            else:
                break
        
        self.out.append(NOUN(self.sentence.pop(0)))

        while any(self.sentence[0].endswith(s) for s in self.adjective_suffixes) or any(self.sentence[0].endswith(s) for s in self.verb_suffixes):
            if any(self.sentence[0].endswith(s) for s in self.adjective_suffixes):
                self.out.append(ADV(self.sentence.pop(0)))

            elif any(self.sentence[0].endswith(s) for s in self.verb_suffixes):
                while any(self.sentence[1].endswith(s) for s in self.verb_suffixes):
                    self.out.append(AUX(self.sentence.pop(0)))
                
                self.out.append(VERB(self.sentence.pop(0)))

        while len(self.sentence) > 1:
            if self.sentence[0] in self.determiners:
                self.out.append(DET(self.sentence.pop(0)))

            elif self.sentence[0] in self.quantifiers_distributives:
                self.out.append(DET(self.sentence.pop(0)))

            elif self.sentence[1] in self.quantifiers_distributives:
                self.out.append(DET(self.sentence.pop(0)))

            elif self.sentence[0] in self.prepositions or self.sentence[0].endswith("ward") or self.sentence[0].endswith("wards"):
                self.out.append(PREP(self.sentence.pop(0)))

            elif any(self.sentence[0].endswith(s) for s in self.adjective_suffixes):
                if any(self.sentence[1].endswith(s) and self.sentence[1] not in (self.quantifiers_distributives + self.determiners) for s in self.verb_suffixes):
                    self.out.append(ADV(self.sentence.pop(0)))
                
                    while any(self.sentence[1].endswith(s) and self.sentence[1] not in (self.quantifiers_distributives + self.determiners) for s in self.verb_suffixes):
                        self.out.append(AUX(self.sentence.pop(0)))
                    
                    self.out.append(VERB(self.sentence.pop(0)))
                
                else:
                    self.out.append(ADJ(self.sentence.pop(0)))

            else:
                break
        
        while self.sentence:
            if any(self.sentence[0].endswith(s) for s in self.adjective_suffixes):
                self.out.append(ADV(self.sentence.pop(0)))

            elif self.sentence[0] in self.prepositions or self.sentence[0].endswith("ward") or self.sentence[0].endswith("wards"):
                self.out.append(PREP(self.sentence.pop(0)))

            else:
                self.out.append(NOUN(self.sentence.pop(0)))
    
        return self.out

while True:
    p = Parse(input("> "))

    print(p())