from __future__ import annotations
from typing import Literal
from copy import deepcopy

from USML.instructions.instructionLookUp import ILU

# Context Object
class Context:
    def __init__(self) -> None:
        self.commands: list[tuple[str, list[str]]] = []
        self.costs: list[float] = []
        self.varNames: list[str] = []

    def addCommand(self, command: tuple[str, list[str]] | list[list[str]], cost: float = None, varsToKeep:Literal["all"]|list|None = "all", index: int|None = None) -> None:
        # set varsToKeep
        if varsToKeep is None :
            varsToKeep = []
        # correct command format
        if len(command) == 1:
            command = (command[0], [])
        elif type(command[1]) == str:
            command = (command[0], command[1:len(command)])
        command:tuple[str, list[str]]
        # replace vars in self.vars and not in varsToKeep
        if varsToKeep != "all":
            hashOfOldNames:dict[str, str] = {}
            for i in range(len(command[1])):
                name = command[1][i]
                if name not in varsToKeep:
                    if name not in hashOfOldNames:
                        hashOfOldNames[name] = self.generateNewVarName(name, command[1])
                    command[1][i] = hashOfOldNames[name]
        # add command
        if index is None or index == len(self.commands):
            for var in command[1]:
                if type(var) == str:
                    if var not in self.varNames:
                        self.varNames.append(var)
            self.commands.append(deepcopy(command))
            self.costs.append(cost)
        else:
            for var in command[1]:
                if type(var) == str:
                    if var not in self.varNames:
                        self.varNames.append(var)
            self.commands.insert(index, deepcopy(command))
            self.costs.insert(index, cost)

    def addCommands(self, commands: list[tuple[str, list[str]]] | list[list[str]], costs: list[float]|None = None, varsToKeep:Literal["all"]|list|None = "all", index: int|None = None):
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
            elif type(command[1]) == str:
                commands[i] = (command[0], command[1:len(command)])
            # get vars used in commands
            for var in commands[i][1]:
                if var not in vars:
                    vars.append(var)
        # loop through all commands
        hashOfOldNames:dict[str, str] = {} # to store the names that have already been changed
        for commandCostPair in zip(commands, costs):
            # replace vars that are in self.vars and not in varsToKeep
            command = commandCostPair[0]
            if varsToKeep != "all":
                for i in range(len(command[1])):
                    name = command[1][i]
                    if type(name) == str:
                        if name not in varsToKeep:
                            if name not in hashOfOldNames:
                                hashOfOldNames[name] = self.generateNewVarName(name, vars)
                            command[1][i] = hashOfOldNames[name]
            # add command
            for var in commandCostPair[0][1]:
                if type(var) == str:
                    if var not in self.varNames:
                        self.varNames.append(var)
            self.commands.insert(index, commandCostPair[0])
            self.costs.insert(index, commandCostPair[1])
            index += 1
    
    def addContext(self, context: Context, varsToKeep:Literal["all"]|list|None = "all", index: int = None) -> None:
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
            def correctVarNames(name, line, type, usageType):
                if name not in varsToKeep:
                    if name not in hashOfOldNames:
                        hashOfOldNames[name] = self.generateNewVarName(name, context.varNames)
                    return hashOfOldNames[name]
                return None
            context.iterOverParams(correctVarNames)
        # loop through all commands
        for commandCostPair in context:
            # add command
            for var in commandCostPair[0][1]:
                if type(var) == str:
                    if var not in self.varNames:
                        self.varNames.append(var)
            self.commands.insert(index, commandCostPair[0])
            self.costs.insert(index, commandCostPair[1])
            index += 1

    def removeCommand(self, index: int) -> tuple[tuple[str, list[str]], float]|None:
        if index >= 0 and index < len(self.commands):
            pair = (self.commands[index], self.costs[index])
            del self.commands[index]
            del self.costs[index]
            self.updateVarNames()
            return pair
        return None

    def getCommand(self, index: int) -> tuple[str, list[str]]|None:
        if index >= 0 and index < len(self.commands):
            return self.commands[index]
        return None
    
    def setCost(self, value: float, index: int) -> None:
        if index >= 0 and index < len(self.commands):
            self.costs[index] = value

    def getCost(self, index: int | None = None) -> float|None:
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
                if line[1][i] == nameToReplace:
                    line[1][i] = nameToUse
        self.updateVarNames()

    def replaceVarNames(self, replacementDict:dict):
        for line in self.commands:
            for i in range(len(line[1])):
                if line[1][i] in replacementDict:
                    line[1][i] = replacementDict[line[1][i]]
        self.updateVarNames()

    def replaceVarNamesWithUniqueNames(self, replacementDict:dict):
        def replaceFunc(name, line, type, usageType):
            if name in replacementDict:
                return replacementDict[name]
            elif name in replacementDict.values():
                replacementDict[name] = self.generateNewVarName(name, replacementDict.values())
                return replacementDict[name]
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

    def getJumpLabelPos(self, labelName) -> int:
        if self.labelPositions is not None:
            if labelName in self.labelPositions:
                return self.labelPositions[labelName]
            raise Exception(f"cound not find label {labelName}")
        self.labelPositions = {}
        for i in range(len(self.context)):
            line = self.context.getCommand(line)
            if line[0] == ".":
                self.labelPositions[line[1][0]] = i
        if labelName in self.labelPositions:
            return self.labelPositions[labelName]
        raise Exception(f"cound not find label {labelName}")

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

    def iterInRunOrder(self, iterInRunOrderData:IterInRunOrderData, lineNumber:int = 0, skipDoLineOnFirstLine:bool = True, vistedLines:dict = None):
        if vistedLines is None:
            vistedLines = {}
        while line not in vistedLines:
            vistedLines[line] = True
            line = self.context.getCommand(lineNumber)
            if line is None:
                    break
            if len(vistedLines) > 1 or not skipDoLineOnFirstLine:
                iterInRunOrderData.doLine(line, lineNumber)
            if "program stop" in ILU.getTags_Mnemonic(line[0]):
                break
            elif "force jump" in ILU.getTags_Mnemonic(line[0]):
                lineNumber = self.getJumpLabelPos(line[1][0])
            elif  "maybe jump" in ILU.getTags_Mnemonic(line[0]):
                yield self.iterInRunOrder(iterInRunOrderData.copy(), self.getJumpLabelPos(line[1][0]), False, deepcopy(vistedLines))
        return iterInRunOrderData

    def varNextRead(self, varName:str, startLineNumber:int, vistedLines = None, hitHold = False):
        varAndLabelUsage = self.getVarAndLabelUsage()
        if vistedLines is None:
            vistedLines:dict[int, bool] = {}
        otherPath:None|dict[str, int] = None
        if startLineNumber in vistedLines:
            if otherPath is None:
                return hitHold
            return otherPath
        vistedLines[startLineNumber] = True
        if otherPath is not None:
            if otherPath["steps"] < len(vistedLines):
                if otherPath is None:
                    return hitHold
                return otherPath
        line = self.context.getCommand(startLineNumber)
        if line is None:
            if otherPath is None:
                return hitHold
            return otherPath
        if line[0] == "@":
            if line[1][1] == varName:
                hitHold = True
        else:
            if "program stop" in ILU.getTags_Mnemonic(line[0]):
                if otherPath is None:
                    return hitHold
                return otherPath
            if "force jump" in ILU.getTags_Mnemonic(line[0]):
                startLineNumber = self.getJumpLabelPos(line[1][0])
            elif  "maybe jump" in ILU.getTags_Mnemonic(line[0]):
                labelUsage = varAndLabelUsage[line[1][0]]
                possibleOtherPath = self.varNextRead(varName, self.getJumpLabelPos(line[1][0]), deepcopy(vistedLines), hitHold)
                if otherPath is None:
                    otherPath = possibleOtherPath
                elif otherPath["steps"] > possibleOtherPath:
                    otherPath = possibleOtherPath
                    
        while True:
            startLineNumber += 1
            if startLineNumber in vistedLines:
                if otherPath is None:
                    return hitHold
                return otherPath
            vistedLines[startLineNumber] = True
            if otherPath is not None:
                if otherPath["steps"] < len(vistedLines):
                    if otherPath is None:
                        return hitHold
                    return otherPath
            line = self.context.getCommand(startLineNumber)
            if line is None:
                if otherPath is None:
                    return hitHold
                return otherPath
            if line[0] == "@":
                if line[1][1] == varName:
                    hitHold = True
            else:
                if "program stop" in ILU.getTags_Mnemonic(line[0]):
                    if otherPath is None:
                        return hitHold
                    return otherPath
                if "force jump" in ILU.getTags_Mnemonic(line[0]):
                    startLineNumber = self.getJumpLabelPos(line[1][0])
                elif  "maybe jump" in ILU.getTags_Mnemonic(line[0]):
                    labelUsage = varAndLabelUsage[line[1][0]]
                    possibleOtherPath = self.varNextRead(varName, self.getJumpLabelPos(line[1][0]), deepcopy(vistedLines), hitHold)
                    if otherPath is None:
                        otherPath = possibleOtherPath
                    elif otherPath["steps"] > possibleOtherPath:
                        otherPath = possibleOtherPath
                for i in range(len(line[1])):
                    if line[1][i] == varName:
                        usageType = ILU.getUsageTypes_Mnemonic(line[0])[i]
                        if usageType == "out":
                            if otherPath is None:
                                return hitHold
                            return otherPath
                        elif usageType in ["in", "both"]:
                            if (otherPath is None) or otherPath["steps"] >= len(vistedLines):
                                return {"lineNumber":startLineNumber, "steps":len(vistedLines), "hitHold":hitHold}
                            else:
                                return otherPath

    def varNextWriten(self, varName:str, startLineNumber:int, vistedLines = None):
        varAndLabelUsage = self.getVarAndLabelUsage()
        if vistedLines is None:
            vistedLines:dict[int, bool] = {}
        otherPath:None|dict[str, int] = None
        if startLineNumber in vistedLines:
            return otherPath
        vistedLines[startLineNumber] = True
        if otherPath is not None:
            if otherPath["steps"] < len(vistedLines):
                return otherPath
        line = self.context.getCommand(startLineNumber)
        if line is None:
            return otherPath
        if "program stop" in ILU.getTags_Mnemonic(line[0]):
            return otherPath
        if "force jump" in ILU.getTags_Mnemonic(line[0]):
            labelUsage = varAndLabelUsage[line[1][0]]
            newstartLineNumber = None
            for usage in labelUsage["usage"]:
                if usage["usageType"] == "out":
                    newstartLineNumber = usage["line"]
            if newstartLineNumber is None:
                raise Exception(f"jump label {line[1][0]} not defined. Line {startLineNumber}")
            startLineNumber = newstartLineNumber
        elif  "maybe jump" in ILU.getTags_Mnemonic(line[0]):
            labelUsage = varAndLabelUsage[line[1][0]]
            for usage in labelUsage["usage"]:
                if usage["usageType"] == "out":
                    possibleOtherPath = self.varNextRead(varName, usage["line"], deepcopy(vistedLines))
                    if otherPath is None:
                        otherPath = possibleOtherPath
                    elif otherPath["steps"] > possibleOtherPath:
                        otherPath = possibleOtherPath
        while True:
            startLineNumber += 1
            if startLineNumber in vistedLines:
                return otherPath
            vistedLines[startLineNumber] = True
            if otherPath is not None:
                if otherPath["steps"] < len(vistedLines):
                    return otherPath
            line = self.context.getCommand(startLineNumber)
            if line is None:
                return otherPath
            if "program stop" in ILU.getTags_Mnemonic(line[0]):
                return otherPath
            if "force jump" in ILU.getTags_Mnemonic(line[0]):
                labelUsage = varAndLabelUsage[line[1][0]]
                newstartLineNumber = None
                for usage in labelUsage["usage"]:
                    if usage["usageType"] == "out":
                        newstartLineNumber = usage["line"]
                if newstartLineNumber is None:
                    raise Exception(f"jump label {line[1][0]} not defined. Line {startLineNumber}")
                startLineNumber = newstartLineNumber
            elif  "maybe jump" in ILU.getTags_Mnemonic(line[0]):
                labelUsage = varAndLabelUsage[line[1][0]]
                for usage in labelUsage["usage"]:
                    if usage["usageType"] == "out":
                        possibleOtherPath = self.varNextRead(varName, usage["line"], deepcopy(vistedLines))
                        if otherPath is None:
                            otherPath = possibleOtherPath
                        elif otherPath["steps"] > possibleOtherPath:
                            otherPath = possibleOtherPath
            for i in range(len(line[1])):
                if line[1][i] == varName:
                    usageType = ILU.getUsageTypes_Mnemonic(line[0])[i]
                    if usageType in ["out", "both"]:
                        if (otherPath is None) or otherPath["steps"] >= len(vistedLines):
                            return {"lineNumber":startLineNumber, "steps":len(vistedLines)}
                        else:
                            return otherPath


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
