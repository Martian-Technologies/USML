from __future__ import annotations
import json

from USML.contextDataGetter import ContextDataGetter
from USML.instructions.instructionLookUp import ILU
from USML.baseAssembler import Assembler
from USML.context import Context

from simpleAssembler.memory import Memory, MemoryPos


class SimpleAssembler(Assembler):
    with open("src/simpleAssembler/Costs.json") as f:
        simpleCosts:dict[str, float] = json.load(f)
    with open("src/simpleAssembler/HasInstruction.json") as f:
        instructionsToUse:dict[str, bool] = json.load(f)
    with open("src/simpleAssembler/InstructionReadAndWritePos.json") as f:
        readAndWritePos:dict[str, list[str|list[str|None]|None]] = json.load(f)
    with open("src/simpleAssembler/Setting.json") as f:
        settings:dict[str] = json.load(f)

    @staticmethod
    def hasInstruction(instructionName):
        if instructionName in SimpleAssembler.instructionsToUse:
            return SimpleAssembler.instructionsToUse[instructionName]
        return False
    
    @staticmethod
    def getSimpleCost(instructionName):
        if instructionName in SimpleAssembler.simpleCosts:
            return SimpleAssembler.simpleCosts[instructionName]
        raise Exception(f"cant get cost for none implemented instruction {instructionName}")
    
    @staticmethod
    def assemble(context:Context) -> Context:
        context = context.copy()
        if "program stop" not in ILU.getTags_Mnemonic(context.getCommand(len(context) - 1)[0]):
            context.addCommand(("HLT", []))
        dataGetter = ContextDataGetter(context)
        dataSetter = MakeDataToAddOrChange(context)
        getVarAndLabelUsage = dataGetter.getVarAndLabelUsage()
        allMem:dict[int, Memory] = {}
        mem = Memory(SimpleAssembler.settings["ramSizes"], SimpleAssembler.settings["regSizes"])
        nextLineNumber = 0
        totalLineCount = len(context)
        toDoJumps:list[tuple[int, int]] = []
        keepGoing = True
        while keepGoing:
            lineNumber = nextLineNumber
            line = context.getCommand(lineNumber)
            SimpleAssembler.doMemoryMannagement(mem, context, dataGetter, dataSetter, lineNumber)
            allMem[lineNumber] = mem.copy()
            tags = ILU.getTags_Mnemonic(line[0])
            if context.getCommand(lineNumber)[0] == ".":
                mem.clearUnmapped()
                nextLineNumber += 1
            elif "force jump" in tags:
                labelData = getVarAndLabelUsage[line[1][0]]
                for usage in labelData["usage"]:
                    if usage["usageType"] == "out":
                        nextLineNumber = usage["line"]
                if nextLineNumber is None:
                    raise Exception(f"Label {line[1][0]} in {line[0]} on line {lineNumber} is not defined.")
                mem.clearRegs()
            elif "maybe jump" in tags:
                labelData = getVarAndLabelUsage[line[1][0]]
                for usage in labelData["usage"]:
                    if usage["usageType"] == "out":
                        jumpLoc = usage["line"]
                if jumpLoc is None:
                    raise Exception(f"Label {line[1][0]} in {line[0]} on line {lineNumber} is not defined.")
                toDoJumps.append((lineNumber, jumpLoc))
                nextLineNumber += 1
            else:
                nextLineNumber += 1
            while (
                    ("program stop" in ILU.getTags_Mnemonic(context.getCommand(lineNumber)[0])) or
                    (nextLineNumber >= totalLineCount) or
                    (nextLineNumber in allMem)
                ):
                if len(toDoJumps) == 0:
                    keepGoing = False
                    break
                jump = toDoJumps.pop()
                nextLineNumber = jump[1]
                if nextLineNumber in allMem:
                    continue
                mem = allMem[jump[0]].copy()
                mem.clearUnmapped()
        return dataSetter.applyCommands()
            
    @staticmethod
    def doMemoryMannagement(mem:Memory, context:Context, dataGetter:ContextDataGetter, dataSetter:MakeDataToAddOrChange, lineNumber:int) -> tuple[tuple[str, list[str]], list[tuple[str, MemoryPos]]]:
        line = context.getCommand(lineNumber)
        commandDataTypes:list[str] = ILU.getExpectedDataType_Mnemonic(line[0])
        commandUsageTypes:list[str] = ILU.getUsageTypes_Mnemonic(line[0])
        # do data in for command
        positionsUsedForInputs:list[MemoryPos] = []
        for paramIndex in range(len(line[1])):
            if commandDataTypes[paramIndex] != "var": # make sure the data type is a var
                continue
            if commandUsageTypes[paramIndex] in ["in", "both"]:
                # get the var's name
                varName = line[1][paramIndex]
                # get the current positions or the var
                positionsOfVar = mem.getAddressesOfVar(varName)
                if len(positionsOfVar) == 0:
                    raise Exception(f"can not used undefined var {varName} on line {lineNumber}")
                # get places it could go
                positions = SimpleAssembler.getReadWritePositions(line[0], paramIndex, mem)
                for pos in positionsUsedForInputs:
                    positions.remove(pos)
                if len(positions) == 0:
                    raise Exception(f"error not enough positions left for var {varName} in line {lineNumber}")
                # get the best pos pair
                bestPos = None
                bestCost = 1000 # bigger than max cost
                for varPos in positionsOfVar:
                    for pos in positions:
                        cost = SimpleAssembler.getMemSlotUsageCost(mem, varPos, pos, lineNumber, dataGetter, varName)
                        if cost is not None and cost < bestCost:
                            bestPos = (varPos, pos)
                            bestCost = cost
                if bestCost is None:
                    raise Exception(f"error not enough positions left for var {varName} in line {lineNumber}")
                # set data
                positionsUsedForInputs.append(bestPos[1])
                if bestPos[0] != bestPos[1]:
                    dataSetter.addCommandBeforeLine(lineNumber, ("MOVE", [bestPos[0], bestPos[1]]))
                dataSetter.addParamChange(lineNumber, paramIndex, bestPos[1])
        # do data out for command
        positionsUsedForOutputs:list[MemoryPos] = []
        varsThatAreOutputs:list[str] = []
        for paramIndex in range(len(line[1])):
            if commandDataTypes[paramIndex] != "var": # make sure the data type is a var
                continue
            if commandUsageTypes[paramIndex] in ["out", "both"]:
                # get the var's name
                varName = line[1][paramIndex]
                # get places it could go
                positions = SimpleAssembler.getReadWritePositions(line[0], paramIndex, mem)
                for pos in positionsUsedForOutputs:
                    positions.remove(pos)
                if len(positions) == 0:
                    raise Exception(f"error not enough positions left for var {varName} in line {lineNumber}")
                # get the best pos
                bestPos = None
                bestCost = 1000 # bigger than max cost
                for pos in positions:
                    cost = None
                    if mem[pos] == varName:
                        cost = 0
                    else:
                        cost = SimpleAssembler.getMemSlotUsageCost(mem, None, pos, lineNumber, dataGetter, varName)
                    if cost is not None and cost < bestCost:
                        bestPos = pos
                        bestCost = cost
                if bestPos is None:
                    raise Exception(f"error not enough positions left for var {varName} in line {lineNumber}")
                positionsUsedForOutputs.append(bestPos)
                varsThatAreOutputs.append(varName)
                dataSetter.addParamChange(lineNumber, paramIndex, bestPos)
                memTMP = mem.copy()
                for command in dataSetter.getCommandsToAddBeforeLineAtLine(lineNumber):
                    if command[0] == "MOVE":
                        memTMP[command[1][1]] = memTMP[command[1][0]]
                for i in range(len(positionsUsedForOutputs)):
                    varName = varsThatAreOutputs[i]
                    for pos in memTMP.getAddressesOfVar(varName):
                        memTMP[pos] = None
                    memTMP[positionsUsedForOutputs[i]] = varName
                for command in dataSetter.getCommandsToAddAfterLineAtLine(lineNumber):
                    if command[0] == "MOVE":
                        memTMP[command[1][1]] = memTMP[command[1][0]]
                savePos = SimpleAssembler.getBestSpotForVarInRam(varName, memTMP, lineNumber, dataGetter)
                mem.setMappingForVar(varName, savePos)
                if savePos != bestPos:
                    dataSetter.addCommandAfterLine(lineNumber, ("MOVE", [bestPos, savePos]))
        # update memory for the next line
        for command in dataSetter.getCommandsToAddBeforeLineAtLine(lineNumber):
            if command[0] == "MOVE":
                mem[command[1][1]] = mem[command[1][0]]
        for i in range(len(positionsUsedForOutputs)):
            varName = varsThatAreOutputs[i]
            for pos in mem.getAddressesOfVar(varName):
                mem[pos] = None
            mem[positionsUsedForOutputs[i]] = varName
        for command in dataSetter.getCommandsToAddAfterLineAtLine(lineNumber):
            if command[0] == "MOVE":
                mem[command[1][1]] = mem[command[1][0]]
        
    @staticmethod
    def getMemSlotUsageCost(mem:Memory, fromPos:MemoryPos|None, toPos:MemoryPos, lineNumber:int, dataGetter:ContextDataGetter, varName:str) -> float|None:
        # if the data does not have to move it is free
        if fromPos == toPos:
            return 0
        # get the next time the var is used
        nextUsed = dataGetter.varNextUsed(mem[toPos], lineNumber)
        # if the pos you are writing to is not used it is cheep
        if (mem[toPos] is None) or (nextUsed is None):
            # if the var is not yet mapped put it in ram so that it does not need to move
            if mem.getMappingForVar(varName) == None:
                if toPos.ramOrReg == "ram":
                    return 3
            return 5
        # get cost of overwriting needed data
        # how long till the next time which the data is used (exulding usage pos and this line)
        overwriteCost = max((100 - nextUsed["steps"])/20, 0) # 100 / 20 = 5 so max value added is 5
        # if the data is used at this line and the data is in the correct place
        line = dataGetter.context.getCommand(lineNumber)
        usageTypes = ILU.getUsageTypes_Mnemonic(line[0])
        for i in range(len(line[1])):
            if usageTypes[i] == "in":
                if mem[toPos] == line[1][i]:
                    if toPos in SimpleAssembler.getReadWritePositions(line[0], i, mem):
                        overwriteCost += 10
                        break
        # if the pos you are writing to is only a reg it is slightly less cheep
        if (toPos.ramOrReg == "reg"):
            return 6 + overwriteCost
        # check if you can even do the movement
        if SimpleAssembler.canOverwriteMemoryPos(mem, toPos, lineNumber, dataGetter):
            return 10 + overwriteCost
        # if you can't overwrite the pos. Don't!
        return None

    @staticmethod
    def canOverwriteMemoryPos(mem:Memory, pos:MemoryPos|None, lineNumber:int, dataGetter:ContextDataGetter):
        # you can overwrite reg data
        if pos.ramOrReg == "reg":
            return True
        # is the pos is not used not used you can overwrite it
        if (mem[pos] is None) or (dataGetter.varNextUsed(mem[pos], lineNumber) is None):
            return True
        # if the pos is used and ram you can right to it
        if pos.ramOrReg == "ram":
            return False

    @staticmethod
    def getReadWritePositions(commandMnemonic:str, paramIndex:int, mem:Memory):
        commandName = ILU.getName(commandMnemonic)
        if commandName not in SimpleAssembler.readAndWritePos:
            raise Exception(f"No command read write data found for command {commandName}")
        if len(SimpleAssembler.readAndWritePos[commandName]) <= paramIndex:
            raise Exception(f"Param index {paramIndex} out of read/write positions data range for command {commandName}")
        return mem.getMemoryAddressesFromData(SimpleAssembler.readAndWritePos[commandName][paramIndex])

    @staticmethod
    def getBestSpotForVarInRam(varName:str, mem:Memory, lineNumber:int, dataGetter:ContextDataGetter):
        pos = mem.getMappingForVar(varName)
        if pos is not None:
            return pos
        bestPos = None
        bestCost = 1000
        for pos in mem.getMemoryAddressesFromData("ram"):
            cost = None
            if mem[pos] == varName: # the data is already stored there because that is where it was put for the write
                cost = 0
            else:
                var = mem.getVarMappedToPos(pos)
                if var is None: # Do a better choice later, for now this will work
                    cost = 5
            if cost is not None and cost < bestCost:
                bestPos = pos
                bestCost = cost
        if bestPos is not None:
            return bestPos
        raise Exception(f"could not find room in ram to store var {varName} at line {lineNumber}")


class MakeDataToAddOrChange:
    def __init__(self, context:Context) -> None:
        self.context:Context = context.copy()
        self.commandsToAddBeforeLine:dict[int, list] = {}
        self.commandsToAddAfterLine:dict[int, list] = {}
        self.paramsToChange:list[tuple[int, int, str|int|MemoryPos]] = []

    def addCommandBeforeLine(self, lineNumber:int, command:tuple[str, list[str]]) -> None:
        if lineNumber not in self.commandsToAddBeforeLine:
            self.commandsToAddBeforeLine[lineNumber] = []
        self.commandsToAddBeforeLine[lineNumber].append(command)

    def addCommandAfterLine(self, lineNumber:int, command:tuple[str, list[str]]) -> None:
        if lineNumber not in self.commandsToAddAfterLine:
            self.commandsToAddAfterLine[lineNumber] = []
        self.commandsToAddAfterLine[lineNumber].append(command)

    def addParamChange(self, lineNumber:int, paramIndex:int, valueToSet:str|int|MemoryPos):
        self.paramsToChange.append((lineNumber, paramIndex, valueToSet))

    def applyCommands(self) -> Context:
        context = self.context.copy()
        for paramToChange in self.paramsToChange:
            context.getCommand(paramToChange[0])[1][paramToChange[1]] = paramToChange[2]
        for lineNumber in range(len(context)-1, -1, -1):
            if lineNumber in self.commandsToAddAfterLine:
                context.addCommands(self.commandsToAddAfterLine[lineNumber], index=lineNumber+1)
            if lineNumber in self.commandsToAddBeforeLine:
                context.addCommands(self.commandsToAddBeforeLine[lineNumber], index=lineNumber)
        return context

    def getCommandsToAddBeforeLineAtLine(self, lineNumber):
        if lineNumber in self.commandsToAddBeforeLine:
            return self.commandsToAddBeforeLine[lineNumber]
        return []
    
    def getCommandsToAddAfterLineAtLine(self, lineNumber):
        if lineNumber in self.commandsToAddAfterLine:
            return self.commandsToAddAfterLine[lineNumber]
        return []