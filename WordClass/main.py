from re import split, sub


class WORDCLASS(str):
    wordclass: str = ""

    def __repr__(self) -> str:
        return self + f" ({self.wordclass})" * (self.wordclass and self.wordclass != "punc")

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
class QUOTE(WORDCLASS):
    wordclass = "q"

class SENTENCE(list[WORDCLASS]):
    def __repr__(self) -> str:
        return " ".join([repr(w) for w in self.copy()])


class Parser:
    subordinating_conjunctions = [
        "after",
        "although",
        "as",
        "because",
        "before",
        "even",
        "if",
        "in",
        "inasmuch",
        "just",
        "lest",
        "now",
        "provided",
        "since",
        "supposing",
        "than",
        "though",
        "till",
        "unless",
        "until",
        "whenever",
        "whereas",
        "wherever",
        "whether",
        "while",
        "whoever"
    ]
    coordinating_conjunctions = [
        "and",
        "but",
        "for",
        "nor",
        "or",
        "so",
        "yet"
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
        "few"
    ] 
    primary_auxiliary_verbs = [
        "am",
        "are",
        "be",
        "being",
        "did",
        "do",
        "does",
        "doing",
        "had",
        "has",
        "have",
        "having",
        "is"
    ]
    modal_auxiliary_verbs = [
        "can",
        "could",
        "may",
        "might",
        "must",
        "shall",
        "should",
        "to",
        "was",
        "were",
        "will",
        "would"
    ]
    adjective_suffixes = [
        "able",
        "al",
        "ant",
        "ary",
        "ent",
        "er",
        "free",
        "ful",
        "full",
        "ian",
        "ible",
        "ican",
        "ile",
        "ish",
        "ive",
        "less",
        "like",
        "ous",
        "y"
    ]
    verb_suffixes = [
        "ed",
        "en",
        "es",
        "ng",
        "ize",
        "ise"
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
        "without"
    ]
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
        "certain"
    ]
    adjectives = [
        "able",
        "available",
        "bad",
        "best",
        "better",
        "big",
        "black",
        "blue",
        "central",
        "certain",
        "clear",
        "cold",
        "common",
        "cultural"
        "current",
        "dark",
        "dead",
        "democratic",
        "different",
        "difficult",
        "early",
        "easy",
        "economic",
        "entire",
        "environmental",
        "federal",
        "final",
        "financial",
        "fine",
        "foreign",
        "free",
        "full",
        "general",
        "good",
        "great",
        "green",
        "happy",
        "hard",
        "high",
        "hot",
        "huge",
        "important",
        "international",
        "large",
        "late",
        "left",
        "legal",
        "likely",
        "little",
        "local",
        "long",
        "low",
        "main",
        "major",
        "medical",
        "national",
        "natural",
        "new",
        "nice",
        "old",
        "only",
        "other",
        "past",
        "personal",
        "physical",
        "political",
        "poor",
        "popular",
        "possible",
        "private",
        "ready",
        "real",
        "recent",
        "red",
        "religious",
        "right",
        "serious",
        "short",
        "significant",
        "similar",
        "simple",
        "single",
        "small",
        "smart",
        "social",
        "special",
        "strong",
        "sure",
        "traditional",
        "true",
        "various",
        "white",
        "whole",
        "young"
    ]
    questions = [
        "how",
        "what",
        "when",
        "where",
        "which",
        "who",
        "whom",
        "whose",
        "why"
    ]
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
        "not",
        "too",
        "almost",
        "always",
        "annually",
        "constantly",
        "continually",
        "continuously",
        "eventually",
        "ever",
        "frequently",
        "generally",
        "hardly",
        "hourly",
        "infrequently",
        "intermittently",
        "later",
        "monthly",
        "mearly",
        "never",
        "next",
        "nightly",
        "normally",
        "now",
        "occasionally",
        "often",
        "periodically",
        "quarterly",
        "rarely",
        "regularly",
        "scarcely",
        "seldom",
        "sometimes",
        "soon",
        "then",
        "today",
        "tonight",
        "usually",
        "weekly",
        "yearly",
        "yesterday",
        "yet"
    ]
    punctuation = [
        ",",
        ".",
        ";",
        ":",
        "?",
        "!",
        "..."
    ]

    substitute = {
        r"one another": "oneanother",
        r"each other": "eachother",
        r"no one": "noone"
    }

    def add(self, WClass: WORDCLASS) -> None:
        self.out.append((QUOTE if self.sentence[0][0] + self.sentence[0][-1] == "\"\"" else WClass)(self.sentence.pop(0)))

    def __call__(self, sentence: str) -> SENTENCE:
        sentence = sentence.lower()
        self.question = False

        for k, v in self.substitute.items():
            sentence = sub(k, v, sentence)

        self.sentence = [w for w in split(r" |(\.\.\.)|(\"[^\"]+\")|(?=[,.;:?!])", sentence) if w]
        self.out = SENTENCE()

        if not self.sentence:
            return self.out

        if "," in self.sentence:
            while ((any(self.sentence[0].endswith(s) for s in self.adjective_suffixes) or self.sentence[0] in self.prepositions or self.sentence[0].endswith("ward") or self.sentence[0].endswith("wards")) and self.sentence[0] not in self.pronouns + self.determiners + self.quantifiers_distributives) and "," in self.sentence:
                if self.sentence[1] != ",":
                    while self.sentence[0] != ",":
                        if (self.sentence[0] in self.determiners + self.quantifiers_distributives or self.sentence[1] in self.quantifiers_distributives) and self.sentence[1] != ",":
                            self.add(DET)

                            if self.sentence[0].endswith("ing"):
                                self.add(ADJ)
                        
                        elif self.sentence[0] in self.pronouns:
                            self.add(PRON)
                        
                        elif (any(self.sentence[0].endswith(s) for s in self.verb_suffixes) or self.sentence[1] in ["is", "are"]) and self.sentence[0] not in self.quantifiers_distributives + self.determiners + self.prepositions:
                            self.add(VERB)
                            
                            while self.sentence[0] in self.modal_auxiliary_verbs or self.sentence[0].endswith("n't"):
                                self.add(AUX)

                                if len(self.sentence) > 1:
                                    if self.sentence[1] in self.modal_auxiliary_verbs or self.sentence[0].endswith("n't"):
                                        self.add(VERB)
                        
                        elif self.sentence[0] in self.adverbs:
                            self.add(ADV)

                        elif self.sentence[0] in self.prepositions or self.sentence[0].endswith("ward") or self.sentence[0].endswith("wards"):
                            self.add(PREP)
                        
                        elif self.sentence[0] in self.coordinating_conjunctions:
                            self.add(CONJ)
                        
                        elif self.sentence[0] in self.adjectives:
                            self.add(ADJ)
                        
                        elif self.sentence[1] in self.punctuation + self.coordinating_conjunctions or self.sentence[0].endswith("'s") or self.sentence[0].endswith("s'"):
                            self.add(NOUN)

                        else:
                            self.add(ADJ)

                else:
                    self.add(ADV)
                
                self.add(PUNC)

            if ((any(self.sentence[1].endswith(s) for s in self.verb_suffixes) or self.sentence[1] in ["is", "are"]) and self.sentence[1] not in self.quantifiers_distributives + self.determiners) or ("'" in self.sentence[0] and self.sentence[0].split("'")[-1] != "s") or self.sentence[0].endswith("n't"):
                while ((any(self.sentence[1].endswith(s) for s in self.verb_suffixes) or self.sentence[1] in ["is", "are"]) and self.sentence[1] not in self.quantifiers_distributives + self.determiners) or ("'" in self.sentence[0] and self.sentence[0].split("'")[-1] != "s") or self.sentence[0] in self.modal_auxiliary_verbs or self.sentence[0].endswith("n't"):
                    self.add(AUX)

                self.add(VERB)

                if self.sentence:
                    while self.sentence[0] in self.modal_auxiliary_verbs or self.sentence[0].endswith("n't"):
                        self.add(AUX)

                        if len(self.sentence) > 1:
                            if self.sentence[1] in self.modal_auxiliary_verbs or self.sentence[0].endswith("n't"):
                                self.add(VERB)

        while self.sentence:
            skip = False

            while self.sentence[0] in self.subordinating_conjunctions:
                self.add(CONJ)

            if self.sentence[0] in self.primary_auxiliary_verbs + self.modal_auxiliary_verbs + self.questions or self.sentence[0].endswith("n't"):
                if self.sentence[0] in ["whose", "which"]:
                    self.add(DET)
                elif self.sentence[0] in self.pronouns:
                    self.add(PRON)
                elif self.out:
                    self.add(AUX)
                else:
                    self.add(VERB)

                self.question = True
            
                while self.sentence[0] in self.primary_auxiliary_verbs:
                    self.add(AUX)
            
            if self.sentence[0] in self.coordinating_conjunctions:
                self.add(CONJ)

            while len([w for w in self.sentence if w not in self.punctuation]) > 2:
                if self.sentence[0] in self.punctuation:
                    self.add(PUNC)

                elif (self.sentence[0] in self.determiners + self.quantifiers_distributives or self.sentence[1] in self.quantifiers_distributives) and self.sentence[1] not in self.punctuation + self.modal_auxiliary_verbs + self.primary_auxiliary_verbs + self.determiners:
                    if len(self.sentence) > 2:
                        if self.sentence[2] == "to" or self.question or (self.sentence[0] in ["this", "that"] and any(self.sentence[1].endswith(s) for s in ["ed", "en", "er", "es", "ize", "ise", "s"] + self.modal_auxiliary_verbs + self.primary_auxiliary_verbs)):
                            break
                        else:
                            self.add(DET)
                    elif self.sentence[0] in ["this", "that"] and any(self.sentence[1].endswith(s) for s in ["ed", "en", "er", "es", "ize", "ise", "s"] + self.modal_auxiliary_verbs + self.primary_auxiliary_verbs):
                        break
                    else:
                        self.add(DET)

                    if self.sentence[0].endswith("ing"):
                        self.add(ADJ)
                
                elif self.sentence[0] in self.adverbs:
                    self.add(ADV)

                elif self.sentence[0] in self.prepositions or self.sentence[0].endswith("ward") or self.sentence[0].endswith("wards"):
                    self.add(PREP)

                elif self.sentence[0] in self.coordinating_conjunctions:
                    self.add(CONJ)

                elif any(self.sentence[0].endswith(s) and self.sentence[0] != s for s in self.adjective_suffixes) and any(w.wordclass == "n" for w in self.out):
                    if ((any(self.sentence[1].endswith(s) for s in self.verb_suffixes) or self.sentence[1] in ["is", "are"]) and self.sentence[1] not in self.quantifiers_distributives + self.determiners) or ("'" in self.sentence[0] and self.sentence[0].split("'")[-1] != "s"):
                        self.add(ADV)

                        while ((any(self.sentence[1].endswith(s) for s in self.verb_suffixes) or self.sentence[1] in ["is", "are"]) and self.sentence[1] not in self.quantifiers_distributives + self.determiners) or ("'" in self.sentence[0] and self.sentence[0].split("'")[-1] != "s") or self.sentence[0] in self.modal_auxiliary_verbs or self.sentence[0].endswith("n't"):
                            self.add(AUX)

                        self.add(VERB)

                        if self.sentence:
                            while self.sentence[0] in self.modal_auxiliary_verbs or self.sentence[0].endswith("n't"):
                                self.add(AUX)

                                if len(self.sentence) > 1:
                                    if self.sentence[1] in self.modal_auxiliary_verbs or self.sentence[0].endswith("n't"):
                                        self.add(VERB)

                    else:
                        self.add(ADJ)

                elif self.sentence[0] in self.adjectives:
                    self.add(ADJ)

                elif (self.sentence[1] in self.determiners + self.quantifiers_distributives + self.prepositions + self.pronouns and self.sentence[0] not in self.pronouns and self.sentence[2] not in self.primary_auxiliary_verbs + self.modal_auxiliary_verbs) or self.sentence[0].endswith("'s") or self.sentence[0].endswith("s'"):
                    self.add(NOUN)

                else:
                    break

            while self.sentence[0].endswith("'s") or self.sentence[0].endswith("s'"):
                self.add(NOUN)

            if len(self.sentence) > 1:
                if not self.out and self.sentence[1] in self.punctuation:
                    self.add(INT)
                elif self.sentence[0] in self.punctuation:
                    self.add(PUNC)
                elif self.sentence[0] in self.pronouns:
                    self.add(PRON)
                else:
                    self.add(NOUN)
            else:
                if not self.out:
                    self.add(INT)
                elif self.sentence[0] in self.punctuation:
                    self.add(PUNC)
                elif self.sentence[0] in self.pronouns:
                    self.add(PRON)
                else:
                    self.add(NOUN)

            while len(self.sentence) > 1 and not self.question:
                if self.sentence[0] in self.punctuation:
                    self.add(PUNC)

                elif any(self.sentence[0].endswith(s) and self.sentence[0] != s and self.sentence[0] not in self.quantifiers_distributives + self.determiners for s in self.adjective_suffixes) or self.sentence[0] in self.adverbs:
                    self.add(ADV)

                elif ((((any(self.sentence[1].endswith(s) for s in self.verb_suffixes) or self.sentence[1] in self.primary_auxiliary_verbs) and self.sentence[1] not in self.quantifiers_distributives + self.determiners + self.pronouns + self.prepositions) or ("'" in self.sentence[0] and self.sentence[0].split("'")[-1] != "s") or self.sentence[0] in self.modal_auxiliary_verbs) and (not any(self.sentence[1].endswith(s) and self.sentence[1] != s for s in self.adjective_suffixes) or any(w.endswith(s) or w in self.primary_auxiliary_verbs for s in self.verb_suffixes for w in self.sentence[1:] if w not in self.punctuation))) or self.sentence[0].endswith("n't"):
                    if self.sentence[0] in self.modal_auxiliary_verbs + self.primary_auxiliary_verbs or self.sentence[0].endswith("n't"):
                        self.add(AUX)
                    else:
                        self.add(VERB)

                else:
                    if self.out[-1].wordclass == "aux" and self.sentence[1] == "to":
                        self.add(AUX)

                    break

            if not self.sentence:
                return self.out
            else:
                while self.sentence[0] in self.punctuation:
                    self.add(PUNC)

                    if not self.sentence:
                        return self.out

            if self.question:
                if self.out[0] not in ["am", "are", "be", "being", "is", "was"]:
                    self.add(VERB)
            else:
                self.add(VERB)

            if not self.sentence:
                return self.out

            if self.sentence[0] in self.adverbs or self.sentence[0].endswith("ly"):
                self.add(ADV)

            if self.sentence:
                while self.sentence[0] in self.modal_auxiliary_verbs + self.primary_auxiliary_verbs and self.out[-1].wordclass == "v":
                    self.add(AUX)

                    if self.sentence:
                        if self.out[-2] == "to" and self.sentence[0] not in self.punctuation + self.determiners + self.quantifiers_distributives + self.prepositions + self.pronouns:
                            self.add(VERB)
                        elif len(self.sentence) > 1:
                            if self.sentence[1] in self.modal_auxiliary_verbs or self.sentence[0].endswith("n't"):
                                self.add(VERB)
                    else:
                        return self.out

            while len(self.sentence) > 1 and not skip:
                if (self.sentence[0] in self.determiners + self.quantifiers_distributives or self.sentence[1] in self.quantifiers_distributives) and self.sentence[1] not in self.punctuation + self.modal_auxiliary_verbs + self.primary_auxiliary_verbs + self.determiners:
                    self.add(DET)

                    if self.sentence[0].endswith("ing"):
                        self.add(ADJ)

                elif self.sentence[0] in self.pronouns:
                    if self.sentence[0] in self.questions:
                        self.question = True

                    self.add(PRON)

                elif (self.sentence[0] in self.coordinating_conjunctions or self.sentence[0] in self.subordinating_conjunctions) and ((any(self.sentence[1].endswith(s) for s in self.verb_suffixes) or self.sentence[1] in self.primary_auxiliary_verbs) or ("'" in self.sentence[1] and self.sentence[0].split("'")[-1] != "s") or self.sentence[1] in self.modal_auxiliary_verbs + self.punctuation + self.determiners + self.quantifiers_distributives + self.prepositions + self.pronouns or self.sentence[1].endswith("n't")):
                    self.add(CONJ)

                    skip = True

                    continue

                elif self.sentence[0] in self.prepositions or self.sentence[0].endswith("ward") or self.sentence[0].endswith("wards"):
                    if self.sentence[1] in self.punctuation and not self.question:
                        self.add(ADV)
                    else:
                        self.add(PREP)

                elif (any(self.sentence[0].endswith(s) and self.sentence[0] != s for s in self.adjective_suffixes) and self.out[-1] not in self.determiners):
                    if ((any(self.sentence[1].endswith(s) for s in self.verb_suffixes) or self.sentence[1] in ["is", "are"]) and self.sentence[1] not in self.quantifiers_distributives + self.determiners) or ("'" in self.sentence[0] and self.sentence[0].split("'")[-1] != "s"):
                        self.add(ADV)

                        while ((any(self.sentence[1].endswith(s) for s in self.verb_suffixes) or self.sentence[1] in ["is", "are"]) and self.sentence[1] not in self.quantifiers_distributives + self.determiners) or ("'" in self.sentence[0] and self.sentence[0].split("'")[-1] != "s") or self.sentence[0] in self.modal_auxiliary_verbs or self.sentence[0].endswith("n't"):
                            self.add(AUX)

                            if len(self.sentence) == 1:
                                break

                        self.add(VERB)

                        if self.sentence:
                            while self.sentence[0] in self.modal_auxiliary_verbs or self.sentence[0].endswith("n't"):
                                self.add(AUX)

                                if len(self.sentence) > 1:
                                    if self.sentence[1] in self.modal_auxiliary_verbs or self.sentence[0].endswith("n't"):
                                        self.add(VERB)

                    else:
                        self.add(ADJ)

                elif (((any(self.sentence[0].endswith(s) for s in self.verb_suffixes) or self.sentence[0] in ["is", "are"]) and self.sentence[0] not in self.quantifiers_distributives + self.determiners) and not (self.sentence[1] in self.prepositions or self.sentence[1].endswith("ward") or self.sentence[1].endswith("wards")) and self.out[-1] not in self.determiners and not self.out[-1].wordclass == "v" and not self.question) or self.sentence[0] in self.adjectives:
                    self.add(ADJ)

                else:
                    break
            
            if skip:
                continue

            while self.sentence and not skip:
                if self.sentence[0] in self.punctuation:
                    self.add(PUNC)

                    if not self.sentence:
                        break

                    if len(self.sentence) > 1:
                        if self.sentence[1] not in self.punctuation:
                            while self.sentence[0] not in self.punctuation and not skip:
                                if self.sentence[1] in self.quantifiers_distributives and self.sentence[1] not in self.punctuation + self.modal_auxiliary_verbs + self.primary_auxiliary_verbs + self.determiners:
                                    self.add(DET)

                                elif self.sentence[0] in self.determiners + self.quantifiers_distributives and len([w for w in self.sentence if w not in self.punctuation]) > 1:
                                    self.add(DET)

                                    if self.sentence[0].endswith("ing"):
                                        self.add(ADJ)

                                elif self.sentence[0] in self.pronouns:
                                    if self.sentence[0] in self.questions:
                                        self.question = True
                                    
                                    self.add(PRON)

                                elif self.sentence[0] in self.coordinating_conjunctions + self.subordinating_conjunctions:
                                    self.add(CONJ)

                                    skip = True

                                    continue

                                elif self.sentence[0] in self.prepositions or self.sentence[0].endswith("ward") or self.sentence[0].endswith("wards"):
                                    self.add(PREP)

                                elif self.sentence[0] in self.adjectives:
                                    self.add(ADJ)

                                elif self.sentence[1] in self.punctuation + self.coordinating_conjunctions or self.sentence[0].endswith("'s") or self.sentence[0].endswith("s'"):
                                    self.add(NOUN)

                                elif self.sentence[0].endswith("n't"):
                                    self.add(AUX)

                                    self.question = True

                                else:
                                    self.add(ADJ)

                                if len(self.sentence) < 2:
                                    break
                            
                            if skip:
                                continue

                    while self.sentence[0] in self.punctuation:
                        self.add(PUNC)

                        if not self.sentence:
                            return self.out

                    self.add(ADV)

                elif self.sentence[0] in self.determiners + self.quantifiers_distributives and len([w for w in self.sentence if w not in self.punctuation]) > 1:
                    self.add(DET)

                    if self.sentence[0].endswith("ing"):
                        self.add(ADJ)

                elif self.sentence[0] in self.pronouns:
                    if self.sentence[0] in self.questions:
                        self.question = True

                    self.add(PRON)

                elif self.sentence[0] in self.adverbs:
                    self.add(ADV)

                elif self.out[-1].wordclass == "adv":
                    self.add(VERB)

                elif any(self.sentence[0].endswith(s) for s in self.adjective_suffixes):
                    self.add(ADJ)

                elif self.sentence[0] in self.coordinating_conjunctions + self.subordinating_conjunctions:
                    self.add(CONJ)

                    if self.out[-1] != "and":
                        continue

                elif self.sentence[0] in self.prepositions or self.sentence[0].endswith("ward") or self.sentence[0].endswith("wards"):
                    self.add(PREP)

                elif self.sentence[0] in [w for w in self.modal_auxiliary_verbs + self.primary_auxiliary_verbs if w not in ["am", "are", "be", "being", "is", "was", "to"]] or self.sentence[0].endswith("n't"):
                    self.add(AUX)

                elif (any(self.sentence[0].endswith(s) for s in self.verb_suffixes) and not self.out[-1].wordclass == "adj" and self.out[-1] not in self.quantifiers_distributives + self.determiners and not self.question) or self.out[-1].wordclass in ["aux", "adv"]:
                    self.add(VERB)

                elif self.sentence[0] in self.adjectives:
                    self.add(ADJ)

                elif self.question and self.out[0] in self.modal_auxiliary_verbs and self.out[-1].wordclass in ["aux", "v"]:
                    self.add(ADV)

                else:
                    if len(self.sentence) > 1:
                        if any(self.sentence[1].endswith(s) for s in self.adjective_suffixes):
                            self.add(ADJ)
                        else:
                            self.add(NOUN)
                    else:
                        self.add(NOUN)
            
            if skip:
                continue

        return self.out


if __name__ == "__main__":
    parse = Parser()

    print("\nRunning tests...")

    with open("tests.txt") as f:
        incorrect = 0

        for l in (tests := f.read().strip().split("\n")):
            phrase, correct = l.split("|")
            flag = False

            try:
                print("\n > ", phrase.strip())
                print(end="\n    ")

                for w, c in zip(parse(phrase), correct.split()):
                    print(end=f"\x1b[3{(w.wordclass == c) + 1}m" + f"{repr(w)}\x1b[0m ")

                    flag |= w.wordclass != c

                if parse.question:
                    print("(Q)")
                elif any(w.wordclass == "v" for w in parse.out):
                    print("(S)")
                else:
                    print("(F)")
            except Exception as e:
                print("\n    \x1b[31mError:", e, end="\x1b[0m\n")
                print("    Last state recorded:", parse.out)

                flag = True

            incorrect += flag

    print(f"\nTesting complete: {len(tests) - incorrect}/{len(tests)} correct.\n\n************************************************************\n\nEntering Interactive Mode. Press Ctrl+C to exit...")

    while True:
        try:
            print("\n   \x1b[33m", parse(input("\n >  ")), end="\x1b[0m ")

            if parse.question:
                print("(Q)")
            elif any(w.wordclass == "v" for w in parse.out):
                print("(S)")
            elif parse.out:
                print("(F)")

        except KeyboardInterrupt:
            print("\x1b[0m\x1b[2K\rExiting...\n")

            break

        except EOFError:
            print("\x1b[0m\x1b[2K\rExiting...\n")

            break

        except Exception as e:
            print("\n    \x1b[31mError:", e, end="\x1b[0m\n")
            print("    Last state recorded:", parse.out)
