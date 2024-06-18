from __future__ import annotations
import os
import importlib
import pathlib
from USML.instructions.instruction import Instruction

class LookUp:
    lookUp = None
    
    def __init__(self) -> None:
        LookUp.lookUp = self
        self.nameToMnemonic = {}
        self.mnemonicToName = {}
        self.nameToexpectedDataType = {}
        self.nameTousageTypes = {}
        self.nameToClass = {}
        # self.nameToImplementations:dict[str, list[list[tuple[str, list[str]]]]] = {}
        src = pathlib.Path("src")
        instructions_path = src / 'USML' / 'instructions'
        classFiles = [f for f in os.listdir(instructions_path) if os.path.isfile(instructions_path / f)]
        for className in classFiles:
            className = className[0:-3]
            module = importlib.import_module("USML.instructions." + className)
            classObj:type[Instruction] = getattr(module, "".join([i.capitalize() for i in className.split()]))
            self.nameToMnemonic[classObj.name] = classObj.mnemonic
            self.mnemonicToName[classObj.mnemonic] = classObj.name
            self.nameToexpectedDataType[classObj.name] = classObj.expectedDataType
            self.nameTousageTypes[classObj.name] = classObj.usageTypes
            self.nameToClass[classObj.name] = classObj

    def getName(self, mnemonic: str) -> str:
        """
        Used to get the name of the instruction associated with the mnemonic (mnemonic)

        Args:
            mnemonic (str): The mnemonic associated instruction

        Returns:
            name str: The name of the instruction
        """
        return self.mnemonicToName[mnemonic]

    def getMnemonic(self, name: str) -> str:
        """
        Used to get the mnemonic associated with the instruction named (name)

        Args:
            name (str): The name of the instruction

        Returns:
            mnemonic (str): The mnemonic associated instruction
        """
        return self.nameToMnemonic[name]

    def getexpectedDataType(self, name: str):
        """
        Used to get the expectedDataType of the instruction named (name)

        Args:
            name (str): The name of the instruction

        Returns:
            expectedDataType (list[str]): A list of the expected data types for the instruction [list of "var", "num", "label"]
        """

    def getusageTypes(self, name: str) -> list[str]:
        """
        Used to get the usageTypes of the instruction named (name)

        Args:
            name (str): The name of the instruction

        Returns:
            usageTypes (list[str]): A list of the usage types for the instruction [list of "in", "out", "both"]
        """

    def getClass(self, name: str) -> Instruction:
        """
        Used to get the class of the instruction named (name)

        Args:
            name (str): The name of the instruction

        Returns:
            class (Instruction): A instances of the instruction
        """
        return self.nameToClass[name]()

if LookUp.lookUp == None:
    LookUp()