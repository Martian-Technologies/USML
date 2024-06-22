from __future__ import annotations
from typing import Literal
from copy import deepcopy


class Memory:
    def __init__(self, ramSizes:list[int], regSizes:list[int]) -> None:
        self.ram:list[list[None|str]] = []
        self.ramMapping:dict[str, MemoryPos] = {}
        self.regs:list[list[None|str]] = []
        for size in ramSizes:
            self.ram.append([None] * size)
        for size in regSizes:
            self.regs.append([None] * size)

    def read(self, address:MemoryPos) -> str|Literal[False]|None:
        if address.ramOrReg == "ram":
            if len(self.ram) > address.memIndex:
                if len(self.ram[address.memIndex]) > address.memAddress:
                    return self.ram[address.memIndex][address.memAddress]
        elif address.ramOrReg == "reg":
            if len(self.regs) > address.memIndex:
                if len(self.regs[address.memIndex]) > address.memAddress:
                    return self.regs[address.memIndex][address.memAddress]
        return False
    
    def write(self, address:MemoryPos, varName:str) -> str|Literal[False]|None:
        if address.ramOrReg in ["ram", "reg"]:
            if len(self[address.ramOrReg]) > address.memIndex:
                if len(self[address.ramOrReg][address.memIndex]) > address.memAddress:
                    atAddress = self[address.ramOrReg][address.memIndex][address.memAddress]
                    self[address.ramOrReg][address.memIndex][address.memAddress] = varName
                    return atAddress
        return False
    
    def setMappingForVar(self, varName:str, pos:MemoryPos) -> None:
        self.ramMapping[varName] = pos

    def getMappingForVar(self, varName:str) -> MemoryPos|None:
        if varName in self.ramMapping:
            return self.ramMapping[varName]
        return None

    def getVarMappedToPos(self, pos:MemoryPos):
        for var in self.ramMapping:
            if pos == self.ramMapping[var]:
                return var
        return None

    def clearUnmapped(self):
        for memName in ["ram", "reg"]:
            for memIndex in range(len(self[memName])):
                for memAddress in range(len(self[memName][memIndex])):
                    pos = MemoryPos(memName, memIndex, memAddress)
                    if pos not in self.ramMapping.values():
                        self[pos] = None
        
    def getAddressesOfVar(self, varName) -> list[MemoryPos]:
        addresses = []
        for memName in ["ram", "reg"]:
            for memIndex in range(len(self[memName])):
                for memAddress in range(len(self[memName][memIndex])):
                    if self[memName][memIndex][memAddress] == varName:
                        addresses.append(MemoryPos(memName, memIndex, memAddress))
        return addresses
    
    def getMemoryAddressesFromData(self, data) -> list[MemoryPos]:
        if type(data) == str:
            data = [data]
        positions:list[MemoryPos] = []
        for pos in data:
            foundPositionsForPos = False
            if type(pos) == list:
                if len(pos) == 1:
                    pos = pos[0]
                elif len(pos) == 2:
                    for memAddress in range(len(self[pos[0]][pos[1]])):
                        positions.append(MemoryPos(pos[0], pos[1], memAddress))
                        foundPositionsForPos = True
                elif len(pos) == 3:
                    positions.append(MemoryPos(pos[0], pos[1], pos[2]))
                    foundPositionsForPos = True
            if type(pos) == str:
                if pos == "reg" or pos == "all":
                    for memIndex in range(len(self.regs)):
                        for memAddress in range(len(self.regs[memIndex])):
                            positions.append(MemoryPos("reg", memIndex, memAddress))
                            foundPositionsForPos = True
                if pos == "ram" or pos == "all":
                    for memIndex in range(len(self.ram)):
                        for memAddress in range(len(self.ram[memIndex])):
                            positions.append(MemoryPos("ram", memIndex, memAddress))
                            foundPositionsForPos = True
            if not foundPositionsForPos:
                raise Exception(f"could not make positions from data {pos} for data {data}")
        return positions

    def copy(self) -> Memory:
        return self.__copy__()

    def __getitem__(self, index:int|MemoryPos) -> str|list[None|str]|Literal[False]|None:
        if type(index) == MemoryPos:
            return self.read(index)
        if index == "ram":
            return self.ram
        if index == "reg":
            return self.regs
        return False
    
    def __setitem__(self, index:MemoryPos, item) -> str|Literal[False]|None:
        return self.write(index, item)

    def __str__(self) -> str:
        return f"ram: {self.ram}, regs: {self.regs}"
    
    def __format__(self, format_spec) -> str:
        return str(self)
    
    def __repr__(self) -> str:
        return str(self)
    
    def __copy__(self) -> Memory:
        newMem = Memory([], [])
        newMem.ram = deepcopy(self.ram)
        newMem.regs = deepcopy(self.regs)
        newMem.ramMapping = deepcopy(self.ramMapping)
        return newMem
    
    def __iter__(self):
        return iter(self.mem)

class MemoryPos:
    def __init__(self, ramOrReg:str ,memIndex:int, memAddress:int) -> None:
        self.ramOrReg = ramOrReg
        self.memIndex:int = memIndex
        self.memAddress:int = memAddress

    def __str__(self) -> str:
        return f"pos [{self.ramOrReg}, {self.memIndex}, {self.memAddress}]"
    
    def __format__(self, format_spec) -> str:
        return str(self)
    
    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other) -> bool:
        if type(other) == MemoryPos:
            return self.ramOrReg == other.ramOrReg and self.memIndex == other.memIndex and self.memAddress == other.memAddress
        return False
