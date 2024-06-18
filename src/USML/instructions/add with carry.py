from USML.instructions import instruction
from USML.bitString import BitString

class AddWithCarry(instruction.Instruction):
    name = "Add With Carry"
    mnemonic = "ADDC"
    expectedDataType = ["var", "var", "var", "var"]
    usageTypes = ["in", "in", "out", "out"]

    def __init__(self):
        super().__init__()

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        sum = memory[params[0]]["value"].getInt() + memory[params[1]]["value"].getInt()
        memory[params[2]]["value"].setInt(sum)
        memory[params[3]]["value"].setInt(int(sum > memory[params[2]]["value"].maxIntValue()))

    def getImplementations(self) -> list[list[list[str]]]:
        return [[["ADDC", "PARAM1", "PARAM2", "PARAM3", "PARAM4"]]]