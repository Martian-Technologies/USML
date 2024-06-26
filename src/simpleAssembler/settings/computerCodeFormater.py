from USML.instructions.instructionLookUp import ILU
from USML.bitString import BitString

from simpleAssembler.internals.simpleAssembler import SimpleAssembler
from simpleAssembler.internals.memory import MemoryPos

def makeAssembly(line:tuple[str, list[int|MemoryPos]], instructionData:dict[str|int|list[str]]) -> str:
    """
    This function is used to allow people to have custom formating for the output of the Assembler.\n
    The function ran once per line in the assembly\n
    Args:
        This line.\n
        The instruction data for this command (defined in "InstructionData.json")\n
    Returns:
        A String that represents this line in the formating you want
    """
    commandMnemonic = line[0]
    commandName = ILU.getName(commandMnemonic)
    params = line[1]
    # -------- RENAMING --------
    # rename copy
    newName = None
    if commandName == "Copy":
        for movementCommand in SimpleAssembler.settings["movementCommands"]:
            if params[0].containedInData(movementCommand["movementFrom"]):
                if params[1].containedInData(movementCommand["movementTo"]):
                    newName = movementCommand["commandName"]
        if newName == None:
            raise Exception(f"cant find movement from {params[0], params[1]}")
    # rename other
    else:
        newName = instructionData["instructionName"]

    # -------- RAM AND REG POSITION --------
    # change pos data
    for i in range(len(params)):
        param = params[i]
        if type(param) == MemoryPos:
            if param.ramOrReg == "ram": # do ram formating
                params[i] = param.memAddress
            else:                       # do reg formating
                params[i] = param.memAddress

    # -------- REORDER PARAMS --------
    # reorder and merge to string
    paramOrder = instructionData["paramOrder"]
    paramStr = ""
    for paramIndex in paramOrder:
        paramIndex = int(paramIndex[5:len(paramIndex)]) - 1
        param = params[paramIndex]
        # some formatting
        paramStr += " " + str(param)
        if paramStr[len(paramStr)-2:len(paramStr)] == ".0":
            paramStr = paramStr[0:len(paramStr)-2]

    # remove space for labels
    if newName == ".":
        paramStr = paramStr[1:len(paramStr)]
    # return line
    return newName + paramStr

def makeBinary(line:tuple[str, list[int|MemoryPos]], instructionData:dict[str|int|list[str]]) -> str:
    """
    This function is used to allow people to have custom binary formating for the output of the Assembler.\n
    The function ran once per line in the assembly\n
    Args:
        This line.\n
        The instruction data for this command (defined in "InstructionData.json")\n
    Returns:
        A String that represents this line in the binary formating you want
    """
    commandMnemonic = line[0]
    commandName = ILU.getName(commandMnemonic)
    params = line[1]
    # create bit strings to format binary data
    numberF = BitString(SimpleAssembler.settings["numberBitCount"])
    addressF = BitString(SimpleAssembler.settings["addressBitCount"])
    commandF = BitString(SimpleAssembler.settings["commandBitCount"])
    # -------- RENAMING --------
    # rename copy
    newName = None
    if commandName == "Copy":
        for movementCommand in SimpleAssembler.settings["movementCommands"]:
            if params[0].containedInData(movementCommand["movementFrom"]):
                if params[1].containedInData(movementCommand["movementTo"]):
                    commandF.setInt(movementCommand["commandId"])
                    newName = commandF.getBitString()
        if newName == None:
            raise Exception(f"cant find movement from {params[0], params[1]}")
    # rename other
    else:
        commandF.setInt(instructionData["instructionId"])
        newName = commandF.getBitString()

    # -------- RAM AND REG POSITION / FORMAT PARAMS--------
    # change pos data
    for i in range(len(params)):
        param = params[i]
        if type(param) == MemoryPos:
            if param.ramOrReg == "ram": # do ram formating
                addressF.setInt(param.memAddress)
                params[i] = addressF.getBitString()
            else:                       # do reg formating
                addressF.setInt(param.memAddress)
                params[i] = addressF.getBitString()
        elif type(param) == str: # labels
            pass
        else: # must be a number
            numberF.setInt(param)
            params[i] = numberF.getBitString()
    # -------- REORDER PARAMS --------
    # reorder and merge to string
    paramOrder = instructionData["paramOrder"]
    paramStr = ""
    for paramIndex in paramOrder:
        paramIndex = int(paramIndex[5:len(paramIndex)]) - 1
        param = params[paramIndex]
        # some formatting
        paramStr += " " + param
        if paramStr[len(paramStr)-2:len(paramStr)] == ".0":
            paramStr = paramStr[0:len(paramStr)-2]

    # return line
    return newName + paramStr