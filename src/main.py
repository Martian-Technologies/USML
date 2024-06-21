from USML.usmlRunner import USMLRunner
from USML.codeRunner import CodeRunner
from simpleAssembler.simpleAssembler import SimpleAssembler


runner = USMLRunner(SimpleAssembler)

with open("prog.usml") as codeStr:
    code, assembly = runner.process(codeStr.read())
    print(assembly)
    input("press enter to run")
    runner = CodeRunner(code, bitCount=8)
    runner.run()
