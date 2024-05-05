from instructions import instruction

class CarryNot(instruction.Instruction):
    name =  "Carry Not"
    mnemonic = "CNOT"
    
    def __init__(self):
        super().__init__()
