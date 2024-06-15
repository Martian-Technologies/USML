from __future__ import annotations
import os
import importlib
import pathlib
from USML.instructions.instruction import Instruction

class LookUp:
    def __init__(self) -> None:
        self.nameToMnemonic = {}
        self.mnemonicToName = {}
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

    def getMnemonic(self, name: str):
        """
        Used to get the mnemonic associated with the instruction named (name)

        Args:
            name (str): The name of the instruction

        Returns:
            mnemonic (str): The mnemonic associated instruction
        """
        return self.nameToMnemonic[name]

    def getClass(self, name: str) -> Instruction:
        """
        Used to get the class of the instruction named (name)

        Args:
            name (str): The name of the instruction

        Returns:
            class (Instruction): A instances of the instruction
        """
        return self.nameToClass[name]()
