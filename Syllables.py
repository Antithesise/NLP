from hyph_pat import custom as patterns
from re import subn, sub as replace, Match


global pos
pos = []
text = "Computer algorithm hyphenation concatenation mathematics typesetting program supercalifragilisticexpialidocious"
output = ""

def process(m: Match, sub: str):
    global pos

    i = -1
    for n in sub:  
        if n.isdigit():
            pos[i + m.start()] = max(pos[i + m.start()], int(n))
        else:
            i += 1

    return sub


for word in text.split():
    pos = [0 for i in word]

    for p, res in patterns.items():
        pat = replace(r"\*", lambda x: "(?<!\\A)" if x.start() == 0 else "(?!\\Z)", replace(r"\!", lambda x: "(?<=\\A)" if x.start() == 0 else "(?=\\Z)", p))
        
        x = subn(pat, lambda x: process(x, res), word.lower())[0]

        if x != word.lower():
            print(f"{p}\r\x1b[8C{res}")

    pos[-1] = 0
    output += (out := "".join([f"{w}{'-' * (n % 2)}" for w, n in zip(word, pos)])) + " "
    print("".join([f"{l}{n or ''}" for l, n in zip(word, pos)]), f"\t{out}\n")

print()

output = output.strip()

print(output)
