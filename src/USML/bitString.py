from __future__ import annotations
from copy import copy
import math
from random import randint


class BitString:
    def __init__(self, bitCount:int) -> None:
        self.bits:list[bool] = [False] * bitCount
        self.bitCount = bitCount
    
    def getBit(self, index):
        return self.bits[index]
    
    def setBit(self, index, state:int|bool):
        self.bits[index] = bool(state)

    def getInt(self) -> int:
        num:int = 0
        for i in range(self.bitCount):
            if self.bits[i]:
                num = round(num + math.pow(2, i))
        return num
    
    def setInt(self, num:int) -> None:
        while num < 0:
            num = num + math.pow(2, self.bitCount)
        i = self.bitCount-1
        overFlow = 0
        while i >= 0:
            bitValue = math.pow(2, i)
            if bitValue*2 <= num:
                i += 1
            else:
                if i > self.bitCount-1:
                    num -= bitValue
                    overFlow += bitValue
                elif bitValue > num:
                    self.bits[i] = False
                else:
                    self.bits[i] = True
                    num -= bitValue
                i -= 1
        return overFlow / math.pow(2, self.bitCount)
    
    def maxIntValue(self) -> int:
        return math.pow(2, self.bitCount) - 1

    def randomized(self:int) -> None|BitString:
        """
        if used on a static pass in the bit length
        if used on a instance dont pass anything
        """
        if type(self) != BitString: # static call
            self:BitString = BitString(self)
            for i in range(self.bitCount):
                self.bits[i] = (randint(0, 1) == 0)
            return self
        else:
            for i in range(self.bitCount):
                self.bits[i] = (randint(0, 1) == 0)

    def copy(self):
        return self.__copy__()

    def __str__(self) -> str:
        string = ""
        for bit in self.bits:
            string = ("1" if bit else "0") + string
        string = "[" + string
        string += "]:" + str(self.getInt())
        return string
    
    def __copy__(self) -> BitString:
        newBitString = BitString(len(self.bits))
        newBitString.bits = copy(self.bits)
        return newBitString