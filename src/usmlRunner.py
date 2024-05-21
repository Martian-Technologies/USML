import lookUp
from assembler import Assembler as baseAssembler
from context import Context

class USMLRunner:
    def __init__(self, assembler = None) -> None:
        if assembler == None:
            assembler = baseAssembler()

    def process(self, codeStr:str):
        code = []
        cost = []
        for line in codeStr.splitlines():
            lineData = line.split(" ")
            if lineData[0][0] == ".":
                lineData = [".", lineData[0][1:len(lineData[0])]]
            bestLine = lookUp.getBestCost(lookUp.getName(lineData[0]), lineData[1:len(lineData)])
            cost = bestLine[1]
            code.extend(bestLine[0])
        for line in code:
            print(line)