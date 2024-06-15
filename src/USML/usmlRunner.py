from USML.lookUp import LookUp
from assembler import Assembler as baseAssembler
from USML.context import Context
from copy import copy as shalowCopy

class USMLRunner:
    def __init__(self, assembler = None) -> None:
        if assembler == None:
            assembler = baseAssembler()
        self.assembler:baseAssembler = assembler
        self.lookup:LookUp = LookUp()
        self.bestInstructionSimple:dict[str, tuple[Context, float]] = {}
    
    def process(self, codeStr:str):
        code = Context()
        for line in codeStr.splitlines():
            lineData = line.split(" ")
            if lineData[0][0] == ".":
                lineData = [".", lineData[0][1:len(lineData[0])]]
            for i in range(len(lineData[1:len(lineData)])):
                try:
                    lineData[i + 1] = float(lineData[i + 1])
                except:
                    pass
            con = self.getBestInstructionSimple(self.lookup.getName(lineData[0]))
            toReplace = []
            i = 1
            for var in lineData[1:len(lineData)]:
                toReplace.append("PARAM" + str(i))
                i += 1
            con.replaceVarNamesWithUniqueNames(dict(zip(toReplace, lineData[1:len(lineData)])))
            code.addContext(con, lineData[1:len(lineData)])
        return code

    def getBestInstructionSimple(self, instructionName:str, instructionNotToUse:list|None = None) -> Context|None:
        instructionNotToUse = shalowCopy(instructionNotToUse)
        # already hashed the instruction
        if instructionName in self.bestInstructionSimple:
            if self.bestInstructionSimple[instructionName] == None:
                raise Exception("cant find implimation for {instructionName}")
            return self.bestInstructionSimple[instructionName]
        # find best instruction simple
        if instructionNotToUse == None:
            isMain = True
            instructionNotToUse = [instructionName]
        else:
            isMain = False
            if instructionName in instructionNotToUse:
                return None
            instructionNotToUse.append(instructionName)
        best:Context|None = None
        for implimation in self.lookup.getClass(instructionName).getImplementations():
            if len(implimation) == 1 and self.lookup.getName(implimation[0][0]) == instructionName:
                if self.assembler.hasInstruction(instructionName):
                    con = Context()
                    con.addCommand(implimation[0], self.assembler.getSimpleCost(instructionName))
                    if best == None:
                        best = con
                    elif con.getCost() <= best.getCost():
                        best = con
            else:
                con = Context()
                for line in implimation:
                    if line[0][0] == ".":
                        line = [".", line[0][1:len(line[0])]]
                    conLine = self.getBestInstructionSimple(self.lookup.getName(line[0]), instructionNotToUse)
                    if conLine == None:
                        con = None
                        break
                    toReplace = []
                    i = 1
                    for var in line[1:len(line)]:
                        toReplace.append("PARAM" + str(i))
                        i += 1
                    conLine.replaceVarNamesWithUniqueNames(dict(zip(toReplace, line[1:len(line)])))
                    con.addContext(conLine, line[1:len(line)])
                if con != None:
                    if best == None:
                        best = con
                    elif con.getCost() < best.getCost():
                        best = con
        if best == None and isMain:
            raise Exception("cant find implimation for {instructionName}")
        return best