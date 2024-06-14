import lookUp
from assembler import Assembler as baseAssembler
from context import Context

class USMLRunner:
    def __init__(self, assembler = None) -> None:
        if assembler == None:
            assembler = baseAssembler()

    def process(self, codeStr:str):
        code = Context()
        cost = []
        for line in codeStr.splitlines():
            lineData = line.split(" ")
            if lineData[0][0] == ".":
                lineData = [".", lineData[0][1:len(lineData[0])]]
            code.addCommand(lineData)
        print(code)
