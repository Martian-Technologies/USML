from __future__ import annotations
import os
# import json
import importlib
import pathlib
# from copy import copy, deepcopy
from instructions.instruction import Instruction

class LookUp:
    def __init__(self) -> None:
        self.nameToMnemonic = {}
        self.mnemonicToName = {}
        self.nameToClass = {}
        # self.nameToImplementations:dict[str, list[list[tuple[str, list[str]]]]] = {}
        src = pathlib.Path("src")
        instructions_path = src / 'instructions'
        classFiles = [f for f in os.listdir(instructions_path) if os.path.isfile(instructions_path / f)]
        for className in classFiles:
            className = className[0:-3]
            module = importlib.import_module("instructions." + className)
            classObj:type[Instruction] = getattr(module, "".join([i.capitalize() for i in className.split()]))
            self.nameToMnemonic[classObj.name] = classObj.mnemonic
            self.mnemonicToName[classObj.mnemonic] = classObj.name
            self.nameToClass[classObj.name] = classObj
        # with open(src / 'Costs.json') as f:
            # self.nameToCost:dict[str, float] = json.load(f)
        # with open(pathlib.Path(src / 'Implementations.json')) as f:
            # implementations:dict[str, list[list[list[str]]]] = json.load(f)
            # for name in implementations.keys():
            #     self.nameToImplementations[name] = []
            #     for implementation in implementations[name]:
            #         self.nameToImplementations[name].append([])
            #         for instructionData in implementation:
            #             if instructionData[0][0] == "." and len(instructionData[0]) != 1:
            #                 self.nameToImplementations[name][-1].append(
            #                     (
            #                         "Label",
            #                         [instructionData[0][1 : len(instructionData[0])]]
            #                         )
            #                     )
            #             else:
            #                 self.nameToImplementations[name][-1].append(
            #                     (
            #                         self.getName(instructionData[0]),
            #                         instructionData[1 : len(instructionData)]
            #                     )
            #                 )

    def getName(self, mnemonic: str) -> str:
        """
        Used to get the name of the instruction associated with the mnemonic (mnemonic)

        Args:
            mnemonic (str): The mnemonic associated instruction

        Returns:
            name str: The name of the instruction
        """
        return self.mnemonicToName[mnemonic]

    def getMnemonic(self, name: str):
        """
        Used to get the mnemonic associated with the instruction named (name)

        Args:
            name (str): The name of the instruction

        Returns:
            mnemonic (str): The mnemonic associated instruction
        """
        return self.nameToMnemonic[name]

    def getClass(self, name: str) -> type[Instruction]:
        """
        Used to get the class of the instruction named (name)

        Args:
            name (str): The name of the instruction

        Returns:
            class (type[Instruction]): The class of the instruction
        """
        return self.nameToClass[name]

    # def getCost(self, name: str):
    #     """
    #     Used to get the cost of the instruction named (name)\n
    #     Costs are definded in "Cost.json"

    #     Args:
    #         name (str): The name of the instruction

    #     Returns:
    #         cost (float): The cost of the instruction
    #     """
    #     if name == "Defalt":
    #         return None
    #     return self.nameToCost[name]

    # def getImplementations(self, name:str) -> list[list[tuple[str, list[str]]]] | None:
    #     """
    #     Used to get all the possible implementations of an instruction named (name)

    #     Args:
    #         name (str): The name of the instruction

    #     Returns:
    #         implementations (list): All the possible implementations of the instruction
    #     """
    #     if name == "Defalt" or name not in self.nameToImplementations.keys():
    #         return None
    #     return self.nameToImplementations[name]

    # def getBestCost(self, instructionName:str, context:list[str], usedInstructions:list[str] = None) -> tuple[list[tuple[str, list[str]]], float]:
    #     """
    #     Used to get the best possible implementation of an instruction named (name) in the given context (context)

    #     Args:
    #         instructionName (str): The name of the instruction
    #         context (idk what this will be): The context the command is used in. This is for more complex cost functions that need to know what other commands are around this one.
    #         usedInstructions (list[str]): Used when running recusively to stop circular implementations. Defaults to None.

    #     Returns:
    #         (list): The best possible implementation of the instruction
    #         (float): The cost of that implementation
    #     """
    #     if usedInstructions == None:
    #         usedInstructions = [instructionName]
    #     else:
    #         usedInstructions.append(instructionName)
    #     bestCost:float = None
    #     bestSource:list[tuple[str, list[str]]] = {}
    #     for implementation in self.getImplementations(instructionName):
    #         if implementation[0][0] == instructionName:
    #             cost = self.getClass(instructionName).getCostIfAdded(instructionName, context)
    #             if bestCost == None or bestCost >= cost:
    #                 bestCost = cost
    #                 bestSource = deepcopy(implementation)
    #             continue
    #         canDoImplementation = True
    #         for opp in implementation:
    #             if opp[0] in usedInstructions:
    #                 canDoImplementation = False
    #                 break
    #         if not canDoImplementation:
    #             continue
    #         cost = 0
    #         source:list = []
    #         for opp in implementation:
    #             oppSource, oppCost = self.getBestCost(opp[0], context + source, copy(usedInstructions))
    #             if oppCost == None:
    #                 canDoImplementation = False
    #                 break
    #             for oppCommand in oppSource:
    #                 params = oppCommand[1]
    #                 for i in range(len(params)):
    #                     param = params[i]
    #                     if param[0:4] == "PARAM" and param[4:len(param)].isnumeric():
    #                         params[i] = opp[1][int(param[4:len(param)])-1]
    #             if type(oppSource) == str:
    #                 source.append(oppSource)
    #             else:
    #                 source.extend(oppSource)
    #             cost += oppCost
    #             if bestCost != None and cost >= bestCost:
    #                 canDoImplementation = False
    #                 break
    #         if (bestCost == None or bestCost > cost) and canDoImplementation:
    #             bestCost = cost
    #             bestSource = source
    #     if bestCost == None:
    #         print("could not find cost for instruction " + instructionName)
    #     return deepcopy(bestSource), bestCost
