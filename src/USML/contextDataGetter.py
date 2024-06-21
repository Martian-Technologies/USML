from copy import deepcopy

from USML.instructions.instructionLookUp import ILU
from USML.context import Context


class ContextDataGetter:
    def __init__(self, context:Context):
        self.context:Context = context.copy()
        self.varAndLabelUsage = None

    def getVarAndLabelUsage(self) -> dict[str, dict[str, list[dict[str, int]]|int]]:
        if self.varAndLabelUsage is not None:
            return self.varAndLabelUsage
        data:dict[str, dict[str, str|int|list[dict[str, int]]]] = {}
        def getData(name:str, line:int, type:str, usageType:str):
            if name not in data:
                data[name] = {
                    "usage": [],
                    "count": 0,
                    "type": type
                }
            data[name]["count"] += 1
            data[name]["usage"].append({"usageType": usageType, "line": line})

        self.context.iterOverParams(getData)
        self.varAndLabelUsage = data
        return data
    
    def varNextUsed(self, varName:str, startLineNumber:int, vistedLines = None):
        varAndLabelUsage = self.getVarAndLabelUsage()
        if vistedLines is None:
            vistedLines:dict[int, bool] = {}
        otherPath:None|dict[str, int] = None
        if startLineNumber in vistedLines:
            return otherPath
        vistedLines[startLineNumber] = True
        if otherPath is not None:
            if otherPath["steps"] < len(vistedLines):
                return otherPath
        line = self.context.getCommand(startLineNumber)
        if line is None:
            return otherPath
        if "program stop" in ILU.getTags_Mnemonic(line[0]):
            return otherPath
        if "force jump" in ILU.getTags_Mnemonic(line[0]):
            labelUsage = varAndLabelUsage[line[1][0]]
            newstartLineNumber = None
            for usage in labelUsage["usage"]:
                if usage["usageType"] == "out":
                    newstartLineNumber = usage["line"]
            if newstartLineNumber is None:
                raise Exception(f"jump label {line[1][0]} not defined. Line {startLineNumber}")
            startLineNumber = newstartLineNumber
        elif  "maybe jump" in ILU.getTags_Mnemonic(line[0]):
            labelUsage = varAndLabelUsage[line[1][0]]
            for usage in labelUsage["usage"]:
                if usage["usageType"] == "out":
                    possibleOtherPath = self.varNextUsed(varName, usage["line"], deepcopy(vistedLines))
                    if otherPath is None:
                        otherPath = possibleOtherPath
                    elif otherPath["steps"] > possibleOtherPath:
                        otherPath = possibleOtherPath
        while True:
            startLineNumber += 1
            if startLineNumber in vistedLines:
                return otherPath
            vistedLines[startLineNumber] = True
            if otherPath is not None:
                if otherPath["steps"] < len(vistedLines):
                    return otherPath
            line = self.context.getCommand(startLineNumber)
            if line is None:
                return otherPath
            if "program stop" in ILU.getTags_Mnemonic(line[0]):
                return otherPath
            if "force jump" in ILU.getTags_Mnemonic(line[0]):
                labelUsage = varAndLabelUsage[line[1][0]]
                newstartLineNumber = None
                for usage in labelUsage["usage"]:
                    if usage["usageType"] == "out":
                        newstartLineNumber = usage["line"]
                if newstartLineNumber is None:
                    raise Exception(f"jump label {line[1][0]} not defined. Line {startLineNumber}")
                startLineNumber = newstartLineNumber
            elif  "maybe jump" in ILU.getTags_Mnemonic(line[0]):
                labelUsage = varAndLabelUsage[line[1][0]]
                for usage in labelUsage["usage"]:
                    if usage["usageType"] == "out":
                        possibleOtherPath = self.varNextUsed(varName, usage["line"], deepcopy(vistedLines))
                        if otherPath is None:
                            otherPath = possibleOtherPath
                        elif otherPath["steps"] > possibleOtherPath:
                            otherPath = possibleOtherPath
            for i in range(len(line[1])):
                if line[1][i] == varName:
                    usageType = ILU.getUsageTypes_Mnemonic(line[0])[i]
                    if usageType == "out":
                        return otherPath
                    elif usageType in ["in", "both"]:
                        if (otherPath is None) or otherPath["steps"] >= len(vistedLines):
                            return {"lineNumber":startLineNumber, "steps":len(vistedLines)}
                        else:
                            return otherPath
                        