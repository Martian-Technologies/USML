from instructions import instruction

class Less(instruction.Instruction):
    name =  "Less"
    mnemonic = "LES"
    
    def __init__(self):
        super().__init__()
