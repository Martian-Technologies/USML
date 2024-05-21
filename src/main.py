# import lookUp
# print(lookUp.getBestCost(lookUp.getName("."), []))

from usmlRunner import USMLRunner

runner = USMLRunner()

with open("prog.usml") as code:
    runner.process(code.read())