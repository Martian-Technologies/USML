from copy import copy as shalowCopy

from USML.instructions.instructionLookUp import ILU
from USML.optimizers.simple.simpleOptimizerGetter import SimpleOptimizerGetter
from assembler import Assembler as baseAssembler
from USML.context import Context


class USMLRunner:
    def __init__(self, assembler = None) -> None:
        if assembler is None:
            assembler = baseAssembler()
        self.assembler:baseAssembler = assembler
        self.bestInstructionSimple:dict[str, tuple[Context, float]] = {}
    
    def process(self, codeStr:str):
        code = Context()
        for line in codeStr.splitlines():
            lineData = line.split(" ")
            if len(lineData) == 0:
                continue
            if lineData[0] == "":
                continue
            if lineData[0][0] == ".":
                lineData = [".", lineData[0][1:len(lineData[0])]]
            for i in range(len(lineData[1:len(lineData)])):
                try:
                    lineData[i + 1] = float(lineData[i + 1])
                except:
                    pass
            con = self.getBestInstructionSimple(ILU.getName(lineData[0]))
            toReplace = []
            i = 1
            for var in lineData[1:len(lineData)]:
                toReplace.append("PARAM" + str(i))
                i += 1
            con.replaceVarNamesWithUniqueNames(dict(zip(toReplace, lineData[1:len(lineData)])))
            code.addContext(con, lineData[1:len(lineData)])
        print("before")
        print(code)
        for optimizer in SimpleOptimizerGetter.simpleOptimizerGetter.getOptimizer():
            code = optimizer.run(code)
        print("after")
        print(code)
        return code

    def getBestInstructionSimple(self, instructionName:str, instructionNotToUse:list|None = None) -> Context|None:
        instructionNotToUse = shalowCopy(instructionNotToUse)
        # already hashed the instruction
        if instructionName in self.bestInstructionSimple:
            if self.bestInstructionSimple[instructionName] is None:
                raise Exception("cant find implimation for {instructionName}")
            return self.bestInstructionSimple[instructionName]
        # find best instruction simple
        if instructionNotToUse is None:
            isMain = True
            instructionNotToUse = [instructionName]
        else:
            isMain = False
            if instructionName in instructionNotToUse:
                return None
            instructionNotToUse.append(instructionName)
        best:Context|None = None
        for implimation in ILU.getClass_Name(instructionName).getImplementations():
            if len(implimation) == 1 and ILU.getName(implimation[0][0]) == instructionName:
                if self.assembler.hasInstruction(instructionName):
                    con = Context()
                    con.addCommand(implimation[0], self.assembler.getSimpleCost(instructionName))
                    if best is None:
                        best = con
                    elif con.getCost() <= best.getCost():
                        best = con
            else:
                con = Context()
                for line in implimation:
                    if line[0][0] == ".":
                        line = [".", line[0][1:len(line[0])]]
                    conLine = self.getBestInstructionSimple(ILU.getName(line[0]), instructionNotToUse)
                    if conLine is None:
                        con = None
                        break
                    toReplace = []
                    i = 1
                    for var in line[1:len(line)]:
                        toReplace.append("PARAM" + str(i))
                        i += 1
                    conLine.replaceVarNamesWithUniqueNames(dict(zip(toReplace, line[1:len(line)])))
                    con.addContext(conLine, line[1:len(line)])
                if con is not None:
                    if best is None:
                        best = con
                    elif con.getCost() < best.getCost():
                        best = con
        if best is None and isMain:
            raise Exception("cant find implimation for {instructionName}")
        return best