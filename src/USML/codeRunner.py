from USML.context import Context
from USML.lookUp import LookUp
from USML.instructions.instruction import Instruction
from random import randint
from USML.bitString import BitString

class CodeRunner:
    def __init__(self, code:Context, bitCount:int = 8) -> None:
        self.code:Context = code
        self.vars:dict[str, dict[str, BitString|str|int]] = {}
        self.instructionPointer:int = 0
        self.lastInstructionPointer:None|int = None
        self.lookup:LookUp = LookUp()
        self.bitCount = bitCount
        self.findLabels()

    def run(self, debug=False):
        while self.stepCode():
            if debug:
                print(self)

    def stepCode(self):
        self.lastInstructionPointer = self.instructionPointer
        command = None
        while command == None:
            if self.instructionPointer >= len(self.code):
                return None
            couldBeCommand = self.code.getCommand(self.instructionPointer)
            if couldBeCommand[0] != ".":
                command = couldBeCommand
            else:
                self.instructionPointer += 1
        commandClass:Instruction = self.lookup.getClass(self.lookup.getName(command[0]))
        commandShouldBeParamTypes:list[str] = commandClass.getExpectedParams()
        params = command[1]
        for i in range(len(params)):
            param = params[i]
            if param in self.vars:
                paramType = self.vars[param]["type"]
                if commandShouldBeParamTypes[i] != paramType:
                    raise Exception(
                        f"Param {i + 1} in {command} on line {self.instructionPointer} not correct type.It is {paramType} which it should be {commandShouldBeParamTypes[i]}"
                        )
            else:
                if commandShouldBeParamTypes[i] == "var":
                    if type(param) != str:
                        raise Exception(
                            f"Var {i + 1} in {command} on line {self.instructionPointer} not correct type. It is {type(param)} which it should be str"
                            )
                    self.vars[param] = {"type": commandShouldBeParamTypes[i], "value":BitString.randomized(self.bitCount)}
                elif commandShouldBeParamTypes[i] == "label":
                    if type(param) != str:
                        raise Exception(
                            f"Label {i + 1} in {command} on line {self.instructionPointer} not correct type. It is {type(param)} which it should be str"
                            )
                    raise Exception(f"Label {i + 1} in {command} on line {self.instructionPointer} is not defined.")
        newPointer = commandClass.run(params, self.vars)
        if newPointer == "END":
            self.instructionPointer = len(self.code) - 1
        elif newPointer != None:
            self.instructionPointer = newPointer
        self.instructionPointer += 1
        return True

    def findLabels(self):
        for i in range(len(self.code)):
            command = self.code.getCommand(i)
            if command[0] == ".":
                if len(command[1]) == 1:
                    label = command[1][0]
                    if type(label) != str:
                        raise Exception(
                            f"Param {i + 1} in {command} on line {self.ininstructionPointerst} not correct type. It is {type(label)} which it should be str"
                            )
                    if label in self.vars: # there should only be labels in this at this point
                        raise Exception(f"Cant have labels with the same names. Line {i} and line {self.vars[label]['value']}")
                    self.vars[label] = {"type": "label", "value":i}
                else:
                    raise Exception(f"Invalid label params {command[0]} on line {i}")
    
    def __str__(self) -> str:
        string = str(self.code)
        string += "---- info ----\n"
        string += f"Last Line: {self.lastInstructionPointer}\n"
        string += f"Next Line: {self.instructionPointer}\n"
        string += "---- VARS ----\n"
        for varName in self.vars:
            if self.vars[varName]["type"] == "var":
                string += f"{varName} : {self.vars[varName]['value']}\n"
        return string
                    
