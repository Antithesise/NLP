from typing import NoReturn
from sys import exit
from CLI import CLI

cmdln = CLI()

@cmdln.add_cmd
def echo(*text: str, sep: str=" ", end: str="\n") -> None:
    print(*text, sep=sep, end=end)

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

cmdln()
