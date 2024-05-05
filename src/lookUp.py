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
nameToImplementations:dict[str, list[list[tuple[str, list[str]] | "str"] | str]] = {}

classFiles = [f for f in os.listdir(pathlib.Path("src\instructions")) if os.path.isfile(pathlib.Path("src\instructions" + "/"+f))]
for className in classFiles:
    className = className[0:-3]
    module = importlib.import_module("instructions." + className)
    classObj:type[Instruction] = getattr(module, "".join([i.capitalize() for i in className.split()]))
    nameToMnemonic[classObj.name] = classObj.mnemonic
    mnemonicToName[classObj.mnemonic] = classObj.name
    nameToClass[classObj.name] = classObj

@staticmethod
def getName(mnemonic: str):
    return mnemonicToName[mnemonic]

@staticmethod
def getMnemonic(name: str):
    return nameToMnemonic[name]

@staticmethod
def getClass(name: str) -> type[Instruction]:
    return nameToClass[name]

with open(pathlib.Path("src/Costs.json")) as f:
    nameToCost: dict[str, float] = json.load(f)

@staticmethod
def getCost(name: str):
    if name == "Defalt":
        return None
    return nameToCost[name]

with open(pathlib.Path("src/Implementations.json")) as f:
    implementations: dict[str, list[list[tuple[str, list]]]] = json.load(f)
    for name in implementations.keys():
        nameToImplementations[name] = []
        for implementation in implementations[name]:
            nameToImplementations[name].append([])
            for instructionData in implementation:
                if instructionData[0][0] == "." and len(instructionData[0]) != 1:
                    nameToImplementations[name][-1].append(
                        (
                            "Label",
                            instructionData[0][1:len(instructionData[0])]
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
def getImplementations(name):
    if name == "Defalt":
        return None
    return nameToImplementations[name]

def getBestCost(instructionName:str, context:list[Instruction], usedInstructions:list[str] = None) -> tuple[list[str] | str, float]:
    if usedInstructions == None:
        usedInstructions = []
    bestCost:float = None
    bestSource:list[tuple[str, list[str]]] = {}
    for implementation in getImplementations(instructionName):
        if implementation[0][0] == instructionName:
            cost = getClass(instructionName).getCostIfAdded(instructionName, context)
            if bestCost == None or bestCost >= cost:
                bestCost = cost
                bestSource = copy(implementation)
        else:
            canDoImplementation = True
            for opp in implementation:
                if opp[0] in usedInstructions:
                    canDoImplementation = False
                    break
            if canDoImplementation:
                cost = 0
                source:list = []
                for opp in implementation:
                    oppSource, oppCost = getBestCost(opp[0], context + source, usedInstructions + [opp[0]])
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
