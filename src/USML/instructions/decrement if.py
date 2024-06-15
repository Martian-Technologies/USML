from USML.instructions import instruction

class DecrementIf(instruction.Instruction):
    name =  "Decrement If"
    mnemonic = "DECI"
    
    def __init__(self):
        super().__init__()

    def run(self, params):
        raise Exception(f"Failed running instruction {self.name}")

    def getImplementations(self):
        return[
            [["DECI", "PARAM1", "PARAM2", "PARAM3"]],
            [
                ["JMIFN", "NoDec", "PARAM3"],
                ["INC", "PARAM1", "PARAM2"],
                [".NoDec"]
            ]
        ]