__all__ = [
    "uk", "ukfull", "us", "us1", "us2", "usmax", "custom"
]


def parse(name: str):
    with open(f"hyph_pat/{name}.txt") as f:
        return {
            "".join([
                l for l in p if not l.isdigit()
            ]): p.strip("*") for p in f.read().replace(".", "*").splitlines()
        }


uk = parse("ukhyph")
ukfull = parse("ukhyphen")
us = parse("ushyph")
us1 = parse("ushyph1")
us2 = parse("ushyph2")
usmax = parse("ushyphmax")
custom = parse("hyph")

del parse