from instructions import instruction

class JumpIfCarry(instruction.Instruction):
    name = "Jump If Carry"
    mnemonic = "JFC"
    
    def __init__(self):
        super().__init__()
