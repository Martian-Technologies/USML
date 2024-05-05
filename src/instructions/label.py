from instructions import instruction

class Label(instruction.Instruction):
    name = "Label"
    mnemonic = "."
    
    def __init__(self):
        super().__init__()
