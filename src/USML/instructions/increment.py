from USML.instructions import instruction
from USML.bitString import BitString

class Increment(instruction.Instruction):
    name =  "Increment"
    mnemonic = "INC"
    expectedParams = ['var']
    
    def __init__(self):
        super().__init__()

    def run(self, params:tuple[str|float], memory:dict[str, dict[str, BitString|str|int]]) -> None|int:
        memory[params[0]]["value"].setInt(memory[params[0]]["value"].getInt() + 1)

    def getImplementations(self) -> list[list[list[str]]]:
        return [
            [["INC", "PARAM1"]],
            [
                ["SET", "one", "1"],
                ["INCI", "PARAM1", "one"]
            ],
            [
                ["SET", "one", "1"],
                ["ADD", "PARAM1", "one", "PARAM1"]
            ]
        ]