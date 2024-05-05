from instructions import instruction

class Xor(instruction.Instruction):
    name =  "Xor"
    mnemonic = "XOR"
    
    def __init__(self):
        super().__init__()
