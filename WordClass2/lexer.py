from random import choice
from time import sleep

from typing import Literal


vowels = "aeiouy" # Vowels and consonants (in phonemic orthography, at least). Y can function as a vowel so we can include
consonants = "bcdfghjklmnpqrstvwxyz" # it in the vowels, as these lists is mainly used for conjugation and pluralisation


def conjugate(infinitive: str, tense: Literal["past", "present", "future"]="present", case: Literal["simple", "cont", "perfect", "perfcont"]="simple", plural: bool=False, formal: bool=False, person: int=3, participle: bool=False) -> str:
    conj = {
        "past": {
            "simple": [
                ("*", "*"), # I, we
                ("*", "*"), # you, you
                ("*", "*") # it, they
            ],
            "cont": [
                ("was *", "were *"), # I, we
                ("were *", "were *"), # you, you
                ("was *", "were *") # it, they
            ],
            "perfect": [
                ("had *", "had *"),
                ("had *", "had *"),
                ("had *", "had *")
            ],
            "perfcont": [
                ("had been *", "had been *"), # I, we
                ("had been *", "had been *"), # you, you
                ("had been *", "had been *") # it, they
            ],
        },
        "present": {
            "simple": [
                ("*", "*"), # I, we
                ("*", "*"), # you, you
                ("*", "*") # it, they
            ],
            "cont": [
                ("am *", "are *"), # I, we
                ("are *", "are *"), # you, you
                ("is *", "are *") # it, they
            ],
            "perfect": [
                ("have *", "have *"), # I, we
                ("have *", "have *"), # you, you
                ("has *", "have *") # it, they
            ],
            "perfcont": [
                ("have been *", "have been *"), # I, we
                ("have been *", "have been *"), # you, you
                ("has been *", "have been *") # it, they
            ]
        },
        "future": {
            "simple": [
                ("will *", "will *"), # I, we
                ("will *", "will *"), # you, you
                ("will *", "will *") # it, they
            ],
            "cont": [
                ("will be *", "will be *"), # I, we
                ("will be *", "will be *"), # you, you
                ("will be *", "will be *") # it, they
            ],
            "perfect": [
                ("will have *", "will have *"), # I, we
                ("will have *", "will have *"), # you, you
                ("will have *", "will have *") # it, they
            ],
            "perfcont": [
                ("will have been *", "will have been *"), # I, we
                ("will have been *", "will have been *"), # you, you
                ("will have been *", "will have been *") # it, they
            ]
        },
        "participle": {
            "past": "*",
            "present": "*",
            "perfect": "have *"
        }
    }

    auxconj = { # verb, tense, case, person, plural
        "be": {
            "past": {
                "simple": [
                    ("was", "were"), # I, we
                    ("were", "were"), # you, you
                    ("was", "were") # it, they
                ],
                "cont": [
                    ("was being", "were being"), # I, we
                    ("were being", "were being"), # you, you
                    ("was being", "were being") # it, they
                ],
                "perfect": [
                    ("had been", "had been"),
                    ("had been", "had been"),
                    ("had been", "had been")
                ],
                "perfcont": [
                    ("had been being", "had been being"), # I, we
                    ("had been being", "had been being"), # you, you
                    ("had been being", "had been being") # it, they
                ],
            },
            "present": {
                "simple": [
                    ("am", "are"), # I, we
                    ("are", "are"), # you, you
                    ("is", "are") # it, they
                ],
                "cont": [
                    ("am being", "are being"), # I, we
                    ("are being", "are being"), # you, you
                    ("is being", "are being") # it, they
                ],
                "perfect": [
                    ("have been", "have been"), # I, we
                    ("have been", "have been"), # you, you
                    ("has been", "have been") # it, they
                ],
                "perfcont": [
                    ("have been being", "have been being"), # I, we
                    ("have been being", "have been being"), # you, you
                    ("has been being", "have been being") # it, they
                ]
            },
            "future": {
                "simple": [
                    ("will be", "will be"), # I, we
                    ("will be", "will be"), # you, you
                    ("will be", "will be") # it, they
                ],
                "cont": [
                    ("will be being", "will be being"), # I, we
                    ("will be being", "will be being"), # you, you
                    ("will be being", "will be being") # it, they
                ],
                "perfect": [
                    ("will have been", "will have been"), # I, we
                    ("will have been", "will have been"), # you, you
                    ("will have been", "will have been") # it, they
                ],
                "perfcont": [
                    ("will have been being", "will have been being"), # I, we
                    ("will have been being", "will have been being"), # you, you
                    ("will have been being", "will have been being") # it, they
                ]
            },
            "participle": {
                "past": "been",
                "present": "being",
                "perfect": "having been"
            }
        },
        "do": {
            "past": {
                "simple": [
                    ("did", "did"), # I, we
                    ("did", "did"), # you, you
                    ("did", "did") # it, they
                ],
                "cont": [
                    ("was doing", "were doing"), # I, we
                    ("were doing", "were doing"), # you, you
                    ("was doing", "were doing") # it, they
                ],
                "perfect": [
                    ("had done", "had done"), # I, we
                    ("had done", "had done"), # you, you
                    ("had done", "had done") # it, they
                ],
                "perfcont": [
                    ("had been doing", "had been doing"), # I, we
                    ("had been doing", "had been doing"), # you, you
                    ("had been doing", "had been doing") # it, they
                ]
            },
            "present": {
                "simple": [
                    ("do", "do"), # I, we
                    ("do", "do"), # you, you
                    ("does", "do") # it, they
                ],
                "cont": [
                    ("am doing", "are doing"), # I, we
                    ("are doing", "are doing"), # you, you
                    ("is doing", "are doing") # it, they
                ],
                "perfect": [
                    ("have done", "have done"), # I, we
                    ("have done", "have done"), # you, you
                    ("has done", "have done") # it, they
                ],
                "perfcont": [
                    ("have been doing", "have been doing"), # I, we
                    ("have been doing", "have been doing"), # you, you
                    ("has been doing", "have been doing") # it, they
                ]
            },
            "future": {
                "simple": [
                    ("will do", "will do"), # I, we
                    ("will do", "will do"), # you, you
                    ("will do", "will do") # it, they
                ],
                "cont": [
                    ("will be doing", "will be doing"), # I, we
                    ("will be doing", "will be doing"), # you, you
                    ("will be doing", "will be doing") # it, they
                ],
                "perfect": [
                    ("will have done", "will have done"), # I, we
                    ("will have done", "will have done"), # you, you
                    ("will have done", "will have done") # it, they
                ],
                "perfcont": [
                    ("will have been doing", "will have been doing"), # I, we
                    ("will have been doing", "will have been doing"), # you, you
                    ("will have been doing", "will have been doing") # it, they
                ]
            },
            "participle": {
                "past": "done",
                "present": "doing",
                "perfect": "having done"
            }
        },
        "have": {
            "past": {
                "simple": [
                    ("had", "had"), # I, we
                    ("had", "had"), # you, you
                    ("had", "had") # it, they
                ],
                "cont": [
                    ("was having", "were having"), # I, we
                    ("were having", "were habing"), # you, you
                    ("was having", "were having") # it, they
                ],
                "perfect": [
                    ("had had", "had had"), # I, we
                    ("had had", "had had"), # you, you
                    ("had had", "had had") # it, they
                ],
                "perfcont": [
                    ("was having", "were having"), # I, we
                    ("were having", "were having"), # you, you
                    ("was having", "were having") # it, they
                ]
            },
            "present": {
                "simple": [
                    ("have", "have"), # I, we
                    ("have", "have"), # you, you
                    ("has", "have") # it, they
                ],
                "cont": [
                    ("am having", "are having"), # I, we
                    ("are having", "are having"), # you, you
                    ("is having", "are having") # it, they
                ],
                "perfect": [
                    ("have had", "have had"), # I, we
                    ("have had", "have had"), # you, you
                    ("has had", "have had") # it, they
                ],
                "perfcont": [
                    ("have been having", "have been having"), # I, we
                    ("have been having", "have been having"), # you, you
                    ("has been having", "have been having") # it, they
                ]
            },
            "future": {
                "simple": [
                    ("will have", "will have"), # I, we
                    ("will have", "will have"), # you, you
                    ("will have", "will have") # it, they
                ],
                "cont": [
                    ("will be having", "will be having"), # I, we
                    ("will be having", "will be having"), # you, you
                    ("will be having", "will be having") # it, they
                ],
                "perfect": [
                    ("will have had", "will have had"), # I, we
                    ("will have had", "will have had"), # you, you
                    ("will have had", "will have had") # it, they
                ],
                "perfcont": [
                    ("will have been having", "will have been having"), # I, we
                    ("will have been having", "will have been having"), # you, you
                    ("will have been having", "will have been having") # it, they
                ]
            },
            "participle": {
                "past": "had",
                "present": "having",
                "perfect": "having had"
            }
        }
    }

    if infinitive in auxconj:
        if participle:
            return auxconj[infinitive]["participle"][case if case == "perfect" else "perfect" if tense == "future" else tense]

        return auxconj[infinitive][tense][case][person - 1][plural]

    conjugation = infinitive

    pastp = infinitive
    presentp = infinitive
    perfectp = infinitive

    if infinitive in ["bet", "bite", "cut", "deal", "eat", "give", "grin", "hear", "hurt", "meet", "read", "rise", "sell", "set", "shut", "swim", "wear"]:
        match infinitive:
            case "bet" | "cut" | "shut":
                pastp = pastp
                presentp += "ting"
                perfectp = pastp
            case "bite":
                pastp = "bit"
                presentp += "ing"
                perfectp = pastp + "ten"
            case "deal":
                pastp = "dealt"
                presentp += "ing"
                perfectp = pastp
            case "eat":
                pastp = "ate"
                presentp += "ing"
                perfectp = "eaten"
            case "give":
                pastp = "gave"
                presentp = "giving"
                perfectp += "n"
            case "grin":
                pastp += "ned"
                presentp += "ning"
                perfectp = pastp
            case "hear":
                pastp += "d"
                presentp += "ing"
                perfectp = pastp
            case "meet":
                pastp = "met"
                presentp += "ing"
                perfectp = pastp
            case "rise":
                pastp += "n"
                presentp += "ing"
                perfectp = pastp
            case "sell":
                pastp = "sold"
                presentp += "ing"
                perfectp = pastp
            case "hurt" | "read" | "set":
                pastp = pastp
                presentp += "ing"
                perfectp = pastp
            case "swim":
                pastp = "swam"
                presentp += "ing"
                perfectp = "swum"
            case "wear":
                pastp = "wore"
                presentp += "ing"
                perfectp = "worn"

    elif infinitive.endswith("fight"):
        pastp = pastp[:-4] + "ought"
        presentp += "ing"
        perfectp = pastp

    elif infinitive.endswith("catch"):
        pastp = pastp[:-4] + "aught"
        presentp += "ing"
        perfectp = pastp

    elif infinitive.endswith("leave"):
        pastp = pastp[:-4] + "eft"
        presentp = presentp[:-1] + "ing"
        perfectp = pastp

    elif infinitive.endswith("slide"):
        pastp = pastp[:-1]
        presentp = presentp[:-1] + "ing"
        perfectp = pastp

    elif infinitive.endswith("stand"):
        pastp = pastp[:-3] + "ood"
        presentp = presentp[:-1] + "ing"
        perfectp = pastp

    elif infinitive.endswith("teach"):
        pastp = pastp[:-4] + "ought"
        presentp += "ing"
        perfectp = pastp

    elif infinitive.endswith("think"):
        pastp = pastp[:-3] + "ought"
        presentp += "ing"
        perfectp = pastp

    elif infinitive.endswith("come"):
        pastp = pastp[:-3] + "ame"
        presentp += "ing"
        perfectp = pastp

    elif infinitive.endswith(("hake", "take")):
        pastp = pastp[:-3] + "ook"
        presentp = presentp[:-1] + "ing"
        perfectp = pastp + "n"

    elif infinitive.endswith("hold"):
        pastp = pastp[:-3] + "eld"
        presentp += "ing"
        perfectp = pastp

    elif infinitive.endswith("hide"):
        pastp = pastp[:-1] + "den"
        presentp = presentp[:-1] + "ing"
        perfectp = pastp

    elif infinitive.endswith(("grow", "know", "throw")):
        pastp = pastp[:-2] + "ew"
        presentp += "ing"
        perfectp = perfectp + "n"

    elif infinitive.endswith("make"):
        pastp = pastp[:-2] + "de"
        presentp = presentp[:-1] + "ing"
        perfectp = pastp

    elif infinitive.endswith(("mow", "show", "sow")):
        pastp = pastp + "ed"
        presentp += "ing"
        perfectp = perfectp + "n"

    elif infinitive in ["bid", "forbid"]:
        pastp = pastp[:-2] + "ade"
        presentp = presentp + "ding"
        perfectp = pastp + "den"

    elif infinitive.endswith("ake") and (infinitive in ["bewoke"] or not infinitive.startswith(("b", "c", "f", "o", "s"))):
        pastp = pastp[:-3] + "oke"
        presentp = presentp[:-1] + "ing"
        perfectp = pastp + "n"

    elif infinitive.endswith("eak") and not infinitive.startswith(("c", "l", "pe", "sn", "t", "w")):
        pastp = pastp[:-3] + "oke"
        presentp += "ing"
        perfectp = pastp + "n"

    elif infinitive.endswith("eat"):
        pastp += "en"
        presentp += "ing"
        perfectp = pastp

    elif infinitive.endswith("eel"):
        pastp = pastp[:-2] + "lt"
        presentp += "ing"
        perfectp = pastp

    elif infinitive.endswith("eep"):
        pastp = pastp[:-2] + "pt"
        presentp += "ing"
        perfectp = pastp

    elif infinitive.endswith("get"):
        pastp = pastp[:-2] + "ot"
        presentp += "ting"
        perfectp = pastp + "ten"

    elif infinitive.endswith("hit"):
        pastp = pastp
        presentp += "ting"
        perfectp = pastp

    elif infinitive.endswith(("bind", "find", "grind", "wind")):
        pastp = pastp[:-3] + "ound"
        presentp += "ing"
        perfectp = pastp

    elif infinitive.endswith("ite"):
        pastp = pastp[:-3] + "ote"
        presentp = presentp[:-1] + "ing"
        perfectp = perfectp[:-1] + "ten"

    elif infinitive.endswith(tuple(c + "ay" for c in consonants)) and len(infinitive) == 3:
        pastp = pastp[:-2] + "aid"
        presentp += "ing"
        perfectp = pastp

    elif infinitive.endswith(tuple("oo" + c for c in consonants)):
        pastp += "ed"
        presentp += "ing"
        perfectp = pastp

    elif infinitive.endswith("ee"):
        pastp += "d"
        presentp += "ing"
        perfectp = pastp

    elif infinitive.endswith("et"):
        pastp += "ted"
        presentp += "ing"
        perfectp = pastp

    elif infinitive.endswith("ie"):
        pastp += "d"
        presentp = presentp[:-2] + "ying"
        perfectp = pastp

    elif infinitive.endswith("it"):
        if infinitive.endswith(("posit", "visit")):
            presentp = presentp[:-1]
            pastp += "ed"

        elif infinitive.endswith("hit") or infinitive in ["quit"]:
            pastp = pastp

        elif infinitive.endswith("sit") or infinitive in ["spit"]:
            pastp = pastp[:-2] + "at"

        elif infinitive.endswith(("fit", "kit", "lit", "mit", "nit", "pit")):
            pastp += "ted"

        else:
            pastp += "ed"

        presentp += "ting"
        perfectp = pastp

    elif infinitive.endswith(("bend", "ild", "mend", "send", "spend")) or infinitive in ["forelend", "forlend", "lend"]:
        pastp = pastp[:-1] + "t"
        presentp += "ing"
        perfectp = pastp

    elif infinitive.endswith("un"):
        pastp = pastp[:-2] + "an"
        presentp += "ning"
        perfectp = perfectp

    elif infinitive.endswith(tuple(v * 2 + c for c in consonants for v in vowels) + tuple(v + "il" for v in vowels)):
        pastp += "ed"
        presentp += "ing"
        perfectp = pastp

    elif infinitive.endswith(tuple(v + c for c in consonants for v in vowels if (c not in ["d", "n", "r", "w", "x", "y"] or v + c in ["er"]) and v != "y")) and not infinitive.endswith("elop"):
        pastp += pastp[-1] + "ed"
        presentp += presentp[-1] + "ing"
        perfectp = pastp

    elif infinitive.endswith("e"):
        pastp += "d"
        presentp = presentp[:-1] + "ing"
        perfectp = pastp

    elif infinitive.endswith(tuple(c + "y" for c in consonants)):
        pastp = pastp[:-1] + "ied"
        presentp = presentp + "ing"
        perfectp = pastp

    else:
        pastp += "ed"
        presentp += "ing"
        perfectp = pastp

    match case:
        case "cont" | "perfcont":
            conjugation = presentp

        case "perfect":
            conjugation = perfectp

        case _:
            if tense == "present":
                if plural == False and person == 3:
                    if conjugation.endswith(tuple(c + "y" for c in consonants)):
                        conjugation = conjugation[:-1] + "ie"

                    if conjugation.endswith(("ch", "s", "sh", "x")):
                        conjugation += "e"

                    conjugation += "s"

            elif tense == "past":
                conjugation = pastp

    if participle:
        if case != "perfect":
            if tense == "present":
                conjugation = infinitive
            else:
                conjugation = pastp

        conjugation = conj["participle"][case if case == "perfect" else "perfect" if tense == "future" else tense].replace("*", conjugation)

    else:
        conjugation = conj[tense][case][person - 1][plural].replace("*", conjugation)

    print(f"{infinitive}: {['1st', '2nd', '3rd'][person - 1]} person{' formal' * formal}{' plural' * plural}{' participle' * participle} {case}-{tense} -> {conjugation}")

    return conjugation

def pluralise(words: list[str]) -> list[str]:
    out = []

    for w in words:
        if w in ["alumna", "cactus", "die", "larva", "person", "pupa"]:
            match w:
                case "cactus":
                    w = "cactus"
                case "die":
                    w = "dice"
                case "person":
                    w = "people"
                case _:
                    w += "e"
        elif w in ["louse"] or w.endswith("mouse"):
            w = w[:-4] + "ice"
        elif w in ["foot", "goose", "tooth"]:
            w.replace("oo", "ee")
        elif w in ["ox", "cox"]:
            w += "en"
        elif w.endswith(("enon", "rion", "ron")) and w not in ["ton"]:
            w = w[:-2] + "a" # indeterminate
        elif w.endswith("fish"):
            w = w # doesn't change
        elif w.endswith("hild"):
            w += "ren"
        elif w.endswith("ano") and not w.endswith(("piano", "volcano", "vulcano")):
            w = w[:-1] + "i"
        elif w.endswith("eau"):
            w += "x"
        elif w.endswith("ies"):
            w = w # doesn't change
        elif w.endswith("ife"):
            w = w[:-2] + "ves"
        elif w.startswith(("llo", "sso", "tto", "zzo")) and w not in ["armadillo", "hello", "hollo", "hullo"]:
            w = w[:-1] + "i"
        elif w.endswith("man"):
            w = w[:-2] + "en"
        elif w.endswith("quy"):
            w = w[:-1] + "ies"
        elif w.endswith("tex"):
            w = w[:-2] + "ices"
        elif w.endswith("ton") and not w.startswith("c"):
            w = w[:-2] + "a" # indeterminate
        elif w.endswith("is"):
            w = w[:-2] + "es"
        elif w.endswith("ix") and w not in ["fix", "flix", "nix", "six"]:
            w = w[:-2] + "ices"
        elif w.endswith("ma"):
            w += "ta" # indeterminate
        elif w.endswith("um") and len(w) > 3 and w not in ["forum", "grum", "museum", "plum", "scum", "scrum", "thrum"]:
            w = w[:-2] + "a"
        elif w.endswith("us") and len(w) > 4 and w not in ["meatus", "status", "apparatus"]:
            w = w[:-2] + "i"
        elif w.endswith(tuple(c + "o" for c in consonants)) and not w.endswith(("piano", "volcano", "vulcano")):
            w += "es" # indeterminate
        elif w.endswith(tuple(c + "y" for c in consonants)):
            w = w[:-1] + "ies"
        elif w.endswith("f") and not w.endswith(("ef", "ff", "golf", "if", "roof", "ulf", "urf")):
            w = w[:-1] + "ves"
        elif w.endswith("i"):
            w += "es" # indeterminate
        elif w.endswith("s"):
            w += "es"
        elif w.endswith("y"):
            w += "s"
        else:
            w += "s"

        out.append(w)

    return out


noun = [
    "acorn",
    "apple",
    "bag",
    "ball",
    "banana",
    "book",
    "cake",
    "car",
    "cat",
    "cookie",
    "desk",
    "dog",
    "dolphin",
    "duck",
    "egg",
    "elephant",
    "feather",
    "fire",
    "fish",
    "flower",
    "globe",
    "grape",
    "guitar",
    "hamburger",
    "hammer",
    "hat",
    "house",
    "ice cream",
    "igloo",
    "island",
    "jacket",
    "jellyfish",
    "jigsaw",
    "juice",
    "key",
    "kite",
    "koala",
    "lamp",
    "laptop",
    "lemon",
    "mango",
    "moon",
    "mountain",
    "mouse",
    "necklace",
    "nest",
    "notebook",
    "ocean",
    "octopus",
    "orange",
    "panda",
    "pencil",
    "penguin",
    "piano",
    "quill",
    "quilt",
    "quokka",
    "rainbow",
    "raincoat",
    "robot",
    "rose",
    "sailboat",
    "star",
    "sun",
    "teddy bear",
    "tiger",
    "tree",
    "umbrella",
    "unicorn",
    "vase",
    "vase",
    "violin",
    "wagon",
    "waterfall",
    "whale",
    "window",
    "xylophone",
    "yacht",
    "yoghurt",
    "zebra",
    "zeppelin",
]
plnoun = pluralise(noun)
art = [
    "a",
    "the"
]
plart = [
    "the",
    "no"
]
det = [
    "every"
]
pldet = [
    "all",
    "both",
    "most",
    "many"
]
quant = [
    "one"
]
plquant = [
    "zero",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten"
]
adj = [
    "tall",
    "short",
    "red",
    "blue",
    "green",
    "single"
]
adv = [
    "fast",
    "slowly",
    "grumpily",
    "happily"
]
praverb = averb = [
    "be",
    "do",
    "have"
]
prplaverb = plaverb = [
    "be",
    "do",
    "have"
]
mverb = [
    "can",
    "could",
    "may",
    "might",
    "must",
    "should",
    "will",
    "would",
]
mverb2 = [
    "can",
    "could",
    "dare",
    "may",
    "might",
    "must",
    "need",
    "ought",
    "should",
    "will",
    "would",
]
priverb = iverb = [
    "act",
    "admire",
    "agree",
    "appear",
    "applaud",
    "appreciate",
    "approve",
    "arrive",
    "ask",
    "assert",
    "assure",
    "attempt",
    "attend",
    "attract",
    "avoid",
    "bark",
    "be",
    "bear",
    "beat",
    "become",
    "believe",
    "belong",
    "bend",
    "bet",
    "bite",
    "bless",
    "boil",
    "bounce",
    "break",
    "breathe",
    "celebrate",
    "clap",
    "climb",
    "close",
    "collapse",
    "complain",
    "concentrate",
    "concern",
    "confess",
    "confide",
    "confuse",
    "connect",
    "consist",
    "contain",
    "continue",
    "cry",
    "dance",
    "dare",
    "deal",
    "decide",
    "demand",
    "die",
    "disagree",
    "disappear",
    "drift",
    "drive",
    "dwell",
    "eat",
    "enjoy",
    "exist",
    "fear",
    "feel",
    "fight",
    "find",
    "finish",
    "flow",
    "fly",
    "follow",
    "forget",
    "forgive",
    "freeze",
    "get",
    "go",
    "grin",
    "grow",
    "guess",
    "happen",
    "have",
    "hear",
    "hide",
    "hit",
    "hope",
    "hug",
    "hurry",
    "hurt",
    "imagine",
    "include",
    "intend",
    "invite",
    "jump",
    "laugh",
    "leave",
    "lie",
    "listen",
    "live",
    "look",
    "lose",
    "love",
    "matter",
    "mean",
    "meet",
    "melt",
    "miss",
    "move",
    "notice",
    "obey",
    "observe",
    "open",
    "overlap",
    "own",
    "play",
    "please",
    "point",
    "prefer",
    "prepare",
    "promise",
    "quit",
    "reach",
    "read",
    "realise",
    "receive",
    "recognise",
    "reflect",
    "regret",
    "rejoice",
    "relax",
    "rely",
    "remember",
    "repeat",
    "retire",
    "return",
    "rise",
    "run",
    "rush",
    "sail",
    "say",
    "see",
    "shake",
    "sing",
    "sit",
    "sleep",
    "smile",
    "stand",
    "start",
    "stay",
    "stop",
    "study",
    "succeed",
    "suffer",
    "suggest",
    "surprise",
    "swim",
    "think",
    "travel",
    "try",
    "understand",
    "wait",
    "wake",
    "walk",
    "want",
    "work",
    "worry"
]
prpliverb = pliverb = [
    "act",
    "admire",
    "agree",
    "appear",
    "applaud",
    "appreciate",
    "approve",
    "arrive",
    "ask",
    "assert",
    "assure",
    "attempt",
    "attend",
    "attract",
    "avoid",
    "bark",
    "be",
    "bear",
    "beat",
    "become",
    "believe",
    "belong",
    "bend",
    "bet",
    "bite",
    "bless",
    "boil",
    "bounce",
    "break",
    "breathe",
    "celebrate",
    "clap",
    "climb",
    "close",
    "collapse",
    "complain",
    "concentrate",
    "concern",
    "confess",
    "confide",
    "confuse",
    "connect",
    "consist",
    "contain",
    "continue",
    "cry",
    "dance",
    "dare",
    "deal",
    "decide",
    "demand",
    "disappear",
    "die",
    "disagree",
    "drift",
    "drive",
    "dwell",
    "eat",
    "enjoy",
    "exist",
    "fear",
    "feel",
    "fight",
    "find",
    "finish",
    "flow",
    "fly",
    "follow",
    "forget",
    "forgive",
    "freeze",
    "get",
    "go",
    "grin",
    "grow",
    "guess",
    "happen",
    "have",
    "hear",
    "hide",
    "hit",
    "hope",
    "hug",
    "hurry",
    "hurt",
    "imagine",
    "include",
    "intend",
    "invite",
    "jump",
    "laugh",
    "leave",
    "lie",
    "listen",
    "live",
    "look",
    "lose",
    "love",
    "matter",
    "mean",
    "meet",
    "melt",
    "miss",
    "move",
    "notice",
    "obey",
    "observe",
    "open",
    "overlap",
    "own",
    "play",
    "please",
    "point",
    "prefer",
    "prepare",
    "promise",
    "quit",
    "reach",
    "read",
    "realise",
    "receive",
    "recognise",
    "reflect",
    "regret",
    "rejoice",
    "relax",
    "rely",
    "remember",
    "repeat",
    "retire",
    "return",
    "rise",
    "run",
    "rush",
    "sail",
    "say",
    "see",
    "shake",
    "sing",
    "sit",
    "sleep",
    "smile",
    "stand",
    "start",
    "stay",
    "stop",
    "study",
    "succeed",
    "suffer",
    "suggest",
    "surprise",
    "swim",
    "think",
    "travel",
    "try",
    "understand",
    "wait",
    "wake",
    "walk",
    "want",
    "work",
    "worry"
]
prtverb = tverb = [
    "accept",
    "achieve",
    "add",
    "advise",
    "announce",
    "apologise",
    "attach",
    "bake",
    "blame",
    "borrow",
    "build",
    "buy",
    "calculate",
    "carry",
    "catch",
    "change",
    "cheat",
    "check",
    "choose",
    "clean",
    "copy",
    "count",
    "cut",
    "deliver",
    "describe",
    "develop",
    "discover",
    "discuss",
    "divide",
    "edit",
    "educate",
    "encourage",
    "explain",
    "fix",
    "give",
    "help",
    "hold",
    "improve",
    "influence",
    "inform",
    "introduce",
    "join",
    "keep",
    "kiss",
    "make",
    "manage",
    "mention",
    "mix",
    "need",
    "offer",
    "organise",
    "own",
    "paint",
    "park",
    "pay",
    "perform",
    "permit",
    "plan",
    "present",
    "print",
    "protect",
    "provide",
    "punish",
    "question",
    "record",
    "reduce",
    "refuse",
    "release",
    "remind",
    "repair",
    "replace",
    "report",
    "represent",
    "require",
    "research",
    "respect",
    "save",
    "sell",
    "send",
    "serve",
    "set",
    "settle",
    "show",
    "shut",
    "solve",
    "spend",
    "support",
    "talk",
    "teach",
    "tell",
    "thank",
    "throw",
    "touch",
    "train",
    "try",
    "use",
    "visit",
    "watch",
    "wear",
    "write"
]
prpltverb = pltverb = [
    "accept",
    "achieve",
    "add",
    "advise",
    "announce",
    "apologise",
    "attach",
    "bake",
    "blame",
    "borrow",
    "build",
    "buy",
    "calculate",
    "carry",
    "catch",
    "change",
    "cheat",
    "check",
    "choose",
    "clean",
    "copy",
    "count",
    "cut",
    "deliver",
    "describe",
    "develop",
    "discover",
    "discuss",
    "divide",
    "edit",
    "educate",
    "encourage",
    "explain",
    "fix",
    "give",
    "help",
    "hold",
    "improve",
    "influence",
    "inform",
    "introduce",
    "join",
    "keep",
    "kiss",
    "make",
    "manage",
    "mention",
    "mix",
    "need",
    "offer",
    "organise",
    "own",
    "paint",
    "park",
    "pay",
    "perform",
    "permit",
    "plan",
    "present",
    "print",
    "protect",
    "provide",
    "punish",
    "question",
    "record",
    "reduce",
    "refuse",
    "release",
    "remind",
    "repair",
    "replace",
    "report",
    "represent",
    "require",
    "research",
    "respect",
    "save",
    "sell",
    "send",
    "serve",
    "set",
    "settle",
    "show",
    "shut",
    "solve",
    "spend",
    "support",
    "talk",
    "teach",
    "tell",
    "thank",
    "throw",
    "touch",
    "train",
    "try",
    "use",
    "visit",
    "watch",
    "wear",
    "write"
]
comp = [
    "more",
    "less",
    "longer",
    "shorter"
]
suplat = [
    "most",
    "least",
    "longest",
    "shorter"
]
prep = [
    "at",
    "for",
    "in",
    "on",
    "over",
    "to",
    "under",
    "through",
    "around"
]
coord = [
    "for",
    "and",
    "but",
    "or",
    "yet",
    "so"
]

classnames = [
    "noun", "plnoun", "art", "plart", "det", "pldet", "quant", "plquant", "adj", "adv", "averb", "plaverb", "praverb", "prplaverb", "mverb", "mverb2", "iverb", "pliverb", "priverb", "prpliverb", "tverb", "pltverb", "prtverb", "prpltverb", "comp", "suplat", "prep", "coord"
]
structnames = [
    "dp", "pldp", "qp", "plqp", "ap", "cn", "plcn", "np", "plnp", "cnp", "plcnp", "pp", "plpp", "cpp", "plcpp", "avp", "plavp", "cavp", "plcavp", "pravp", "prplavp", "prcavp", "prplcavp", "ivp", "plivp", "civp", "plcivp", "privp", "prplivp", "prcivp", "prplcivp", "tvp", "pltvp", "ctvp", "plctvp", "prtvp", "prpltvp", "prctvp", "prplctvp", "c", "mc", "cc", "cmc", "ac", "mac", "cac", "cmac", "cs", "ccs", "s"
]

structures = {
    "dp": ["*/det", "*/art"],
    "pldp": ["*/pldet", "*/plart"],
    "qp": "*/quant",
    "plqp": "*/plquant",
    "ap": "*/adj", # don't want to think obout adj ordering yet
    "cn": {
        # "*/noun": None,
        "*/ap": "*/noun"
    },
    "plcn": {
        # "*/plnoun": None,
        "*/ap": "*/plnoun"
    },
    "np": {
        "*/cn": None,
        "*/dp": "*/cn",
        "*/qp": {
            "*/cn": None,
            "of": {
                "*/det": "*/cn",
                "*/pldet": "*/plcn",
                "*/plart": {
                    "*/plcn": None,
                    "*/plqp": "*/plcn"
                },
                "*/qp": "*/cn",
                "*/plqp": "*/plcn"
            }
        }
    },
    "plnp": {
        "*/plcn": None,
        "*/plart": {
            "*/plcn": None,
            "*/plqp": "*/plcn"
        },
        "*/pldet": {
            "*/plcn": None,
            "*/plqp": "*/plcn"
        },
        "*/plqp": {
            "of": {
                "*/det": "*/cn",
                "*/pldet": "*/plcn",
                "*/plart": {
                    "*/plcn": None,
                    "*/plqp": "*/plcn"
                },
                "*/qp": "*/cn",
                "*/plqp": "*/plcn"
            },
            "*/plcn": None
        }
    },
    "cnp": {
        "*/np": None
    },
    "plcnp": {
        "*/plnp": None,
        "both": {
            "*/np": {
                ",": {
                    "and": {
                        "*/np": ","
                    }
                },
            },
            "*/plnp": {
                ",": {
                    "and": {
                        "*/plnp": ","
                    }
                },
            },
        },
        "either": {
            "*/np": {
                ",": {
                    "or": {
                        "*/np": ","
                    }
                },
            },
            "*/plnp": {
                ",": {
                    "or": {
                        "*/plnp": ","
                    }
                },
            },
        },
        "neither": {
            "*/np": {
                ",": {
                    "nor": {
                        "*/np": ","
                    }
                },
            },
            "*/plnp": {
                ",": {
                    "nor": {
                        "*/plnp": ","
                    }
                },
            },
        },
        "*/pldet": {
            "except": {
                "for": ["*/np", "*/plnp"]
            }
        },
        "not": {
            "only": {
                "*/np": {
                    ",": {
                        "but": {
                            "also": "*/np",
                            "*/np": {
                                "also": ","
                            }
                        }
                    }
                },
                "*/plnp": {
                    ",": {
                        "but": {
                            "also": "*/plnp",
                            "*/plnp": {
                                "also": ","
                            }
                        }
                    }
                }
            },
            "*/np": {
                ",": {
                    "but": {
                        "rather": {
                            ",": "*/np"
                        }
                    }
                }
            },
            "*/plnp": {
                ",": {
                    "but": {
                        "rather": {
                            ",": "*/np"
                        }
                    }
                }
            }
        },
    },
    "pp": {
        "*/prep": "*/np"
    },
    "plpp": {
        "*/prep": "*/plnp"
    },
    "cpp": {
        "*/pp": None,
        "*/prep": "*/cnp"
    },
    "plcpp": {
        "*/plpp": None,
        "*/prep": "*/plcnp"
    },
    "avp": {
        "*/averb": "*/np"
    },
    "plavp": {
        "*/plaverb": "*/plnp"
    },
    "cavp": {
        "*/averb": "*/cnp"
    },
    "plcavp": {
        "*/plaverb": "*/plcnp"
    },
    "pravp": {
        "*/praverb": "*/np"
    },
    "prplavp": {
        "*/prplaverb": "*/plnp"
    },
    "prcavp": {
        "*/praverb": "*/cnp"
    },
    "prplcavp": {
        "*/prplaverb": "*/plcnp"
    },
    "ivp": {
        "*/iverb": {
            "*/adv": None,
            "*/cpp": None,
            "*/plpp": None,
            "*/prep": "*/prpltvp"
        }
    },
    "plivp": {
        "*/pliverb": {
            "*/adv": None,
            "*/cpp": None,
            "*/plpp": None,
            "*/prep": "*/prpltvp"
        }
    },
    "civp": {
        "*/ivp": None,
        "*/iverb": {
            "*/adv": None,
            "*/cpp": None,
            "*/plcpp": None,
            "*/prep": "*/prplctvp"
        }
    },
    "plcivp": {
        "*/plivp": None,
        "*/pliverb": {
            "*/adv": None,
            "*/cpp": None,
            "*/plcpp": None,
            "*/prep": "*/prplctvp"
        }
    },
    "privp": {
        "*/priverb": {
            "*/adv": None,
            "*/cpp": None,
            "*/plpp": None,
            "*/prep": "*/prpltvp"
        }
    },
    "prplivp": {
        "*/prpliverb": {
            "*/adv": None,
            "*/cpp": None,
            "*/plpp": None,
            "*/prep": "*/prpltvp"
        }
    },
    "prcivp": {
        "*/privp": None,
        "*/priverb": {
            "*/adv": None,
            "*/cpp": None,
            "*/plcpp": None,
            "*/prep": "*/prplctvp"
        }
    },
    "prplcivp": {
        "*/prplivp": None,
        "*/prpliverb": {
            "*/adv": None,
            "*/cpp": None,
            "*/plcpp": None,
            "*/prep": "*/prplctvp"
        }
    },
    "tvp": {
        "*/avp": None,
        "*/tverb": "*/np"
    },
    "pltvp": {
        "*/plavp": None,
        "*/pltverb": "*/np"
    },
    "ctvp": {
        "*/tvp": None,
        "*/cavp": None,
        "*/tverb": "*/cnp"
    },
    "plctvp": {
        "*/pltvp": None,
        "*/plcavp": None,
        "*/pltverb": "*/cnp"
    },
    "prtvp": {
        "*/pravp": None,
        "*/prtverb": "*/np"
    },
    "prpltvp": {
        "*/prplavp": None,
        "*/prpltverb": "*/np"
    },
    "prctvp": {
        "*/prtvp": None,
        "*/prcavp": None,
        "*/prtverb": "*/cnp"
    },
    "prplctvp": {
        "*/prpltvp": None,
        "*/prplcavp": None,
        "*/prpltverb": "*/cnp"
    },
    "c": {
        "*/ac": None,
        "*/np": ["*/ivp", "*/tvp"],
        "*/plnp": ["*/plivp", "*/pltvp"]
    },
    "mc": {
        "*/c": None,
        "*/mac": None,
        "*/np": {
            "*/mverb2": ["*/prplivp", "*/prpltvp"]
        },
        "*/plnp": {
            "*/mverb2": ["*/prplivp", "*/prpltvp"]
        }
    },
    "cc": {
        "*/c": None,
        "*/cac": None,
        "*/cnp": ["*/civp", "*/ctvp"],
        "*/plcnp": ["*/plcivp", "*/plctvp"]
    },
    "cmc": {
        "*/mc": None,
        "*/cmac": None,
        "*/cnp": {
            "*/mverb2": ["*/prplcivp", "*/prplctvp"]
        },
        "*/plcnp": {
            "*/mverb2": ["*/prplcivp", "*/prplctvp"]
        }
    },
    "ac": {
        "*/np": "*/avp",
        "*/plnp": "*/plavp"
    },
    "mac": {
        "*/ac": None,
        "*/np": {
            "*/mverb2": "*/prplavp"
        },
        "*/plnp": {
            "*/mverb2": "*/prplavp"
        }
    },
    "cac": {
        "*/ac": None,
        "*/cnp": "*/cavp",
        "*/plcnp": "*/plcavp"
    },
    "cmac": {
        "*/mac": None,
        "*/cnp": {
            "*/mverb2": "*/prplcavp"
        },
        "*/plcnp": {
            "*/mverb2": "*/prplcavp"
        }
    },
    "cs": {
        "*/c": {
            ",": {
                "*/coord": ["*/c", "*/mc"]
            }
        },
        "*/mc": {
            ",": {
                "*/coord": ["*/c", "*/mc"]
            }
        },
        "*/corrl": None
    },
    "ccs": {
        "*/cs": None,
        "*/cc": {
            ",": {
                "*/coord": ["*/cc", "*/cmc"]
            }
        },
        "*/cmc": {
            ",": {
                "*/coord": ["*/cc", "*/cmc"]
            }
        },
        "*/corrl": None
    },
    "s": ["*/cc", "*/ccs"]
}
corrl = {
    "as": {
        "*/adj": {
            "as": {
                "*/cnp": {
                    ",": ["*/cc", "*/cmc"]
                },
                "*/cac": {
                    ",": ["*/cc", "*/cmc"]
                }
            }
        }
    },
    "not": {
        "*/adv": {
            ",": {
                "but": {
                    "*/adv": {
                        "*/cc": None,
                        "*/cmc": None,
                        "*/mverb": "*/cc"
                    }
                }
            }
        }
    },
    "rather" : {
        "than": {
            "*/prplcivp": {
                ",": {
                    "*/np": {
                        "*/mverb": {
                            "instead": ["*/prplcivp", "*/prplctvp"],
                            "rather": ["*/prplcivp", "*/prplctvp"]
                        }
                    },
                    "*/plnp": {
                        "*/mverb": {
                            "instead": ["*/prplcivp", "*/prplctvp"],
                            "rather": ["*/prplcivp", "*/prplctvp"]
                        }
                    }
                }
            },
            "*/prplctvp": {
                ",": {
                    "*/np": {
                        "*/mverb": {
                            "instead": ["*/prplcivp", "*/prplctvp"],
                            "rather": ["*/prplcivp", "*/prplctvp"]
                        }
                    },
                    "*/plnp": {
                        "*/mverb": {
                            "instead": ["*/prplcivp", "*/prplctvp"],
                            "rather": ["*/prplcivp", "*/prplctvp"]
                        }
                    }
                }
            }
        }
    },
    "*/np": {
        "*/mverb": {
            "rather": {
                "*/prplcivp": {
                    "than": ["*/prplcivp", "*/prplctvp"]
                },
                "*/prplctvp": {
                    "than": ["*/prplcivp", "*/prplctvp"]
                }
            }
        }
    },
    "*/plnp": {
        "*/mverb": {
            "rather": {
                "*/prplcivp": {
                    "than": ["*/prplcivp", "*/prplctvp"]
                },
                "*/prplctvp": {
                    "than": ["*/prplcivp", "*/prplctvp"]
                }
            }
        }
    },
    "the": {
        "*/comp": {
            "*/cnp": {
                "*/civp": {
                    ",": {
                        "the": {
                            "*/comp": ["*/cc", "*/cmc"]
                        }
                    }
                },
                "*/ctvp": {
                    ",": {
                        "the": {
                            "*/comp": ["*/cc", "*/cmc"]
                        }
                    }
                }
            },
            "*/plcnp": {
                "*/plcivp": {
                    ",": {
                        "the": {
                            "*/comp": ["*/cc", "*/cmc"]
                        }
                    }
                },
                "*/plctvp": {
                    ",": {
                        "the": {
                            "*/comp": ["*/cc", "*/cmc"]
                        }
                    }
                }
            }
        }
    },
    "whether" : {
        "*/cc": {
            ",": {
                "or": {
                    "not": {
                        ",": ["*/cc", "*/cmc"]
                    },
                    "*/cc": {
                        ",": ["*/cc", "*/cmc"]
                    },
                    "*/cmc": {
                        ",": ["*/cc", "*/cmc"]
                    }
                }
            }
        },
        "*/cmc": {
            ",": {
                "or": {
                    "not": {
                        ",": ["*/cc", "*/cmc"]
                    },
                    "*/cc": {
                        ",": ["*/cc", "*/cmc"]
                    },
                    "*/cmc": {
                        ",": ["*/cc", "*/cmc"]
                    }
                }
            }
        }
    },
    "while": {
        "*/cc": {
            ",": {
                "*/np": {
                    "*/mverb": {
                        "also": ["*/prplcivp", "*/prplctvp"]
                    }
                },
                "*/plnp": {
                    "*/mverb": {
                        "also": ["*/prplcivp", "*/prplctvp"]
                    }
                }
            }
        },
        "*/cmc": {
            ",": {
                "*/np": {
                    "*/mverb": {
                        "also": ["*/prplcivp", "*/prplctvp"]
                    }
                },
                "*/plnp": {
                    "*/mverb": {
                        "also": ["*/prplcivp", "*/prplctvp"]
                    }
                }
            }
        }
    }
}


def factory(head: dict | list | str | None, tail: dict | list | str | None=None, depth: int=0, random: bool=True) -> list[str]:
    res = []

    if depth > 40 or head is tail is None:
        return [""]

    if random:
        if isinstance(head, str):
            if "*" in head:
                w = head.rsplit("/", 1)[-1]

                if w in classnames:
                    res += [choice(globals()[w])]

                elif w in structnames:
                    res += [t for t in factory(structures[w], None, depth+1, random) if t]

                elif w == "corrl":
                    res += [t for t in factory(corrl, None, depth+1, random) if t]

                else:
                    raise ValueError(f"{w} not a registered class or phrase type")

                if w.endswith(("averb", "iverb", "tverb")):
                    res = [choice([conjugate(r, tense, case, w.startswith(("pl", "prpl")), formal, person, w.startswith("pr")) for person in [3] for formal in [False, True] for case in ["simple", "cont", "perfect", "perfcont"] for tense in ["past", "present", "future"] for r in res])] # type: ignore

            else:
                res.append(head)

        elif isinstance(head, dict):
            res += [h for h in factory(*choice(list(head.items())), depth+1, random) if h]

        elif isinstance(head, list):
            res += [t for t in factory(choice(head), None, depth+1, random) if t]

        else:
            raise ValueError(f"{head} not a registered class or phrase type, or a pattern containing the aforementioned")

    else:
        if isinstance(head, str):
            if "*" in head:
                w = head.rsplit("/", 1)[-1]

                if w in classnames:
                    res += globals()[w]

                elif w in structnames:
                    res += [t for t in factory(structures[w], None, depth+1, random) if t]

                elif w == "corrl":
                    res += [t for t in factory(corrl, None, depth+1, random) if t]

                else:
                    raise ValueError(f"{w} not a registered class or phrase type")

                if w.endswith(("averb", "iverb", "tverb")):
                    res = [conjugate(r, tense, case, w.startswith(("pl", "prpl")), formal, person, w.startswith("pr")) for person in [3] for formal in [False, True] for case in ["simple", "cont", "perfect", "perfcont"] for tense in (["present"] if w.startswith("pr") else ["past", "present", "future"]) for r in res] # type: ignore

            else:
                res.append(head)

        elif isinstance(head, dict):
            for k, v in head.items():
                res += [h for h in factory(k, v, depth+1, random) if h]

        elif isinstance(head, list):
            for p in head:
                if p:
                    res += [t for t in factory(p, None, depth+1, random) if t]

        else:
            raise ValueError(f"{head} not a registered class or phrase type, or a pattern containing the aforementioned")

    res = [h.replace(" ,", ",").replace(",,", ",") if t == None else (h + " " * bool(t) + t).replace(" ,", ",").replace(",,", ",") for t in factory(tail, None, depth+1, random) for h in res if h or t]

    return res


if __name__ == "__main__":
    while True:
        sentences = factory("*/s", random=True)

        for s in sentences or []:
            print(s.rstrip(".") + ".")

        sleep(1)