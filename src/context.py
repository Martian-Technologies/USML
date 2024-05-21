from __future__ import annotations
from collections.abc import Iterable
from copy import deepcopy
from pram.pram import Pram

class Context:
    def __init__(self) -> None:
        self.commands:list[tuple[str, list[Pram]]] = []

    def addCommand(self, command:tuple[str, list[Pram]], index:int = None):
        if index == None or index == len(self.commands):
            self.commands.append(deepcopy(command()))
        else:
            self.commands.insert(deepcopy(command), index)

    def addContext(self, context:Context, index:int = None):
        if index == None:
            index = 0
        for command in context.getIter():
            self.commands.insert(deepcopy(command), index)
            index += 1

    def removeCommand(self, index:int):
        if index >= 0 and index < len(self.commands):
            del self.commands[index]

    def getCommand(self, index:int) -> tuple[str, list[Pram]]:
        if index >= 0 and index < len(self.commands):
            return self.commands[index]
        
    def copy(self):
        newContext = Context()
        newContext.addContext(self)
        return newContext

    def getIter(self) -> Iterable[tuple[str, list[Pram]]]:
        return self.commands