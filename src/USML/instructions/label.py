from USML.instructions import instruction
from USML.bitString import BitString

class Label(instruction.Instruction):
    name = "Label"
    mnemonic = "."
    description = "A label for the program to jump to. Does nothing."
    expectedDataType = ["label"]
    usageTypes = ["out"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        raise Exception(f"Tried to run label {params[0]}. Labels should not be run.")

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [[[".", "PARAM1"]]]