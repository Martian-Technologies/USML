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
        rwPos = SimpleAssembler.readAndWritePos # make it simple
        dataGetter = ContextDataGetter(context)
        getVarAndLabelUsage = dataGetter.getVarAndLabelUsage()
        allMem:dict[int, Memory] = {}
        mem = Memory(SimpleAssembler.settings["memorySizes"])
        dataToSet:list[tuple[int, tuple[list[tuple[str, list[str]]], list[tuple[str, MemoryPos|str]]]]] = []
        lineNumber = 0
        totalLineCount = len(context)
        toDoJumps:list[tuple[int, int]] = []
        keepGoing = True
        while keepGoing:
            line = context.getCommand(lineNumber)
            data = (lineNumber, SimpleAssembler.doMemoryMannagement(mem, context, rwPos, dataGetter, lineNumber))
            dataToSet.append(data)
            allMem[lineNumber] = mem.copy()
            tags = ILU.getTags_Mnemonic(line[0])
            if "force jump" in tags:
                labelData = getVarAndLabelUsage[line[1][0]]
                newLineNumber = None
                for usage in labelData["usage"]:
                    if usage["usageType"] == "out":
                        newLineNumber = usage["line"]
                if newLineNumber is None:
                    raise Exception(f"Label {i + 1} in {command} on line {lineNumber} is not defined.")
                if newLineNumber in allMem:
                    commands:list[tuple[str, list[str]]] = SimpleAssembler.mergeMemoryAtLabel(allMem[newLineNumber], mem, newLineNumber, dataGetter)
                    if len(commands) != 0:
                        newLabel = context.generateNewVarName(line[1][0])
                        commands.insert(0, (".", [newLabel]))
                        commands.append(("JMP", [line[1][0]]))
                        dataToSet.append((lineNumber, ([], [(line[1][0], newLabel)])))
                        dataToSet.append((totalLineCount, (commands, [])))
                    lineNumber = newLineNumber
                else:
                    lineNumber = newLineNumber - 1
            elif "maybe jump" in tags:
                labelData = getVarAndLabelUsage[line[1][0]]
                newLineNumber = None
                for usage in labelData["usage"]:
                    if usage["usageType"] == "out":
                        newLineNumber = usage["line"]
                if newLineNumber is None:
                    raise Exception(f"Label {i + 1} in {command} on line {lineNumber} is not defined.")
                toDoJumps.append((lineNumber, newLineNumber))
            elif ("program stop" in tags) or (lineNumber+1 >= totalLineCount):
                if len(toDoJumps) == 0:
                    keepGoing = False
                else:
                    jump = toDoJumps.pop()
                    lineNumber = jump[0]
                    line = context.getCommand(lineNumber)
                    mem = allMem[lineNumber].copy()
                    newLineNumber = jump[1]
                    if newLineNumber in allMem:
                        commands:list[tuple[str, list[str]]] = SimpleAssembler.mergeMemoryAtLabel(allMem[newLineNumber], mem, newLineNumber, dataGetter)
                        if len(commands) != 0:
                            newLabel = context.generateNewVarName(line[1][0])
                            commands.insert(0, (".", [newLabel]))
                            commands.append(("JMP", [line[1][0]]))
                            dataToSet.append((lineNumber, ([], [(line[1][0], newLabel)])))
                            dataToSet.append((totalLineCount, (commands, [])))
                        lineNumber = newLineNumber
                    else:
                        lineNumber = newLineNumber - 1
            lineNumber += 1
            if context.getCommand(lineNumber)[0] == ".":
                if lineNumber in allMem:
                    commands:list[tuple[str, list[str]]] = SimpleAssembler.mergeMemoryAtLabel(allMem[lineNumber], mem, lineNumber, dataGetter)
                    if len(commands) != 0:
                        dataToSet.append((lineNumber, (commands, [])))
            while (lineNumber in allMem) and keepGoing:
                if len(toDoJumps) == 0:
                    keepGoing = False
                else:
                    jump = toDoJumps.pop()
                    lineNumber = jump[0]
                    line = context.getCommand(lineNumber)
                    mem = allMem[lineNumber].copy()
                    newLineNumber = jump[1]
                    if newLineNumber in allMem:
                        commands:list[tuple[str, list[str]]] = SimpleAssembler.mergeMemoryAtLabel(allMem[newLineNumber], mem, newLineNumber, dataGetter)
                        if len(commands) != 0:
                            newLabel = context.generateNewVarName(line[1][0])
                            commands.insert(0, (".", [newLabel]))
                            commands.append(("JMP", [line[1][0]]))
                            dataToSet.append((lineNumber, ([], [(line[1][0], newLabel)])))
                            dataToSet.append((totalLineCount, (commands, [])))
                        lineNumber = newLineNumber
                    else:
                        lineNumber = newLineNumber - 1
        dataToSet = sorted(dataToSet, key=(lambda a:-a[0]))
        orderingOffsetsPerLine = {}
        for data in dataToSet:
            lineNumber = data[0]
            if lineNumber not in orderingOffsetsPerLine:
                orderingOffsetsPerLine[lineNumber] = 0
            varValuesToChange = data[1][1]
            for varValue in varValuesToChange:
                line = context.getCommand(lineNumber + orderingOffsetsPerLine[lineNumber])
                for i in range(len(line[1])):
                    if line[1][i] == varValue[0]:
                        line[1][i] = varValue[1]
            commands = data[1][0]
            for command in commands:
                context.addCommand(command, index=lineNumber + orderingOffsetsPerLine[lineNumber])
                orderingOffsetsPerLine[lineNumber] += 1
        return context
            
    @staticmethod
    def doMemoryMannagement(mem:Memory, context:Context, rwPos:dict[str, list[str|list[str|None]|None]], dataGetter:ContextDataGetter, lineNumber:int) -> tuple[tuple[str, list[str]], list[tuple[str, MemoryPos]]]:
        line = context.getCommand(lineNumber)
        commandDataTypes:list[str] = ILU.getExpectedDataType_Mnemonic(line[0])
        commandUsageTypes:list[str] = ILU.getUsageTypes_Mnemonic(line[0])
        commandRWPos = rwPos[ILU.getName(line[0])]
        positionsUsedForInputs:list[MemoryPos] = []
        positionsUsedForGettingInputs:list[MemoryPos] = []
        positionsUsedForOutputs:list[MemoryPos] = []
        varNamesUsedForOutputs:list[str] = []
        varsToGiveAddresses:list[tuple[str, MemoryPos]] = []
        for i in range(len(line[1])):
            if commandDataTypes[i] != "var": # make sure the data type is a var
                continue
            if commandUsageTypes[i] in ["in", "both"]:
                # get the var's name
                varName = line[1][i]
                # get the current positions or the var
                positionsOfVar = []
                for memTypeIndex in range(len(mem)):
                    memType = mem[memTypeIndex]
                    for memIndex in range(len(memType)):
                        if memType[memIndex] == varName:
                            positionsOfVar.append(MemoryPos(memTypeIndex, memIndex))
                if len(positionsOfVar) == 0:
                    raise Exception(f"can not used undefined var {varName} on line {lineNumber}")
                # get memory addresses
                positionsCompact:str|list[str|None]|None = commandRWPos[i]
                if positionsCompact is None or len(positionsCompact) == 0: # all var params need positions
                    raise Exception(f"Command {ILU.getName(line[0])} can not have var with out read or write pos at param {i}")
                positions:list[MemoryPos] = []
                for pos in positionsCompact:
                    positions.extend(SimpleAssembler.getMemoryAddressesFromData(pos, mem, positionsUsedForInputs))
                if len(positions) == 0:
                    raise Exception(f"error not enough positions left for var {varName} in line {lineNumber}")
                # get all the possible positions and costs for the var
                possiblePositions:list[tuple[int, MemoryPos]] = []
                for varPos in positionsOfVar:
                    for pos in positions:
                        cost = SimpleAssembler.getMemSlotUsageCost(mem, varPos, pos, lineNumber, dataGetter)
                        possiblePositions.append((cost, pos, varPos))
                # get the position with the least cost
                best = None
                for pos in possiblePositions:
                    if best is None:
                        best = pos
                    elif pos[0] < best[0]:
                        best = pos
                varsToGiveAddresses.append((varName, best[1]))
                positionsUsedForGettingInputs.append(best[2])
                positionsUsedForInputs.append(best[1])
                if commandUsageTypes[i] == "both":
                    varNamesUsedForOutputs.append(varName)
                    positionsUsedForOutputs.append(best[1])
        for i in range(len(line[1])):
            if commandDataTypes[i] != "var": # make sure the data type is a var
                continue
            if commandUsageTypes[i] == "out":
                # get the var's name
                varName = line[1][i]
                # get memory addresses
                positionsCompact:str|list[str|None]|None = commandRWPos[i]
                if positionsCompact is None: # all var params need positions
                    raise Exception(f"Command {ILU.getName(line[0])} can not have var with out read or write pos at param {i}")
                positions:list[MemoryPos] = []
                for pos in positionsCompact:
                    positions.extend(SimpleAssembler.getMemoryAddressesFromData(pos, mem, positionsUsedForOutputs))
                # get all the possible positions and costs for the var
                possiblePositions:list[tuple[int, MemoryPos]] = []
                for pos in positions:
                    cost = None
                    if mem[pos] == varName:
                        cost = 0
                    else:
                        cost = SimpleAssembler.getMemSlotUsageCost(mem, None, pos, lineNumber, dataGetter)
                    possiblePositions.append((cost, pos))
                # get the position with the least cost
                best = None
                for pos in possiblePositions:
                    if best is None:
                        best = pos
                    elif pos[0] < best[0]:
                        best = pos
                varsToGiveAddresses.append((varName, best[1]))
                varNamesUsedForOutputs.append(varName)
                positionsUsedForOutputs.append(best[1])
        commandsToAdd = []
        memThatWillBeSet = []
        for i in range(len(positionsUsedForInputs)):
            fromPos = positionsUsedForGettingInputs[i]
            toPos = positionsUsedForInputs[i]
            if fromPos == toPos:
                continue
            if mem[toPos] == mem[fromPos] or SimpleAssembler.canOverwriteMemoryPos(mem, toPos, lineNumber, dataGetter, commandsToAdd):
                commandsToAdd.append(("move", [fromPos, toPos]))
            else:
                possiblePositions = []
                for memIndex in range(len(mem)):
                    for memAddress in range(len(mem[memIndex])):
                        pos = MemoryPos(memIndex, memAddress)
                        if not ((pos in positionsUsedForInputs) or (pos in positionsUsedForOutputs) or (pos in positionsUsedForGettingInputs)):
                            cost = SimpleAssembler.getMemSlotUsageCost(mem, toPos, pos, lineNumber, dataGetter, commandsToAdd)
                            if cost is not None:
                                possiblePositions.append((cost, pos))
                            else:
                                raise Exception(f"ran out of memory to store {mem[toPos]} (to allow other data to go there) at line {lineNumber}")
                best = None
                for pos in possiblePositions:
                    if best is None:
                        best = pos
                    elif pos[0] < best[0]:
                        best = pos
                commandsToAdd.append(("move", [toPos, best[1]]))
                commandsToAdd.append(("move", [fromPos, toPos]))
        for i in range(len(positionsUsedForOutputs)):
            writePos = positionsUsedForOutputs[i]
            varName = varNamesUsedForOutputs[i]
            if mem[writePos] == varName or SimpleAssembler.canOverwriteMemoryPos(mem, writePos, lineNumber, dataGetter, commandsToAdd):
                memThatWillBeSet.append((writePos, varNamesUsedForOutputs[i]))
            else:
                possiblePositions = []
                for memIndex in range(len(mem)):
                    for memAddress in range(len(mem[memIndex])):
                        pos = MemoryPos(memIndex, memAddress)
                        if not ((pos in positionsUsedForInputs) or (pos in positionsUsedForOutputs) or (pos in positionsUsedForGettingInputs)):
                            cost = SimpleAssembler.getMemSlotUsageCost(mem, writePos, pos, lineNumber, dataGetter, commandsToAdd)
                            if cost is not None:
                                possiblePositions.append((cost, pos))
                            else:
                                raise Exception(f"ran out of memory to store {mem[writePos]} (to allow other data to go there) at line {lineNumber}")
                best = None
                for pos in possiblePositions:
                    if best is None:
                        best = pos
                    elif pos[0] < best[0]:
                        best = pos
                commandsToAdd.append(("move", [writePos, best[1]]))
                memThatWillBeSet.append((writePos, varName))
       
        for command in commandsToAdd:
            if command[0] == "move":
                mem[command[1][1]] = mem[command[1][0]]
        for posName in memThatWillBeSet:
            for pos in mem.getAddressesOfVar(posName[1]):
                mem[pos] = None
            mem[posName[0]] = posName[1]
        return commandsToAdd, varsToGiveAddresses

    @staticmethod
    def mergeMemoryAtLabel(memToKeep:Memory, memToChange:Memory, lineNumber:int, dataGetter:ContextDataGetter) -> list[tuple[str, list[str]]]:
        commandsToAdd:list[tuple[str, list[str]]] = []
        memToChange = memToChange.copy()
        todo:list[MemoryPos] = SimpleAssembler.getMemoryAddressesFromData("all", memToKeep)
        while len(todo) > 0:
            position:MemoryPos = todo.pop()
            data = SimpleAssembler.mergeMemoryAtLabelRec(memToKeep, memToChange, lineNumber, dataGetter, position)
            commandsToAdd.extend(data[0])  
            todo.extend(data[1])
        return commandsToAdd
    
    @staticmethod
    def mergeMemoryAtLabelRec(memToKeep:Memory, memToChange:Memory, lineNumber:int, dataGetter:ContextDataGetter, position:MemoryPos) -> list[tuple[str, list[str]]]:
        shouldBeAtAddress = memToKeep[position]
        varAtAddress = memToChange[position]
        if (shouldBeAtAddress is None) or (dataGetter.varNextUsed(shouldBeAtAddress, lineNumber) is None) or (shouldBeAtAddress == varAtAddress):
            return ([], [])
        commandsToAdd:list[tuple[str, list[str]]] = []
        dirtiedPositions:list[MemoryPos] = []
        addresses = memToChange.getAddressesOfVar(shouldBeAtAddress)
        addressesUnwantedMemToChange = memToChange.getAddressesOfVar(varAtAddress)
        addressesUnwantedMemToKeep = memToKeep.getAddressesOfVar(varAtAddress)
        if (varAtAddress is None) or (dataGetter.varNextUsed(varAtAddress, lineNumber) is None) or (len(addressesUnwantedMemToChange) > 1) or (len(addressesUnwantedMemToKeep) == 0):
            if len(addresses) == 0:
                raise Exception(f"failed to find var {shouldBeAtAddress} while doing memory merge on memorys {memToKeep} and {memToChange} at memory {position}")
            memToChange[addresses[0]] = shouldBeAtAddress
            commandsToAdd.append(("move", [addresses[0], position]))
        else:
            possiblePositions = []
            for memIndex in range(len(memToChange)):
                for memAddress in range(len(memToChange[memIndex])):
                    pos = MemoryPos(memIndex, memAddress)
                    shouldBeAtPos = memToKeep[pos]
                    varAtPos = memToChange[pos]
                    cost = 0
                    if (varAtPos is None) or (dataGetter.varNextUsed(varAtPos, lineNumber) is None) or (len(memToChange.getAddressesOfVar(varAtPos)) > 1) or (len(memToKeep.getAddressesOfVar(varAtPos)) == 0):
                        if shouldBeAtPos == varAtPos:
                            cost += 5
                        if shouldBeAtPos == varAtAddress:
                            cost -= 20
                        possiblePositions.append((cost, pos))
            best = None
            for pos in possiblePositions:
                if best is None:
                    best = pos
                elif pos[0] < best[0]:
                    best = pos
            if best is None:
                raise Exception(f"ran out of memory to store {varAtAddress} (to allow other data to go there)\
                                  while doing memory merge on memorys {memToKeep} and {memToChange} at memory {position}")
            memToChange[best[1]] = memToChange[position]
            dirtiedPositions.append(best[1])
            commandsToAdd.append(("move", [position, best[1]]))
            addresses = memToChange.getAddressesOfVar(shouldBeAtAddress)
            if len(addresses) == 0:
                raise Exception(f"failed to find var {shouldBeAtAddress} while doing memory merge on memorys {memToKeep} and {memToChange} at memory {position}. Also this should not happen")
            commandsToAdd.append(("move", [addresses[0] ,position]))
        return commandsToAdd, dirtiedPositions

    @staticmethod
    def getMemSlotUsageCost(mem:Memory, fromPos:MemoryPos|None, toPos:MemoryPos, lineNumber:int, dataGetter:ContextDataGetter, commandsToAdd=None, allowOverWrite=True) -> float|None:
        if fromPos == toPos:
            return 0
        nextUsed = dataGetter.varNextUsed(mem[toPos], lineNumber)
        if (mem[toPos] is None) or (nextUsed is None): # rather not overwrite vars
            return 5
        if SimpleAssembler.canOverwriteMemoryPos(mem, toPos, lineNumber, dataGetter, commandsToAdd):
            return 10 + max((100 - nextUsed["steps"])/20, 0)
        line = dataGetter.context.getCommand(lineNumber)
        usageTypes = ILU.getUsageTypes_Mnemonic(line[0])
        isNeeded = False
        for i in range(len(line[1])):
            if mem[toPos] == line[1][i]:
                if usageTypes[i] == "in":
                    isNeeded = True
                    break
        if allowOverWrite:
            return 20 + max((100 - nextUsed["steps"])/20, 0) +(10 if isNeeded else 0)
        return None

    @staticmethod
    def canOverwriteMemoryPos(mem:Memory, pos:MemoryPos|None, lineNumber:int, dataGetter:ContextDataGetter, commandsToAdd=None):
        if commandsToAdd != None:
            mem = mem.copy()
            for command in commandsToAdd:
                if command[0] == "move":
                    mem[command[1][1]] = mem[command[1][0]]
        return (mem[pos] is None) or (len(mem.getAddressesOfVar(mem[pos])) > 1) or (dataGetter.varNextUsed(mem[pos], lineNumber) is None)

    @staticmethod
    def getMemoryAddressesFromData(data, mem:Memory, positionNotToUse:list[MemoryPos] = None):
        if positionNotToUse is None:
            positionNotToUse = []
        positions:list[MemoryPos] = []
        if type(data) == list:
            if len(data) == 1:
                for memAddress in range(len(mem[data[0]])):
                    positions.append(MemoryPos(data[0], memAddress))
            elif type(data[1]) == list:
                if len(data[1]) == 1:
                    positions.append(MemoryPos(data[0], data[1][0]))
                for memAddress in range(data[1][0], data[1][1] + (-1 if (data[1][0] > data[1][1]) else 1), -1 if (data[1][0] > data[1][1]) else 1):
                    positions.append(MemoryPos(data[0], memAddress))
            else:
                positions.append(MemoryPos(data[0], data[1]))
        elif type(data) == str:
            if data == "all":
                for memIndex in range(len(mem)):
                    for memAddress in range(len(mem[memIndex])):
                        positions.append(MemoryPos(memIndex, memAddress))
        else:
            for memIndex in range(len(mem[data])):
                positions.append(MemoryPos(data, memIndex))
        for pos in positionNotToUse:
            positions.remove(pos)
        return positions
