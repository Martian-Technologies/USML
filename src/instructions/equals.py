from instructions import instruction

class Equals(instruction.Instruction):
    name = "Equals"
    mnemonic = "EQU"
    
    def __init__(self):
        super().__init__()
