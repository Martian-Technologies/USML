from USML.usmlRunner import USMLRunner
from USML.codeRunner import CodeRunner

runner = USMLRunner()

with open("prog.usml") as codeStr:
    code = runner.process(codeStr.read())
    runner = CodeRunner(code)
    runner.run(True)
