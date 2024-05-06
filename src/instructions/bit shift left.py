from instructions import instruction

class BitShiftLeft(instruction.Instruction):
    name = "Bit Shift Left"
    mnemonic = "BSL"
    
    def __init__(self):
        super().__init__()
