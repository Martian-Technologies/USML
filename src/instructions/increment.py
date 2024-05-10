from instructions import instruction

class Increment(instruction.Instruction):
    name =  "Increment"
    mnemonic = "INC"
    
    def __init__(self):
        super().__init__()
