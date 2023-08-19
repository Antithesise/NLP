from os import get_terminal_size
from syntax import Syntax
from lexer import Lexer


if __name__ == "__main__":
    lexer = Lexer(debug=False)
    syntax = Syntax(debug=False)

    with open("tests.txt") as f:
        for l in (tests := f.read().strip().split("\n")):
            phrase, correct = l.split("|")

            try:
                print("\n > ", phrase.strip() + "\n")

                print("\n   ", lexer(phrase), f"({lexer.out.sentenceclass})")
                print("\n   ", syntax(lexer.out))
            except Exception as e:
                print("\n    \x1b[31mError:", e, end="\x1b[0m\n")
                print("    Last state recorded:", lexer.out)

    print(f"\nTesting complete.\n\n{'*' * get_terminal_size().columns}\n\nEntering Interactive Mode. Press Ctrl+C to exit...")

    while True:
        try:
            print("\n   \x1b[33m", syntax(lexer(input("\n >  "))), f"({lexer.out.sentenceclass})\x1b[0m")

        except KeyboardInterrupt:
            print("\x1b[0m\x1b[2K\rExiting...\n")

            break

        except EOFError:
            print("\x1b[0m\x1b[2K\rExiting...\n")

            break

        except Exception as e:
            print("\n    \x1b[31mError:", e, end="\x1b[0m\n")