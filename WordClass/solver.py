from ast import operator
from regex import findall, match, sub
from typing import Optional, Union
from math import e, factorial, pi


class ALPHANUM(str):
    @property
    def isknown(self) -> bool:
        try:
            float(self)
            return True
        except ValueError:
            return False

    @property
    def ispositive(self) -> bool:
        return not self.startswith("-")

    def contains(self, alphanum: "ALPHANUM") -> bool:
        return alphanum == self

    def __repr__(self) -> str:
        return self

class OPERATION:
    operator = ""
    isknown = False

    def __init__(self, operator: str, operands: list[Union["OPERATION", ALPHANUM]]) -> None:
        self.operator = operator
        self.operands = operands

    @property
    def inverse(self) -> Optional[str]:
        return {"+": "-", "-": "+", "*": "/", "/": "*", "^": "\\", "\\": "^"}.get(self.operator)

    @property
    def ispositive(self) -> bool:
        if self.operator == "^":
            return self.operands[0].ispositive or self.operands[1] % 2
        elif self.operator == "\\":
            return self.operands[1].ispositive
        elif self.operator == "!":
            return self.operands[0].ispositive
        else:
            return self.operands[0]

    def contains(self, alphanum: ALPHANUM) -> bool:
        for x in self.operands:
            if isinstance(x, OPERATION):
                if x.contains(alphanum):
                    return True
            elif x == alphanum:
                return True
        
        return False

    def invert(self) -> None:
        self.operator = (self.inverse or self.operator)
    
    def apply(self, op1: ALPHANUM, op2: Optional[ALPHANUM]=None) -> ALPHANUM:
        op1 = float(op1)
        
        if self.operator == "!":
            op1 = factorial(op1)
        elif op2:
            op2 = float(op2)

            if self.operator == "+":
                op1 += op2
            elif self.operator == "-":
                op1 -= op2
            elif self.operator == "*":
                op1 *= op2
            elif self.operator == "/":
                op1 /= op2
            elif self.operator == "^":
                op1 **= op2
            elif self.operator == "\\":
                op1 = op2 ** (1 / op1) 
        
        op1 = (int if float(op1).is_integer() else float)(float(op1))

        return ALPHANUM(op1)
        
    
    def __repr__(self) -> str:
        return f"({self.operator.join([repr(o) for o in self.operands])}{'!' * (self.operator == '!')})"

class EXPR:
    precedence = {"+" : 0, "-" : 0, "*" : 1, "/" : 1, "\\": 2, "!": 3, "^": 4}

    def __init__(self, expr: str) -> None:
        self.expr = self.parse("".join(expr.split()))

    def __repr__(self) -> str:
        return repr(self.expr).removeprefix("(").removesuffix(")")

    def contains(self, alphanum: ALPHANUM) -> bool:
        return self.expr.contains(alphanum)

    def parse(self, expr: str) -> OPERATION | ALPHANUM:
        tokens: list[str] = findall(r"[\+\*\/\!\^\(\)a-zA-Z]|(?:(?<=^|[\+\-\*\/\^])\-)?(?:π|\d+(?:\.\d+)?)|\-", sub(r"\-\-|\+\+", r"\+", sub(r"^\+|\+(\-)|([\-\*\/\^])\+", r"\1", sub(r"([a-zA-Zπ0-9\)])(?=[a-zA-Zπ\(])", r"\1*", expr))))
        operators = []
        values = []
        parens = 0

        subparse = ""

        for t in tokens:
            if t == ")":
                parens -= 1

                if parens == 0:
                    values.append(self.parse(subparse))

                    subparse = ""

            if parens:
                subparse += t
            elif match(r"[a-zA-Zπ]|[\+\-]?\d+", t):
                sign = t.startswith("-") * -2 + 1

                if "π" in t:
                    values.append(ALPHANUM(pi * sign))
                elif "e" in t:
                    values.append(ALPHANUM(e * sign))
                else:
                    values.append(ALPHANUM(t))
            elif t not in "()":
                while operators:
                    if self.precedence.get(operators[-1]) < self.precedence[t]:
                        break

                    if operators[-1] == "!":
                        values.append(OPERATION(operators.pop(), [values.pop()]))
                    else:
                        x = values.pop()

                        values.append(OPERATION(operators.pop(), [values.pop(), x]))

                operators.append(t)
        
            if t == "(":
                parens += 1

        while operators:
            if operators[-1] == "!":
                values.append(OPERATION(operators.pop(), [values.pop()]))
            else:
                x = values.pop()

                values.append(OPERATION(operators.pop(), [values.pop(), x]))

        return values[0]

    def simplify(self, op: OPERATION | ALPHANUM) -> OPERATION | ALPHANUM:
        if isinstance(op, ALPHANUM):
            return op

        op.operands = [self.simplify(o) for o in op.operands]

        modifyable = [o for o in op.operands if o.isknown]
        simplified = [o for o in op.operands if o not in modifyable]

        if modifyable:
            simplified.append(op.apply(modifyable.pop(0)))

        while modifyable:
            simplified[-1] = op.apply(simplified[-1], modifyable.pop(0))

        if len(simplified) > 1 or op.operator == "!":
            if op.operator == "+":
                simplified.sort(key=lambda x: isinstance(x, OPERATION) - x.isknown, reverse=True)
            elif op.operator == "*":
                simplified.sort(key=lambda x: isinstance(x, ALPHANUM) + x.isknown, reverse=True)
            else:
                simplified.sort(key=lambda x: op.operands.index(x if x in op.operands else None))

            # if simplified[0].ispositive

            return OPERATION(op.operator, simplified)
        else:
            return simplified[-1]

class EQUATION:
    def __init__(self, equation: str) -> None:
        subject, solution = equation.split("=")

        self.subject = EXPR(subject)
        self.solution = EXPR(solution)
    
    def simplify(self) -> None:
        self.subject.expr = self.subject.simplify(self.subject.expr)
        self.solution.expr = self.solution.simplify(self.solution.expr)

        if self.solution.contains(ALPHANUM("y")) and not self.subject.contains(ALPHANUM("y")):
            self.subject, self.solution = self.solution, self.subject
        
        # if self.subject.contains(ALPHANUM("y")):
        #     while True:
        #         if isinstance(self.subject.expr, ALPHANUM):
        #             break
        #         elif self.subject.expr.operator == "!" or all([o.contains("y") for o in self.subject.expr.operands]):
        #             break



class Solver:
    def __call__(self, equation: str) -> str:
        self.equation = EQUATION(equation)

        return repr(self.solve(self.equation).solution)  

    def solve(self, equation: EQUATION) -> EQUATION:
        self.equation.simplify()

        return equation


if __name__ == "__main__":
    solve = Solver()

    print("\nRunning tests...")

    with open("testssolver.txt", encoding="utf-8") as f:
        incorrect = 0

        for l in (tests := f.read().strip().split("\n")):
            equation, correct = l.split("|")

            try:
                print("\n > ", equation.strip())

                answer = solve(equation)

                print(f"\n    \x1b[3{(answer == correct.strip()) + 1}m" + f"{answer}\x1b[0m")

                incorrect += answer != correct.strip()
            except EOFError as e:
                print("\n    \x1b[31mError:", e, end="\x1b[0m\n")

                incorrect += 1

    print(f"\nTesting complete: {len(tests) - incorrect}/{len(tests)} correct.\n\n{'*' * 145}\n\nEntering Interactive Mode. Press Ctrl+C to exit...")

    while True:
        try:
            print("\n   \x1b[33m" + solve(input("\n >  ")) + "\x1b[0m")

        except KeyboardInterrupt:
            print("\x1b[0m\x1b[2K\rExiting...\n")

            break

        except EOFError:
            print("\x1b[0m\x1b[2K\rExiting...\n")

            break

        except Exception as e:
            print("\n    \x1b[31mError:", e, end="\x1b[0m\n")
            print("    Last state recorded:", solve.out)