from __future__ import annotations
from copy import deepcopy


class Context:
    def __init__(self) -> None:
        self.commands: list[tuple[str, list[str]]] = []
        self.costs: list[float] = []

    def addContext(self, context: Context, index: int = None) -> None:
        if index == None:
            index = len(self.commands) + 1
        count = len(context)
        i = 0
        for commandCostPair in context:
            if i >= count:
                break
            self.commands.insert(index, deepcopy(commandCostPair[0]))
            self.costs.insert(index, deepcopy(commandCostPair[1]))
            index += 1
            i += 1

    def addCommand(self, command: tuple[str, list[str]] | list[list[str]], cost: float = None, index: int|None = None) -> None:
        if len(command) == 1:
            command = (command[0], [])
        elif type(command[1]) == str:
            command = (command[0], command[1:len(command)])
        if index == None or index == len(self.commands):
            self.commands.append(deepcopy(command))
            self.costs.append(cost)
        else:
            self.commands.insert(index, deepcopy(command))
            self.costs.insert(index, cost)

    def addCommands(self, commands: list[tuple[str, list[str]]] | list[list[str]], costs: list[float]|None = None, index: int|None = None):
        if index == None:
            index = len(self.commands)
        if costs == None:
            costs = []
        while len(costs) < len(commands):
            costs.append(None)
        for commandCostPair in zip(commands, costs):
            command = commandCostPair[0]
            if len(command) == 1:
                command = (command[0], [])
            elif type(command[1]) == str:
                command = (command[0], command[1:len(command)])
            self.commands.insert(index, deepcopy(command))
            self.costs.insert(index, commandCostPair[1])
            index += 1

    def removeCommand(self, index: int) -> tuple[tuple[str, list[str]], float]:
        if index >= 0 and index < len(self.commands):
            pair = (self.commands[index], self.costs[index])
            del self.commands[index]
            del self.costs[index]
            return pair

    def getCommand(self, index: int) -> tuple[str, list[str]]:
        if index >= 0 and index < len(self.commands):
            return self.commands[index]

    def setCost(self, value: float, index: int) -> None:
        if index >= 0 and index < len(self.commands):
            self.costs[index] = value

    def getCost(self, index: int | None = None) -> float:
        if index == None:
            cost = 0
            for c in self.costs:
                if c != None:
                    cost += c
            return cost
        if index >= 0 and index < len(self.commands):
            return self.costs[index]

    def copy(self):
        newContext = Context()
        newContext.addContext(self)
        return newContext

    def __copy__(self):
        c = Context()
        c.addContext(self)
        return c

    def __len__(self):
        return len(self.commands)

    def __iter__(self):
        return zip(self.commands, self.costs).__iter__()

    def __str__(self):
        string = ""
        string += " L | C |                 |\n"
        string += " I | O |                 |\n"
        string += " N | S |  C O M M A N D  |   P R A M S\n"
        string += " E | T |                 |\n"
        string += "---+---+-----------------+------------+------------+------------+------------+------------+\n"
        i = 0
        while i < len(self.commands):
            cost = self.costs[i]
            if cost == None:
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
                string += " " + item + (11 - len(item)) * " "
                ii += 1
            string += "\n"
            i += 1
        return string
    