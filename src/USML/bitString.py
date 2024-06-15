from __future__ import annotations
from copy import copy
import math
from random import randint


class BitString:
    def __init__(self, bitCount:int) -> None:
        self.bits:list[bool] = [False] * bitCount
    
    def getInt(self) -> int:
        num:int = 0
        for i in range(len(self.bits)):
            if self.bits[i]:
                num = round(num + math.pow(2, i))
        return num
    
    def setInt(self, num:int) -> None:
        if num < 0:
            num = math.pow(2, len(self.bits)) - num
        for i in range(len(self.bits)-1, -1, -1):
            bitValue = math.pow(2, i)
            if bitValue > num:
                self.bits[i] = False
            else:
                self.bits[i] = True
                num -= bitValue
    
    def maxIntValue(self) -> int:
        return math.pow(2, len(self.bits)) - 1

    def randomized(self:int) -> None|BitString:
        """
        if used on a static pass in the bit length
        if used on a instance dont pass anything
        """
        if type(self) != BitString: # static call
            self:BitString = BitString(self)
            for i in range(len(self.bits)):
                self.bits[i] = (randint(0, 1) == 0)
            return self
        else:
            for i in range(len(self.bits)):
                self.bits[i] = (randint(0, 1) == 0)

    def copy(self):
        return self.__copy__()

    def __str__(self) -> str:
        string = "["
        for bit in self.bits:
            string += "1" if bit else "0"
        string += "]:" + str(self.getInt())
        return string
    
    def __copy__(self) -> BitString:
        newBitString = BitString(len(self.bits))
        newBitString.bits = copy(self.bits)