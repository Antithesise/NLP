from re import split


pronouns = [
    "all",
    "any",
    "anybody",
    "anyone",
    "anything",
    "both",
    "each other",
    "each",
    "either",
    "enough",
    "everybody",
    "everyone",
    "everything",
    "few",
    "he",
    "herself",
    "him",
    "himself",
    "I",
    "it",
    "itself",
    "many",
    "me",
    "mine",
    "most",
    "myself",
    "naught",
    "neither",
    "no one",
    "nobody",
    "none",
    "nothing",
    "nought",
    "one another",
    "one",
    "others",
    "ought",
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
    "yours",
    "yourself",
    "yourselves"
]

pronouns2 = [
    "another",
    "her",
    "his",
    "its",
    "my",
    "other",
    "our",
    "their",
    "thy",
    "your",
]


while True:
    sentence = [w for w in split(r" |('[a-z]+)", input("> ").lower()) if w]
    subj = ""
    verb = ""
    obj = ""

    subj = sentence.pop(0)

    if subj in pronouns2 and sentence[0] != "'s":
        subj += " " + sentence.pop(0)

    while sentence[0] == "'s":
        subj += sentence.pop(0) + " " + sentence.pop(0)

    verb = sentence.pop(0)

    obj = " ".join(sentence)


    print(subj, verb, obj, sep="\n")