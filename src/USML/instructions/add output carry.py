from USML.instructions.instruction import Instruction
from USML.bitString import BitString

class AddOutputCarry(Instruction):
    name = "Add Output Carry"
    mnemonic = "ADDC"
    description = "Adds variables 1 and 2 together and stores it in variable 3. The carry flag is stored in variable 4."
    expectedDataType = ["var", "var", "var", "var"]
    usageTypes = ["in", "in", "out", "out"]
    tags = []

    @staticmethod
    def run(params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        sum = memory[params[0]]["value"].getInt() + memory[params[1]]["value"].getInt()
        memory[params[2]]["value"].setInt(sum)
        memory[params[3]]["value"].setInt(int(sum > memory[params[2]]["value"].maxIntValue()))

    @staticmethod
    def getImplementations() -> list[list[list[str]]]:
        return [
            [["ADDC", "PARAM1", "PARAM2", "PARAM3", "PARAM4"]],
            [
                ["ADD", "PARAM1", "PARAM2", "PARAM3"],
                ["GRT", "PARAM1" "PARAM3", "PARAM4"],
            ]
        ]