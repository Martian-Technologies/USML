from USML.optimizers.simple.baseSimpleOptimizer import BaseSimpleOptimizer
from USML.instructions.instructionLookUp import ILU
from USML.context import Context, ContextDataGetter


class UnusedVarOptimizer(BaseSimpleOptimizer):
    @staticmethod
    def run(context:Context) -> Context:
        tryRemove = True
        while tryRemove:
            tryRemove = False
            toDel:dict[int, int] = {}
            dataGetter = ContextDataGetter(context)
            varAndLabelUsage = dataGetter.getVarAndLabelUsage()
            for param in varAndLabelUsage:
                if varAndLabelUsage[param]["type"] == "var":
                    for usage in varAndLabelUsage[param]["usage"]:
                        if usage["usageType"] in ["out", "both"]:
                            if dataGetter.varNextRead(param, usage["line"]) is None:
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

                