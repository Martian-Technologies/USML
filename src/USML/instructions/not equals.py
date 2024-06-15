from USML.instructions import instruction
from USML.bitString import BitString

class NotEquals(instruction.Instruction):
    name =  "Not Equals"
    mnemonic = "NEQU"
    expectedParams = ['var', 'var', 'var']
    
    def __init__(self):
        super().__init__()

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[2]]["value"].setInt(int(memory[params[0]]["value"].getInt() != memory[params[1]]["value"].getInt()))

    def getImplementations(self) -> list[list[list[str]]]:
        return [
            [["NEQU", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["EQU", "PARAM1", "PARAM2", "PARAM3"],
                ["NOT", "PARAM3", "PARAM3"]
            ]
        ]