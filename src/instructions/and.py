from instructions import instruction

class And(instruction.Instruction):
    name = "And"
    mnemonic = "AND"
    
    def __init__(self):
        super().__init__()
