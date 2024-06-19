from USML.usmlRunner import USMLRunner
from USML.codeRunner import CodeRunner

from simpleAssembler import SimpleAssembler


runner = USMLRunner(SimpleAssembler)

with open("prog.usml") as codeStr:
    code = runner.process(codeStr.read())
    input("press enter to run")
    runner = CodeRunner(code, bitCount=8)
    runner.run()
