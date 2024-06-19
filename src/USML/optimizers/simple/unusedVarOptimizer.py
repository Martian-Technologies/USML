from USML.optimizers.simple.baseSimpleOptimizer import BaseSimpleOptimizer
from USML.contextDataGetter import ContextDataGetter as CDG
from USML.instructions.instructionLookUp import ILU
from USML.context import Context


class UnusedVarOptimizer(BaseSimpleOptimizer):
    @staticmethod
    def run(context:Context) -> Context:
        tryRemove = True
        while tryRemove:
            tryRemove = False
            toDel = {}
            dataGetter = CDG(context)
            varAndLabelUsage = dataGetter.getVarAndLabelUsage()
            for param in varAndLabelUsage:
                if varAndLabelUsage[param]["type"] == "var":
                    for usage in varAndLabelUsage[param]["usage"]:
                        if usage["usageType"] in ["out", "both"]:
                            if not UnusedVarOptimizer.varIsUsed(param, usage["line"], context, varAndLabelUsage):
                                if usage["line"] in toDel:
                                    toDel[usage["line"]] += 1
                                else:
                                    toDel[usage["line"]] = 1      
                elif varAndLabelUsage[param]["type"] == "label":
                    if varAndLabelUsage[param]["count"] == 1:
                        lineNum = varAndLabelUsage[param]["usage"][0]["line"]
                        toDel[lineNum] = 1
            for line in sorted(toDel, reverse=True):
                if toDel[line] == UnusedVarOptimizer.instructionOutCount(context.getCommand(line)[0]):
                    context.removeCommand(line)
                    tryRemove = True
        return context
    
    @staticmethod
    def instructionOutCount(instructionMnemonic:str):
        count = 0
        for usage in ILU.getUsageTypes_Mnemonic(instructionMnemonic):
            if usage in ["out", "both"]:
                count += 1
        return count
    
    @staticmethod
    def varIsUsed(varName:str, lineNumber:int, context:Context, varAndLabelUsage:dict[str, dict[str, list[dict[str, int]] | int]], vistedLine = None):
        if vistedLine is None:
            if varAndLabelUsage[varName]["count"] == 1:
                return False
            vistedLine:dict[int, bool] = {lineNumber:True}
        notUsed = True
        while notUsed:
            lineNumber += 1
            if lineNumber in vistedLine:
                return False
            vistedLine[lineNumber] = True
            line = context.getCommand(lineNumber)
            if line is None:
                return False
            if line[0] == ILU.getMnemonic("Jump"):
                labelUsage = varAndLabelUsage[line[1][0]]
                newLineNumber = None
                for usage in labelUsage["usage"]:
                    if usage["usageType"] == "out":
                        newLineNumber = usage["line"]
                if newLineNumber is None:
                    raise Exception(f"jump label {line[1][0]} not defined. Line {lineNumber}")
                lineNumber = newLineNumber
            elif line[0] == ILU.getMnemonic("Jump If") or line[0] == ILU.getMnemonic("Jump If Not"):
                labelUsage = varAndLabelUsage[line[1][0]]
                for usage in labelUsage["usage"]:
                    if usage["usageType"] == "out":
                        if UnusedVarOptimizer.varIsUsed(varName, usage["line"], context, varAndLabelUsage, vistedLine):
                            return True
            for i in range(len(line[1])):
                if line[1][i] == varName:
                    usageType = ILU.getUsageTypes_Mnemonic(line[0])[i]
                    if usageType == "out":
                        return False
                    elif usageType in ["in", "both"]:
                        return True
                    

                        
                