from re import split


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
    "ous"
]

verb_suffixes = [
    "ed",
    "en",
    "er",
    "ing",
    "ize",
    "ise",
    "ened",
    "ered",
    "ized",
    "isee",
]


while True:
    sentence = [w for w in split(r" |('[a-z]+)", input("> ").lower()) if w]
    noun_phrase = ""
    verb_phrase = ""

    while True:
        if sentence[0] in determiners:
            pass
        elif sentence[0] in quantifiers_distributives:
            pass
        elif sentence[1] in quantifiers_distributives:
            pass
        elif any(sentence[0].endswith(s) for s in adjective_suffixes):
            if any(sentence[1].endswith(s) for s in verb_suffixes):
                noun_phrase += sentence.pop(0) + " "
        elif sentence[0] == "of":
            pass
        else:
            break

        noun_phrase += sentence.pop(0) + " "

    noun_phrase += sentence.pop(0)

    verb_phrase = " ".join(sentence)


    print(noun_phrase, verb_phrase, sep="\n")