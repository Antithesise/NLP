from typing import NoReturn
from sys import exit
from CLI import CLI


cmdln = CLI()


@cmdln.add_cmd
def echo(*text: str, sep: str=" ", end: str="\n", flush: bool=False) -> None:
    print(*text, sep=sep, end=end, flush=flush)

@cmdln.add_cmd
def quit(status: object=0) -> NoReturn:
    if str(status).isdigit():
        exit(int(status))
    else:
        exit(status)

@cmdln.add_cmd
def hello(name: str="") -> None:
    if name:
        print(f"Hello {name}!")
    else:
        print("Hello!")

@cmdln.add_cmd
def add(num1: str, num2: str) -> None:
    print(int(num1) + int(num2))

@cmdln.add_cmd
def sub(num1: str, num2: str) -> None:
    print(int(num1) - int(num2))

@cmdln.add_cmd
def cat(*text) -> None:
    print(*text)

@cmdln.setup(1)
def message() -> None:
    print("My CLI v1.0")


cmdln(
    # flags={"method": "w-f"}
)
