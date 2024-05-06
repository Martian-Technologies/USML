from instructions import instruction

class BitShiftRightWithCarry(instruction.Instruction):
    name = "Bit Shift Right With Carry"
    mnemonic = "BSRC"
    
    def __init__(self):
        super().__init__()
