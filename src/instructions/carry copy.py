from instructions import instruction

class CarryCopy(instruction.Instruction):
    name =  "Carry Copy"
    mnemonic = "CCPY"
    
    def __init__(self):
        super().__init__()
