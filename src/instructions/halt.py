from instructions import instruction

class Halt(instruction.Instruction):
    name = "Halt"
    mnemonic = "HLT"
    
    def __init__(self):
        super().__init__()
