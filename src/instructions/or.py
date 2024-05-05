from instructions import instruction

class Or(instruction.Instruction):
    name =  "Or"
    mnemonic = "OR"
    
    def __init__(self):
        super().__init__()
