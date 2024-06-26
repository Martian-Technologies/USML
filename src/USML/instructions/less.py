from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class Less(Instruction):
    name =  "Less"
    mnemonic = "LES"
    description = "Sets the value of variable 3 to 1 if the value of variable 1 is less than the value of variable 2, otherwise sets it to 0."
    expectedDataType = ["var", "var", "var"]
    usageTypes = ["in", "in", "out"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[2]]["value"].setInt(int(memory[params[0]]["value"].getInt() < memory[params[1]]["value"].getInt()))

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["LES", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["GOE", "PARAM1", "PARAM2", "PARAM3"],
                ["NOT", "PARAM3", "PARAM3"]
            ]
        ]