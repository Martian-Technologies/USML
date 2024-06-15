from USML.usmlRunner import USMLRunner

runner = USMLRunner()

with open("prog.usml") as code:
    runner.process(code.read())