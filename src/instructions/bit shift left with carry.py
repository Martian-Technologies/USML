from instructions import instruction

class BitShiftLeftWithCarry(instruction.Instruction):
    name = "Bit Shift Left With Carry"
    mnemonic = "BSLC"
    
    def __init__(self):
        super().__init__()
