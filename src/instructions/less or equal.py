from instructions import instruction

class LessOrEqual(instruction.Instruction):
    name =  "Less Or Equal"
    mnemonic = "LOE"
    
    def __init__(self):
        super().__init__()
