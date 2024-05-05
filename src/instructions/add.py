from instructions import instruction

class Add(instruction.Instruction):
    name = "Add"
    mnemonic = "ADD"
    
    def __init__(self):
        super().__init__()
