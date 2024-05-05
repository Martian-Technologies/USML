from instructions import instruction

class NoOperation(instruction.Instruction):
    name =  "No Operation"
    mnemonic = "NOP"
    
    def __init__(self):
        super().__init__()
