from __future__ import annotations
from copy import copy, deepcopy
import json

from USML.instructions.instructionLookUp import ILU
from USML.baseAssembler import Assembler
from USML.context import Context, ContextDataGetter, ContextDataChanger

from simpleAssembler.internals.memory import Memory, MemoryPos

class SimpleAssembler(Assembler):
    with open("src/simpleAssembler/settings/InstructionData.json") as f:
        instructionData = json.load(f)
    with open("src/simpleAssembler/settings/Setting.json") as f:
        settings:dict[str] = json.load(f)

    @staticmethod
    def hasInstruction(instructionName) -> bool:
        if instructionName in SimpleAssembler.instructionData:
            return SimpleAssembler.instructionData[instructionName]["hasInstruction"]
        return False
    
    @staticmethod
    def getSimpleCost(instructionName) -> float:
        if instructionName in SimpleAssembler.instructionData:
            return SimpleAssembler.instructionData[instructionName]["cost"]
        raise Exception(f"cant get cost for none implemented instruction {instructionName}")
    
    @staticmethod
    def assemble(context:Context) -> Context:
        return SimpleAssemblerMemoryMannager.doMemoryMannagement(context)

    @staticmethod
    def createdFormatedString(memoryMannagedContext:Context) -> str:
        from simpleAssembler.settings.computerCodeFormater import makeAssembly
        code = ""
        for line in memoryMannagedContext:
            code += makeAssembly(deepcopy(line[0]), deepcopy(SimpleAssembler.instructionData[ILU.getName(line[0][0])])) + "\n"
        return code
    
    @staticmethod
    def createdBinaryString(memoryMannagedContext:Context) -> str:
        from simpleAssembler.settings.computerCodeFormater import makeBinary
        code = ""
        for line in memoryMannagedContext:
            code += makeBinary(deepcopy(line[0]), deepcopy(SimpleAssembler.instructionData[ILU.getName(line[0][0])])) + "\n"
        return code

class SimpleAssemblerMemoryMannager:
    @staticmethod
    def doMemoryMannagement(context:Context) -> Context:
        context = context.copy()
        lastCommand = context.getCommand(len(context) - 1)[0]
        if lastCommand == "@" or "program stop" not in ILU.getTags_Mnemonic(lastCommand):
            context.addCommand(("HLT", []))
        dataGetter = ContextDataGetter(context)
        overlapData = SimpleAssemblerMemoryMannager.getNonOverlappingVars(dataGetter)
        ramVarIndexs = SimpleAssemblerMemoryMannager.getVarAddresses(dataGetter, overlapData)
        dataSetter = ContextDataChanger(context)

    @staticmethod
    def getVarAddresses(dataGetter:ContextDataGetter, overlapData:dict[list[str]]):
        varGroupings:list[list[str]] = []
        for var in overlapData:
            varOverLapData = overlapData[var]
            groupingsToAdd = [[var]]
            for grouping in varGroupings:
                skipAdd = False
                for varName in grouping:
                    if varName not in varOverLapData:
                        skipAdd = True
                        break
                if not skipAdd:
                    groupingsToAdd.append(copy(grouping))
                    grouping.append(var)
            varGroupings.extend(groupingsToAdd)
        varGroupings.sort(key=len, reverse=True)
        varsInGroups:list[str] = []
        for group in varGroupings.copy():
            keepGroup = True
            for var in group:
                if var in varsInGroups:
                    keepGroup = False
                    varGroupings.remove(group)
                    break
            if keepGroup:
                for var in group:
                    varsInGroups.append(var)
        varToRamMap = {}
        ramToVarMap = {}
        for i in range(len(varGroupings)):
            group = varGroupings[i]
            for var in group:
                varToRamMap[var] = i
                ramToVarMap[i] = var
        return varToRamMap, ramToVarMap
    
    @staticmethod
    def getNonOverlappingVars(dataGetter:ContextDataGetter) -> dict[list[str]]:
        foundVarOverLaps:dict[str, list[str]] = {}
        for var1 in dataGetter.context.varNames:
            if dataGetter.getJumpLabelPos(var1, False) != None:
                continue
            foundVarOverLaps[var1] = []
            for var2 in dataGetter.context.varNames:
                if dataGetter.getJumpLabelPos(var2, False) != None:
                    continue
                foundVarOverLaps[var1].append(var2)
        for lineNum in range(len(dataGetter.context)):
            lineVars = dataGetter.shouldHaveVar[lineNum]
            for var1 in lineVars:
                for var2 in lineVars:
                    if var2 in foundVarOverLaps[var1]:
                        try:
                            # print(foundVarOverLaps[var1])
                            # print(var2)
                            foundVarOverLaps[var1].remove(var2)
                        except:
                            pass
        return foundVarOverLaps            

    @staticmethod
    def nothing(context:Context):
        context = context.copy()
        lastCommand = context.getCommand(len(context) - 1)[0]
        if lastCommand == "@" or "program stop" not in ILU.getTags_Mnemonic(lastCommand):
            context.addCommand(("HLT", []))
        dataGetter = ContextDataGetter(context)
        dataSetter = ContextDataChanger(context)
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
            SimpleAssemblerMemoryMannager.doMemoryMannagementForLine(mem, context, dataGetter, dataSetter, lineNumber)
            allMem[lineNumber] = mem.copy()
            if line[0] != "@":
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
                    mem.clearUnmapped()
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
            else:
                nextLineNumber += 1
            while (
                    (context.getCommand(lineNumber)[0] != "@" and "program stop" in ILU.getTags_Mnemonic(context.getCommand(lineNumber)[0])) or
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
    def doMemoryMannagementForLine(mem:Memory, context:Context, dataGetter:ContextDataGetter, dataSetter:ContextDataChanger, lineNumber:int) -> tuple[tuple[str, list[str]], list[tuple[str, MemoryPos]]]:
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
                positions = SimpleAssemblerMemoryMannager.getReadWritePositions(line[0], paramIndex, mem)
                for pos in positionsUsedForInputs:
                    positions.remove(pos)
                if len(positions) == 0:
                    raise Exception(f"error not enough positions left for var {varName} in line {lineNumber}")
                # get the best pos pair
                bestPos = None
                bestCost = 1000 # bigger than max cost
                for varPos in positionsOfVar:
                    for pos in positions:
                        cost = SimpleAssemblerMemoryMannager.getMemSlotUsageCost(mem, varPos, pos, lineNumber, dataGetter, varName)
                        if cost is not None and cost < bestCost:
                            bestPos = (varPos, pos)
                            bestCost = cost
                if bestCost is None:
                    raise Exception(f"error not enough positions left for var {varName} in line {lineNumber}")
                # set data
                positionsUsedForInputs.append(bestPos[1])
                if bestPos[0] != bestPos[1]:
                    dataSetter.addCommandBeforeLine(lineNumber, ("CPY", [bestPos[0], bestPos[1]]))
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
                positions = SimpleAssemblerMemoryMannager.getReadWritePositions(line[0], paramIndex, mem)
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
                        cost = SimpleAssemblerMemoryMannager.getMemSlotUsageCost(mem, None, pos, lineNumber, dataGetter, varName)
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
                    if command[0] == "CPY":
                        memTMP[command[1][1]] = memTMP[command[1][0]]
                for i in range(len(positionsUsedForOutputs)):
                    varName = varsThatAreOutputs[i]
                    for pos in memTMP.getAddressesOfVar(varName):
                        memTMP[pos] = None
                    memTMP[positionsUsedForOutputs[i]] = varName
                for command in dataSetter.getCommandsToAddAfterLineAtLine(lineNumber):
                    if command[0] == "CPY":
                        memTMP[command[1][1]] = memTMP[command[1][0]]
                savePos = SimpleAssemblerMemoryMannager.getBestSpotForVarInRam(varName, memTMP, lineNumber, dataGetter)
                mem.setMappingForVar(varName, savePos)
                if savePos != bestPos:
                    dataSetter.addCommandAfterLine(lineNumber, ("CPY", [bestPos, savePos]))
        # update memory for the next line
        for command in dataSetter.getCommandsToAddBeforeLineAtLine(lineNumber):
            if command[0] == "CPY":
                mem[command[1][1]] = mem[command[1][0]]
        for i in range(len(positionsUsedForOutputs)):
            varName = varsThatAreOutputs[i]
            for pos in mem.getAddressesOfVar(varName):
                mem[pos] = None
            mem[positionsUsedForOutputs[i]] = varName
        for command in dataSetter.getCommandsToAddAfterLineAtLine(lineNumber):
            if command[0] == "CPY":
                mem[command[1][1]] = mem[command[1][0]]
        
    @staticmethod
    def getMemSlotUsageCost(mem:Memory, fromPos:MemoryPos|None, toPos:MemoryPos, lineNumber:int, dataGetter:ContextDataGetter, varName:str) -> float|None:
        # if the data does not have to move it is free
        if fromPos == toPos:
            return 0
        if fromPos != None:
            hasMove = False
            for movementCommand in SimpleAssembler.settings["movementCommands"]:
                if fromPos.containedInData(movementCommand["movementFrom"]):
                    if toPos.containedInData(movementCommand["movementTo"]):
                        hasMove = True
                        break
            if not hasMove:
                return None
        # get the next time the var is used
        nextRead = dataGetter.varNextRead(mem[toPos], lineNumber)
        nextWriten = dataGetter.varNextWriten(mem[toPos], lineNumber)
        # if the pos you are writing to is not used it is cheep
        if (mem[toPos] is None) or (nextWriten is None and nextRead is None) or (toPos.ramOrReg == "reg" and nextRead is None):
            # if the var is not yet mapped put it in ram so that it does not need to move
            if mem.getMappingForVar(varName) == None:
                if toPos.ramOrReg == "ram":
                    return 3
            return 5
        # get cost of overwriting needed data
        # how long till the next time which the data is used (exulding usage pos and this line)
        nextUsed = nextRead
        if nextRead == None:
            nextUsed = nextWriten
        overwriteCost = max((100 - nextUsed["steps"])/20, 0) # 100 / 20 = 5 so max value added is 5
        # if the data is used at this line and the data is in the correct place
        line = dataGetter.context.getCommand(lineNumber)
        usageTypes = ILU.getUsageTypes_Mnemonic(line[0])
        for i in range(len(line[1])):
            if usageTypes[i] == "in":
                if mem[toPos] == line[1][i]:
                    if toPos in SimpleAssemblerMemoryMannager.getReadWritePositions(line[0], i, mem):
                        overwriteCost += 10
                        break
        # if the pos you are writing to is only a reg it is slightly less cheep
        if (toPos.ramOrReg == "reg"):
            return 6 + overwriteCost
        # check if you can even do the movement
        if SimpleAssemblerMemoryMannager.canOverwriteMemoryPos(mem, toPos, lineNumber, dataGetter):
            return 10 + overwriteCost
        # if you can't overwrite the pos. Don't!
        return None

    @staticmethod
    def canOverwriteMemoryPos(mem:Memory, pos:MemoryPos|None, lineNumber:int, dataGetter:ContextDataGetter) -> bool:
        # you can overwrite reg data
        if pos.ramOrReg == "reg":
            return True
        # is the pos is not used not used you can overwrite it
        if (mem[pos] is None) or (dataGetter.varNextRead(mem[pos], lineNumber) is None):
            return True
        # if the pos is used and ram you can right to it
        if pos.ramOrReg == "ram":
            return False

    @staticmethod
    def getReadWritePositions(commandMnemonic:str, paramIndex:int, mem:Memory) -> list[MemoryPos]:
        commandName = ILU.getName(commandMnemonic)
        if commandName not in SimpleAssembler.instructionData:
            raise Exception(f"No command read write data found for command {commandName}")
        if len(SimpleAssembler.instructionData[commandName]["readWritePos"]) <= paramIndex:
            raise Exception(f"Param index {paramIndex} out of read/write positions data range for command {commandName}")
        return mem.getMemoryAddressesFromData(SimpleAssembler.instructionData[commandName]["readWritePos"][paramIndex])

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

