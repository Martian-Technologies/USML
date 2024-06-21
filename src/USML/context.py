from __future__ import annotations
from typing import Literal
from copy import deepcopy

from USML.instructions.instructionLookUp import ILU


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
                    newName = functionToRun(
                        name,
                        lineNumber,
                        ILU.getExpectedDataType_Mnemonic(command[0])[i],
                        ILU.getUsageTypes_Mnemonic(command[0])[i]
                    )
                    if newName is not None:
                        command[1][i] = newName

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
    