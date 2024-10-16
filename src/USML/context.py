from __future__ import annotations
from typing import Literal
from copy import copy, deepcopy

from USML.instructions.instructionLookUp import ILU

# Context Object
class Context:
    def __init__(self) -> None:
        self.commands: list[tuple[str, list[str]]] = []
        self.costs: list[float] = []
        self.varNames: list[str] = []

    def addCommand(self, command:tuple[str, list[str]]|list[list[str]], cost:float = None, varsToKeep:Literal["all"]|list|None = "all", index:int|None = None) -> None:
        # set varsToKeep
        if varsToKeep is None:
            varsToKeep = []
        # correct command format
        if len(command) == 1:
            command = (command[0], [])
        elif type(command[1]) != list:
            command = (command[0], command[1:len(command)])
        command:tuple[str, list[str]]
        # replace vars in self.vars and not in varsToKeep
        if varsToKeep != "all":
            hashOfOldNames:dict[str, str] = {}
            for i in range(len(command[1])):
                if command[0] == "@" and i == 0:
                    continue
                name = command[1][i]
                if type(name) == str:
                    pre = ""
                    if name[0:1] == "&":
                        pre = "&"
                        name = name[1:len(name)]
                    if name not in varsToKeep and pre + name not in varsToKeep:
                        if name not in hashOfOldNames and (pre + name) not in hashOfOldNames:
                            hashOfOldNames[name] = self.generateNewVarName(name, command[1])
                        command[1][i] = pre + hashOfOldNames[name]
        # add command
        if index is None or index == len(self.commands):
            for i in range(len(command[1])):
                if command[0] == "@" and i == 0:
                    continue
                var = command[1][i]
                if type(var) == str:
                    if var[0:1] == "&":
                        var = var[1:len(var)]
                    if var not in self.varNames:
                        self.varNames.append(var)
            self.commands.append(deepcopy(command))
            self.costs.append(cost)
        else:
            for i in range(len(command[1])):
                if command[0] == "@" and i == 0:
                    continue
                var = command[1][i]
                if type(var) == str:
                    if var[0:1] == "&":
                        var = var[1:len(var)]
                    if var not in self.varNames:
                        self.varNames.append(var)
            self.commands.insert(index, deepcopy(command))
            self.costs.insert(index, cost)

    def addCommands(self, commands:list[tuple[str, list[str]]]|list[list[str]], costs:list[float]|None = None, varsToKeep:Literal["all"]|list|None = "all", index:int|None = None):
        commands = deepcopy(commands)
        # set index
        if index is None:
            index = len(self.commands)
        # set costs
        if costs is None:
            costs = []
        while len(costs) < len(commands):
            costs.append(None)
        # set varsToKeep
        if varsToKeep is None :
            varsToKeep = []
        # loop through all commands for data collection and correction
        vars = []
        for i in range(len(commands)):
            command = commands[i]
            # format command correctly
            if len(command) == 1:
                commands[i] = (command[0], [])
            elif type(command[1]) != list:
                commands[i] = (command[0], command[1:len(command)])
            # get vars used in commands
            for i in range(len(command[1])):
                if command[0] == "@" and i == 0:
                    continue
                var = command[1][i]
                if type(var) == str:
                    if var[0:1] == "&":
                        var = var[1:len(var)]
                    if var not in vars:
                        vars.append(var)
        # loop through all commands
        hashOfOldNames:dict[str, str] = {} # to store the names that have already been changed
        for commandCostPair in zip(commands, costs):
            # replace vars that are in self.vars and not in varsToKeep
            command = commandCostPair[0]
            if varsToKeep != "all":
                for i in range(len(command[1])):
                    if command[0] == "@" and i == 0:
                        continue
                    name = command[1][i]
                    if type(name) == str:
                        pre = ""
                        if name[0:1] == "&":
                            pre = "&"
                            name = name[1:len(name)]
                        if name not in varsToKeep and pre + name not in varsToKeep:
                            if name not in hashOfOldNames:
                                hashOfOldNames[name] = self.generateNewVarName(name, vars)
                            command[1][i] = pre + hashOfOldNames[name]
            # add command
            for i in range(len(command[1])):
                if command[0] == "@" and i == 0:
                    continue
                var = command[1][i]
                if type(var) == str:
                    if var[0:1] == "&":
                        var = var[1:len(var)]
                    if var not in self.varNames:
                        self.varNames.append(var)
            self.commands.insert(index, commandCostPair[0])
            self.costs.insert(index, commandCostPair[1])
            index += 1
    
    def addContext(self, context:Context, varsToKeep:Literal["all"]|list|None = "all", index:int = None) -> None:
        context = context.copy()
        # set index
        if index is None:
            index = len(self.commands) + 1
        # set varsToKeep
        if varsToKeep is None :
            varsToKeep = []
        # replace vars that are in self.vars and not in varsToKeep
        if varsToKeep != "all":
            hashOfOldNames:dict[str, str] = {}
            def correctVarNames(var, line, type, usageType):
                pre = ""
                if var[0:1] == "&":
                    pre = "&"
                    var = var[1:len(var)]
                if var not in varsToKeep and pre + var not in varsToKeep:
                    if var not in hashOfOldNames:
                        hashOfOldNames[var] = self.generateNewVarName(var, context.varNames)
                    return pre + hashOfOldNames[var]
                return None
            context.iterOverParams(correctVarNames)
        # loop through all commands
        for commandCostPair in context:
            # add command
            command = commandCostPair[0]
            for i in range(len(command[1])):
                if command[0] == "@" and i == 0:
                    continue
                var = command[1][i]
                if type(var) == str:
                    if var[0:1] == "&":
                        var = var[1:len(var)]
                    if var not in self.varNames:
                        self.varNames.append(var)
            self.commands.insert(index, command)
            self.costs.insert(index, commandCostPair[1])
            index += 1

    def removeCommand(self, index:int) -> tuple[tuple[str, list[str]], float]|None:
        if index >= 0 and index < len(self.commands):
            pair = (self.commands[index], self.costs[index])
            del self.commands[index]
            del self.costs[index]
            self.updateVarNames()
            return pair
        return None

    def getCommand(self, index:int) -> tuple[str, list[str]]|None:
        if index >= 0 and index < len(self.commands):
            return self.commands[index]
        return None
    
    def setCost(self, value:float, index:int) -> None:
        if index >= 0 and index < len(self.commands):
            self.costs[index] = value

    def getCost(self, index:int|None = None) -> float|None:
        if index is None:
            cost = 0
            for c in self.costs:
                if c is not None:
                    cost += c
            return cost
        if index >= 0 and index < len(self.commands):
            return self.costs[index]
        return None

    def copy(self):
        newContext = Context()
        newContext.commands = deepcopy(self.commands)
        newContext.costs = deepcopy(self.costs)
        newContext.varNames = deepcopy(self.varNames)
        return newContext

    def replaceVarName(self, nameToReplace, nameToUse):
        for line in self.commands:
            for i in range(len(line[1])):
                if line[0] == "@" and i == 0:
                    continue
                pre = ""
                var = line[1][i]
                if var[0:1] == "&":
                    pre = "&"
                    var = var[1:len(var)]
                if var == nameToReplace:
                    line[1][i] = pre + nameToUse
        self.updateVarNames()

    def replaceVarNames(self, replacementDict:dict):
        def replaceFunc(var, line, varType, usageType):
            pre = ""
            if var[0:1] == "&":
                pre = "&"
                var = var[1:len(var)]
            if var in replacementDict:
                if type(replacementDict[var]) == str:
                    return pre + replacementDict[var]
                return replacementDict[var]
        self.iterOverParams(replaceFunc)
        self.updateVarNames()

    def replaceVarNamesWithUniqueNames(self, replacementDict:dict):
        def replaceFunc(var, line, varType, usageType):
            pre = ""
            if var[0:1] == "&":
                pre = "&"
                var = var[1:len(var)]
            if var in replacementDict:
                if type(replacementDict[var]) == str:
                    return pre + replacementDict[var]
                return replacementDict[var]
            elif var in replacementDict.values():
                replacementDict[var] = self.generateNewVarName(var, replacementDict.values())
                if type(replacementDict[var]) == str:
                    return pre + replacementDict[var]
                return replacementDict[var]
        self.iterOverParams(replaceFunc)
        self.updateVarNames()

    def generateNewVarName(self, oldName:str|None = None, toExclude:None|list[str] = None):
        if toExclude is None:
            toExclude = []
        if oldName in self.varNames:
            i = 1
            while (oldName + str(i) in self.varNames) or (oldName + str(i) in toExclude):
                i += 1
            return oldName + str(i)
        return oldName
    
    def hasVarName(self, varName):
        return varName in self.varNames

    def iterOverParams(self, functionToRun:function, includeNumbers = False):
        """
        calls a function on every param in the context

        Data in: (name, line, type, usageType)
        Returning any data will rename the var to that data.
        """
        for lineNumber in range(len(self.commands)):
            command = self.commands[lineNumber]
            for i in range(len(command[1])):
                if command[0] == "@" and i == 0:
                    continue
                name = command[1][i]
                if includeNumbers or type(name) == str:
                    expectedDataType = None
                    usageTypes = None
                    if command[0] == "@":
                        expectedDataType = [None, "Var"][i]
                        usageTypes = [None, "in"][i]
                    else:
                        expectedDataType = ILU.getExpectedDataType_Mnemonic(command[0])[i]
                        usageTypes = ILU.getUsageTypes_Mnemonic(command[0])[i]
                    newName = functionToRun(
                        name,
                        lineNumber,
                        expectedDataType,
                        usageTypes
                    )
                    if newName is not None:
                        command[1][i] = newName

    def iterOverLines(self, functionToRun:function):
        """
        calls a function on every line in the context

        Data in: (line, lineNumber)
        """
        for lineNumber in range(len(self.commands)):
            command = self.commands[lineNumber]
            newCommand = functionToRun(command, lineNumber)

    def updateVarNames(self):
        self.varNames = []
        def addName(name, line, type, usageType):
            if name[0:1] == "&":
                name = name[1:len(name)]
            if name not in self.varNames:
                self.varNames.append(name)
        self.iterOverParams(addName)

    def __copy__(self):
        return self.copy()

    def __len__(self):
        return len(self.commands)

    def __iter__(self):
        return zip(self.commands, self.costs).__iter__()

    def __str__(self):
        string = ""
        string += " L | C |                 |\n"
        string += " I | O |                 |\n"
        string += " N | S |  C O M M A N D  |   P A R A M S\n"
        string += " E | T |                 |\n"
        string += "---+---+-----------------+------------+------------+------------+------------+------------+\n"
        i = 0
        while i < len(self.commands):
            cost = self.costs[i]
            if cost is None:
                cost = "X"
            else:
                cost = str(cost)
            if len(cost) == 1:
                cost = " " + cost + " "
            elif len(cost) == 2:
                cost = " " + cost
            elif len(cost) == 3:
                cost = cost
            else:
                cost = cost
            line = str(i)
            if len(line) == 1:
                line = " " + line + " "
            elif len(line) == 2:
                line = line + " "
            elif len(line) == 3:
                line = line
            else:
                line = line
            string += line + "|" + cost + "|   " + self.commands[i][0] + (14 - len(self.commands[i][0])) * " " + "|"
            ii = 0
            for item in self.commands[i][1]:
                if ii > 0:
                    string += "|"
                if type(item) == float:
                    item = int(item)
                string += " " + str(item) + (11 - len(str(item))) * " "
                ii += 1
            string += "\n"
            i += 1
        return string

# Context Data Getter Object
class ContextDataGetter:
    def __init__(self, context:Context):
        self.context:Context = context.copy()
        self.varAndLabelUsage = None
        self.labelPositions:dict[str, int] = None
        self.shouldHaveVar:dict[int, list[str]] = {}
        self.varsRead:dict[int, list[str]] = {}
        self.varsWritten:dict[int, list[str]] = {}
        self.getRunOrderData()

    def getJumpLabelPos(self, labelName, raiseExceptions = True) -> int:
        if self.labelPositions is not None:
            if labelName in self.labelPositions:
                return self.labelPositions[labelName]
            if raiseExceptions:
                raise Exception(f"cound not find label {labelName}")
            return None
        self.labelPositions = {}
        for i in range(len(self.context)):
            line = self.context.getCommand(i)
            if line[0] == ".":
                self.labelPositions[line[1][0]] = i
        if labelName in self.labelPositions:
            return self.labelPositions[labelName]
        if raiseExceptions:
            raise Exception(f"cound not find label {labelName}")
        return None

    def getVarAndLabelUsage(self) -> dict[str, dict[str, list[dict[str, int]]|int]]:
        if self.varAndLabelUsage is not None:
            return self.varAndLabelUsage
        data:dict[str, dict[str, str|int|list[dict[str, int]]]] = {}
        def getData(name:str, line:int, type:str, usageType:str):
            if name not in data:
                data[name] = {
                    "usage": [],
                    "count": 0,
                    "type": type
                }
            data[name]["count"] += 1
            data[name]["usage"].append({"usageType": usageType, "line": line})

        self.context.iterOverParams(getData)
        self.varAndLabelUsage = data
        return data

    class IterInRunOrderData:
        def doLine(self, line, lineNumber) -> None:
            pass
            
        def copy(self) -> ContextDataGetter.IterInRunOrderData:
            pass

    def iterInRunOrder(self, iterInRunOrderData:IterInRunOrderData, lineNumber:int = 0, skipDoLineOnFirstLine:bool = True, vistedLines:list[int] = None):
        if vistedLines is None:
            vistedLines = []
        while lineNumber not in vistedLines:
            vistedLines.append(lineNumber)
            line = self.context.getCommand(lineNumber)
            if line is None:
                    break
            if len(vistedLines) > 1 or not skipDoLineOnFirstLine:
                iterInRunOrderData.doLine(line, lineNumber)
            if line[0] != "@":
                if "program stop" in ILU.getTags_Mnemonic(line[0]):
                    break
                elif "force jump" in ILU.getTags_Mnemonic(line[0]):
                    lineNumber = self.getJumpLabelPos(line[1][0])
                elif  "maybe jump" in ILU.getTags_Mnemonic(line[0]):
                    for i in self.iterInRunOrder(iterInRunOrderData.copy(), self.getJumpLabelPos(line[1][0]), False, deepcopy(vistedLines)):
                        yield i
            lineNumber += 1
        yield iterInRunOrderData

    def getRunOrderData(self):
        class IterClass(ContextDataGetter.IterInRunOrderData):
            def __init__(self) -> None:
                self.vistedLineOrder:list = []
                self.shouldHaveVar:dict[int, list[str]] = {}
                self.forceHaveVar:dict[int, list[str]] = {}
                self.varsRead:dict[int, list[str]] = {}
                self.varsWritten:dict[int, list[str]] = {}
                self.lastLine:tuple[str, list[str|int]]|None = None

            def doLine(self, line, lineNumber):
                # if it is the first line there is no previous var data
                if len(self.vistedLineOrder) == 0:
                    self.shouldHaveVar[lineNumber] = []
                    self.forceHaveVar[lineNumber] = []
                else:
                    # copy the forced vars
                    self.shouldHaveVar[lineNumber] = copy(self.forceHaveVar[self.vistedLineOrder[0]])
                    self.forceHaveVar[lineNumber] = copy(self.forceHaveVar[self.vistedLineOrder[0]])
                # make arrays for var read written data
                self.varsRead[lineNumber] = []
                self.varsWritten[lineNumber] = []
                # do line
                if line[0] == "@":
                    if line[1][0] == "hold":
                        if line[1][1] not in self.forceHaveVar[lineNumber]:
                            self.shouldHaveVar[lineNumber].append(line[1][1])
                            self.forceHaveVar[lineNumber].append(line[1][1])
                    elif line[1][0] == "release":
                        if line[1][1] in self.forceHaveVar[lineNumber]:
                            self.shouldHaveVar[lineNumber].remove(line[1][1])
                            self.forceHaveVar[lineNumber].remove(line[1][1])
                else:
                    paramUsageTypes = ILU.getUsageTypes_Mnemonic(line[0])
                    paramDataTypes = ILU.getExpectedDataType_Mnemonic(line[0])
                    params = line[1]
                    for paramIndex in range(len(params)):
                        if paramDataTypes[paramIndex] == "var":                            
                            varName = params[paramIndex]
                            self.shouldHaveVar[lineNumber].append(varName)
                            if paramUsageTypes[paramIndex] in ["out", "both"]:
                                if varName not in self.varsWritten[lineNumber]:
                                    self.varsWritten[lineNumber].append(varName)
                            if paramUsageTypes[paramIndex] in ["in", "both"]:
                                if varName not in self.varsRead[lineNumber]:
                                    self.varsRead[lineNumber].append(varName)
                                    foundVar = False
                                    for previousLinNumber in self.vistedLineOrder:
                                        self.shouldHaveVar[previousLinNumber].append(varName)
                                        if varName in self.varsWritten[previousLinNumber] or varName in self.shouldHaveVar[previousLinNumber]:
                                            foundVar = True
                                            break
                                    if not foundVar:
                                        raise Exception(f"did not find var {varName} on line {lineNumber}. Line trace {str(self.vistedLineOrder)}")
                self.vistedLineOrder.insert(0, lineNumber)
                self.lastLine = line
                        
            def copy(self):
                newClass = IterClass()
                newClass.vistedLineOrder = copy(self.vistedLineOrder)
                newClass.shouldHaveVar = deepcopy(self.shouldHaveVar)
                newClass.forceHaveVar = deepcopy(self.forceHaveVar)
                newClass.varsRead = deepcopy(self.varsRead)
                newClass.varsWritten = deepcopy(self.varsWritten)
                newClass.lastLine = self.lastLine
                return newClass
        self.traceDatas:list[IterClass] = []
        for i in self.iterInRunOrder(IterClass(), skipDoLineOnFirstLine=False):
            self.traceDatas.append(i)
        for lineNumber in range(len(self.context)):
            self.shouldHaveVar[lineNumber] = []
            self.varsRead[lineNumber] = []
            self.varsWritten[lineNumber] = []
            for traceData in self.traceDatas:
                if lineNumber in traceData.shouldHaveVar:
                    for varName in traceData.shouldHaveVar[lineNumber]:
                        if varName not in self.shouldHaveVar[lineNumber]:
                            self.shouldHaveVar[lineNumber].append(varName)
                if lineNumber in traceData.varsRead:
                    for varName in traceData.varsRead[lineNumber]:
                        if varName not in self.varsRead[lineNumber]:
                            self.varsRead[lineNumber].append(varName)
                if lineNumber in traceData.varsWritten:
                    for varName in traceData.varsWritten[lineNumber]:
                        if varName not in self.varsWritten[lineNumber]:
                            self.varsWritten[lineNumber].append(varName)
            
    def needVarOnLine(self, varName:str, lineNumber:int):
        if lineNumber in self.shouldHaveVar:
            return (varName in self.shouldHaveVar[lineNumber])

    def varNextWriten(self, varName:str, lineNumber:int):
        for trace in self.traceDatas:
            if lineNumber in trace.vistedLineOrder:
                index = trace.vistedLineOrder.index(lineNumber)
                while len(self.varsWritten) < index:
                    if varName in self.varsWritten[index]:
                        return lineNumber
                    index += 1
        return None

# Context Data Changer Object
class ContextDataChanger:
    def __init__(self, context:Context) -> None:
        self.context:Context = context.copy()
        self.commandsToAddBeforeLine:dict[int, list] = {}
        self.commandsToAddAfterLine:dict[int, list] = {}
        self.paramsToChange:list[tuple[int, int, str|int]] = []

    def addCommandBeforeLine(self, lineNumber:int, command:tuple[str, list[str]]) -> None:
        if lineNumber not in self.commandsToAddBeforeLine:
            self.commandsToAddBeforeLine[lineNumber] = []
        self.commandsToAddBeforeLine[lineNumber].append(command)

    def addCommandAfterLine(self, lineNumber:int, command:tuple[str, list[str]]) -> None:
        if lineNumber not in self.commandsToAddAfterLine:
            self.commandsToAddAfterLine[lineNumber] = []
        self.commandsToAddAfterLine[lineNumber].append(command)

    def addParamChange(self, lineNumber:int, paramIndex:int, valueToSet:str|int):
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
