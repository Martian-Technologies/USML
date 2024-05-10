from __future__ import annotations
import os
import json
import importlib
import pathlib
from copy import copy, deepcopy
from instructions.instruction import Instruction


nameToMnemonic = {}
mnemonicToName = {}
nameToClass = {}
nameToImplementations:dict[str, list[list[tuple[str, list[str]]]]] = {}
src = pathlib.Path("src")
instructions_path = src / 'instructions'
classFiles = [f for f in os.listdir(instructions_path) if os.path.isfile(instructions_path / f)]
for className in classFiles:
    className = className[0:-3]
    module = importlib.import_module("instructions." + className)
    classObj:type[Instruction] = getattr(module, "".join([i.capitalize() for i in className.split()]))
    nameToMnemonic[classObj.name] = classObj.mnemonic
    mnemonicToName[classObj.mnemonic] = classObj.name
    nameToClass[classObj.name] = classObj

@staticmethod
def getName(mnemonic: str) -> str:
    """
    Used to get the name of the instruction associated with the mnemonic (mnemonic)

    Args:
        mnemonic (str): The mnemonic associated instruction

    Returns:
        name str: The name of the instruction
    """
    return mnemonicToName[mnemonic]

@staticmethod
def getMnemonic(name: str):
    """
    Used to get the mnemonic associated with the instruction named (name)

    Args:
        name (str): The name of the instruction

    Returns:
        mnemonic (str): The mnemonic associated instruction
    """
    return nameToMnemonic[name]

@staticmethod
def getClass(name: str) -> type[Instruction]:
    """
    Used to get the class of the instruction named (name)

    Args:
        name (str): The name of the instruction

    Returns:
        class (type[Instruction]): The class of the instruction
    """
    return nameToClass[name]

with open(src / 'Costs.json') as f:
    nameToCost: dict[str, float] = json.load(f)

@staticmethod
def getCost(name: str):
    """
    Used to get the cost of the instruction named (name)\n
    Costs are definded in "Cost.json"

    Args:
        name (str): The name of the instruction

    Returns:
        cost (float): The cost of the instruction
    """
    if name == "Defalt":
        return None
    return nameToCost[name]

with open(pathlib.Path(src / 'Implementations.json')) as f:
    implementations: dict[str, list[list[list[str]]]] = json.load(f)
    for name in implementations.keys():
        nameToImplementations[name] = []
        for implementation in implementations[name]:
            nameToImplementations[name].append([])
            for instructionData in implementation:
                if instructionData[0][0] == "." and len(instructionData[0]) != 1:
                    nameToImplementations[name][-1].append(
                        (
                            "Label",
                            [instructionData[0][1 : len(instructionData[0])]]
                            )
                        )
                else:
                    nameToImplementations[name][-1].append(
                        (
                            getName(instructionData[0]),
                            instructionData[1 : len(instructionData)]
                        )
                    )

@staticmethod
def getImplementations(name:str) -> list[list[tuple[str, list[str]]]] | None:
    """
    Used to get all the possible implementations of an instruction named (name)

    Args:
        name (str): The name of the instruction

    Returns:
        implementations (list): All the possible implementations of the instruction
    """
    if name == "Defalt" or name not in nameToImplementations.keys():
        return None
    return nameToImplementations[name]

def getBestCost(instructionName:str, context:list[str], usedInstructions:list[str] = None) -> tuple[list[tuple[str, list[str]]], float]:
    """
    Used to get the best possible implementation of an instruction named (name) in the given context (context)

    Args:
        instructionName (str): The name of the instruction
        context (idk what this will be): The context the command is used in. This is for more complex cost functions that need to know what other commands are around this one.
        usedInstructions (list[str]): Used when running recusively to stop circular implementations. Defaults to None.

    Returns:
        (list): The best possible implementation of the instruction
        (float): The cost of that implementation
    """
    if usedInstructions == None:
        usedInstructions = [instructionName]
    else:
        usedInstructions.append(instructionName)
    bestCost:float = None
    bestSource:list[tuple[str, list[str]]] = {}
    for implementation in getImplementations(instructionName):
        if implementation[0][0] == instructionName:
            cost = getClass(instructionName).getCostIfAdded(instructionName, context)
            if bestCost == None or bestCost >= cost:
                bestCost = cost
                bestSource = deepcopy(implementation)
            continue
        canDoImplementation = True
        for opp in implementation:
            if opp[0] in usedInstructions:
                canDoImplementation = False
                break
        if not canDoImplementation:
            continue
        cost = 0
        source:list = []
        for opp in implementation:
            oppSource, oppCost = getBestCost(opp[0], context + source, copy(usedInstructions))
            if oppCost == None:
                canDoImplementation = False
                break
            for oppCommand in oppSource:
                prams = oppCommand[1]
                for i in range(len(prams)):
                    pram = prams[i]
                    if pram[0:4] == "PRAM" and pram[4:len(pram)].isnumeric():
                        prams[i] = opp[1][int(pram[4:len(pram)])-1]
            if type(oppSource) == str:
                source.append(oppSource)
            else:
                source.extend(oppSource)
            cost += oppCost
            if bestCost != None and cost >= bestCost:
                canDoImplementation = False
                break
        if (bestCost == None or bestCost > cost) and canDoImplementation:
            bestCost = cost
            bestSource = source
    if bestCost == None:
        print("could not find cost for instruction " + instructionName)
    return deepcopy(bestSource), bestCost
