from instructions import instruction

class AddWithCarry(instruction.Instruction):
    name = "Add With Carry"
    mnemonic = "ADDC"
    
    def __init__(self):
        super().__init__()
