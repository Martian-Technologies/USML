from __future__ import annotations
from typing import Literal
from copy import deepcopy


class Memory:
    def __init__(self, sizes:list[int]) -> None:
        self.mem:list[list[None|str]] = []
        for size in sizes:
            self.mem.append([None] * size)

    def read(self, address:MemoryPos) -> str|Literal[False]|None:
        if len(self.mem) > address.memIndex:
            if len(self.mem[address.memIndex]) > address.memAddress:
                return self.mem[address.memIndex][address.memAddress]
        return False
    
    def write(self, address:MemoryPos, varName:str) -> str|Literal[False]|None:
        if len(self.mem) > address.memIndex:
            if len(self.mem[address.memIndex]) > address.memAddress:
                atAddress = self.mem[address.memIndex][address.memAddress]
                self.mem[address.memIndex][address.memAddress] = varName
                return atAddress
        return False
    
    def getAddressesOfVar(self, varName) -> list[MemoryPos]:
        addresses = []
        for memIndex in range(len(self.mem)):
            for memAddress in range(len(self.mem[memIndex])):
                if self.mem[memIndex][memAddress] == varName:
                    addresses.append(MemoryPos(memIndex, memAddress))
        return addresses
    
    def copy(self) -> Memory:
        return self.__copy__()

    def __getitem__(self, index:int|MemoryPos) -> str|list[None|str]|Literal[False]|None:
        if type(index) == MemoryPos:
            return self.read(index)
        if len(self.mem) > index:
            return self.mem[index]
        return False
    
    def __setitem__(self, index:MemoryPos, item) -> str|Literal[False]|None:
        return self.write(index, item)

    def __len__(self) -> int:
        return len(self.mem)
    
    def __str__(self) -> str:
        return str(self.mem)
    
    def __format__(self, format_spec) -> str:
        return str(self)
    
    def __repr__(self) -> str:
        return str(self)
    
    def __copy__(self) -> Memory:
        newMem = Memory([])
        newMem.mem = deepcopy(self.mem)
        return newMem
    
    def __iter__(self):
        return iter(self.mem)

class MemoryPos:
    def __init__(self, memIndex:int, memAddress:int) -> None:
        self.memIndex:int = memIndex
        self.memAddress:int = memAddress

    def __str__(self) -> str:
        return f"pos [{self.memIndex}, {self.memAddress}]"
    
    def __format__(self, format_spec) -> str:
        return str(self)
    
    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other) -> bool:
        if type(other) == MemoryPos:
            return self.memIndex == other.memIndex and self.memAddress == other.memAddress
        return False
