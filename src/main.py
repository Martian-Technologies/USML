from USML.usmlRunner import USMLRunner
from USML.codeRunner import CodeRunner
from simpleAssembler.internals.simpleAssembler import SimpleAssembler


runner = USMLRunner(SimpleAssembler)

with open("prog.usml") as codeStr:
    code, assembly = runner.process(codeStr.read())
    print("code")
    print(code)
    # print("assembly")
    # print(assembly)
    # print("createdFormatedString")
    # print(SimpleAssembler.createdFormatedString(assembly))
    # print("createdBinaryString")
    # print(SimpleAssembler.createdBinaryString(assembly))
    input("press enter to run")
    runner = CodeRunner(code, bitCount=8)
    runner.run()
