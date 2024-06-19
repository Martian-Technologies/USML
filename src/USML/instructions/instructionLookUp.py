from __future__ import annotations
import os
import importlib
import pathlib
from USML.instructions.instruction import Instruction


src = pathlib.Path("src")
instructions_path = src / 'USML' / 'instructions'

class InstructionLookUp:    
    nameToMnemonic = {}
    mnemonicToName = {}
    nameToExpectedDataType = {}
    nameToUsageTypes = {}
    nameToTages = {}
    nameToClass = {}
    mnemonicToExpectedDataType = {}
    mnemonicToUsageTypes = {}
    mnemonicToTages = {}
    mnemonicToClass = {}
    classFiles = [f for f in os.listdir(instructions_path) if (os.path.isfile(instructions_path / f) and f != "instructionLookUp.py")]
    for className in classFiles:
        className = className[0:-3]
        module = importlib.import_module("USML.instructions." + className)
        classObj:type[Instruction] = getattr(module, "".join([i.capitalize() for i in className.split()]))
        nameToMnemonic[classObj.name] = classObj.mnemonic
        mnemonicToName[classObj.mnemonic] = classObj.name
        nameToExpectedDataType[classObj.name] = classObj.expectedDataType
        nameToUsageTypes[classObj.name] = classObj.usageTypes
        nameToTages[classObj.name] = classObj.tags
        nameToClass[classObj.name] = classObj
        mnemonicToExpectedDataType[classObj.mnemonic] = classObj.expectedDataType
        mnemonicToUsageTypes[classObj.mnemonic] = classObj.usageTypes
        mnemonicToTages[classObj.mnemonic] = classObj.tags
        mnemonicToClass[classObj.mnemonic] = classObj

    def getName(mnemonic: str) -> str:
        """
        Used to get the name of the instruction associated with the mnemonic (mnemonic)

        Args:
            mnemonic (str): The mnemonic associated instruction

        Returns:
            name str: The name of the instruction
        """
        return InstructionLookUp.mnemonicToName[mnemonic]

    def getMnemonic(name: str) -> str:
        """
        Used to get the mnemonic associated with the instruction named (name)

        Args:
            name (str): The name of the instruction

        Returns:
            mnemonic (str): The mnemonic associated instruction
        """
        return InstructionLookUp.nameToMnemonic[name]

    def getExpectedDataType_Name(name: str):
        """
        Used to get the expectedDataType of the instruction named (name)

        Args:
            name (str): The name of the instruction

        Returns:
            expectedDataType (list[str]): A list of the expected data types for the instruction [list of "var", "num", "label"]
        """
        return InstructionLookUp.nameToExpectedDataType[name]

    def getUsageTypes_Name(name: str) -> list[str]:
        """
        Used to get the usageTypes of the instruction named (name)

        Args:
            name (str): The name of the instruction

        Returns:
            usageTypes (list[str]): A list of the usage types for the instruction [list of "in", "out", "both"]
        """
        return InstructionLookUp.nameToUsageTypes[name]

    def getTags_Name(name: str) -> list[str]:
        """
        Used to get the tags of the instruction named (name)

        Args:
            name (str): The name associated instruction

        Returns:
            tags (list[str]): A list of tags that are assigned to the instruction
        """
        return InstructionLookUp.mnemonicToUsageTypes[name]

    def getClass_Name(name: str) -> Instruction:
        """
        Used to get the class of the instruction named (name)

        Args:
            name (str): The name of the instruction

        Returns:
            class (Instruction): A instances of the instruction
        """
        return InstructionLookUp.nameToClass[name]()

    def getExpectedDataType_Mnemonic(mnemonic: str):
        """
        Used to get the expectedDataType of the instruction associated with the mnemonic (mnemonic)

        Args:
            mnemonic (str): The mnemonic associated instruction

        Returns:
            expectedDataType (list[str]): A list of the expected data types for the instruction [list of "var", "num", "label"]
        """
        return InstructionLookUp.mnemonicToExpectedDataType[mnemonic]

    def getUsageTypes_Mnemonic(mnemonic: str) -> list[str]:
        """
        Used to get the usageTypes of the instruction associated with the mnemonic (mnemonic)

        Args:
            mnemonic (str): The mnemonic associated instruction

        Returns:
            usageTypes (list[str]): A list of the usage types for the instruction [list of "in", "out", "both"]
        """
        return InstructionLookUp.mnemonicToUsageTypes[mnemonic]

    def getTags_Mnemonic(mnemonic: str) -> list[str]:
        """
        Used to get the tags of the instruction associated with the mnemonic (mnemonic)

        Args:
            mnemonic (str): The mnemonic associated instruction

        Returns:
            tags (list[str]): A list of tags that are assigned to the instruction
        """
        return InstructionLookUp.mnemonicToUsageTypes[mnemonic]

    def getClass_Mnemonic(mnemonic: str) -> Instruction:
        """
        Used to get the class of the instruction associated with the mnemonic (mnemonic)

        Args:
            mnemonic (str): The mnemonic associated instruction
        
        Returns:
            class (Instruction): A instances of the instruction
        """
        return InstructionLookUp.mnemonicToClass[mnemonic]()
ILU = InstructionLookUp