from instructions import instruction

class BitShiftRight(instruction.Instruction):
    name = "Bit Shift Right"
    mnemonic = "BSR"
    
    def __init__(self):
        super().__init__()
