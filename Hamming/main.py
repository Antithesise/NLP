from math import sqrt, ceil, log
from functools import reduce
from random import randrange
from typing import Union


class Generate():
    def __init__(self, data: list[int]):
        self.correct = data
        self.errors = []
        self.data = data

    def FromStr(data: str):
        return Generate([int(digit) for digit in reduce(lambda x, y: x + y, [bin(charnum).lstrip("0b") for charnum in bytearray(txt, "utf-8")])])

    def CreateErrors(self, errors: int):
        for _ in range(errors):
            index = randrange(len(self.data))

            self.errors += [index]

            self.data[index] += 1
            self.data[index] %= 2

    def group(self, data: list[int], size: int, parities: int=0) -> list[list[int]]:
        assert size >= 4, "size isn't big enough"
        assert all([digit in [0, 1] for digit in data]), "data isn't a list of 1s and 0s"
        assert sqrt(size) == ceil(sqrt(size)), "size isn't a perfect square"

        bits = size - parities # bits not dedicated to error correction
        batches = ceil(len(data) / bits) # maximum number of batches needed to split data into chunks of 'size'
        out: list[list[int]] = []

        for index in range(batches):
            batch: list = []
            if index * bits >= len(data): # if there isn't enough data to create a full batch
                for digit in data[index * bits:len(data)]:
                    batch.append(digit)
                
                batch += [0] * (bits - len(batch)) # pad end with 0s
            else:
                for digit in data[index * bits:(index+1) * bits]:
                    batch.append(digit)
            
            out.append(batch)

        return out

    def parity(self, size: int) -> list[list[int]]:
        parities = 1
        data = self.group(self.data, size, parities) # split data into chunks of size s with p slots in each chunk empty (automatically pads data in last chunk)

        for bnum, batch in enumerate(data):
            data[bnum].insert(0, sum(batch) % 2) # parity is 1 if there is an odd number of 1s, otherwise 0
        
        return data
        

    def hamming(self, size: int) -> list[list[int]]:
        assert (size & (size - 1) == 0) and size != 0, "size isn't a power of 2"

        parities = int(log(size, 2))
        data = self.group(self.data, size, parities + 1) # include parity bit in 0th position

        for bnum, batch in enumerate(data):
            offset = 0

            for index in range(-1, parities): # include parity bit in 0th position
                data[bnum].insert(round(index**2) + offset, 3) # 3 is place holder
                offset += 1

            rows = [batch[index:index+size] for index in range(0, size**2, size)]
            columns = [[]] * size
            
            for index, digit in enumerate(batch):
                columns[index % size].append(digit)

            for pnum in range(parities - 1):
                if pnum > parities/2: # rows
                    pos: int = 2**(pnum - (parities/2))
                    d = 0

                    for r in range(size):
                        if r % pos <= (pos / 2):
                            d += sum(rows[r])

                    data[bnum][2**pnum] = d % 2 # parity is 1 if there is an odd number of 1s, otherwise 0
                else: # columns
                    pos: int = 2**pnum
                    d = 0

                    for c in range(size):
                        if c % pos <= (pos / 2):
                            d += sum(columns[c])

                    data[bnum][pos] = d % 2 # parity is 1 if there is an odd number of 1s, otherwise 0

            data[bnum][0] = sum(batch) % 2 # leave until last
        
        return data

class Check():
    def hamming(data: list[list[int]], size: int) -> dict[int, int]:
        errors = {} # multiple batches means multiple indexes for errors
        for bnum, batch in enumerate(data):
            errors[bnum] = reduce(lambda a, b: a^b, [index for index, digit in enumerate(batch) if digit]) # use xor to get index of incorrect bit

        return errors

    def parity(data: list[list[int]], size: int) -> dict[int, int]:
        errors = {} # multiple batches means multiple indexes for errors
        for bnum, batch in enumerate(data):
            errors[bnum] = sum(batch) % 2 # no index, just 1 or 0

        return errors

def show(data: Union[list[list[int]], list[int]], size: int) -> None:
    assert sqrt(size) == (s := ceil(sqrt(size))), "size isn't a perfect square"    

    try:
        for batch in data:
            for index, item in enumerate(batch):
                print(f"{item} ", end="\n"*(index % s == 3))
        
            print()
    except TypeError:
        for index, item in enumerate(data):
            print(f"{item} ", end="\n"*(index % s == 3))
        
        print("\n")

txt = input("Text: ")
size = 16 # 4x4 grid

print("ERRORLESS:")

d = Generate.FromStr(txt)
show(d.data, size)

show(d.hamming(size), size)
print(Check.hamming(d.hamming(size), size))

show(d.parity(size), size)
print(Check.parity(d.parity(size), size))

print("ERRORS:")

d.CreateErrors(1)
show(d.data, size)

show(d.hamming(size), size)
print(Check.hamming(d.hamming(size), size))

show(d.parity(size), size)
print(Check.parity(d.parity(size), size))