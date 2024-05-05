from instructions import instruction

class JumpIfNotCarry(instruction.Instruction):
    name = "Jump If Not Carry"
    mnemonic = "JFNC"
    
    def __init__(self):
        super().__init__()
