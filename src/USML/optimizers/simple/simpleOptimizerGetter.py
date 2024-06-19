from __future__ import annotations
import importlib
import pathlib
import os

from USML.optimizers.simple.baseSimpleOptimizer import BaseSimpleOptimizer


class SimpleOptimizerGetter:
    simpleOptimizerGetter:SimpleOptimizerGetter = None
    
    def __init__(self) -> None:
        SimpleOptimizerGetter.simpleOptimizerGetter = self
        self.optimizers:list[type[BaseSimpleOptimizer]] = []
        src = pathlib.Path("src")
        instructions_path = src / 'USML' / 'optimizers' / 'simple'
        classFiles = [f for f in os.listdir(instructions_path) if (os.path.isfile(instructions_path / f) and f != "simpleOptimizerGetter.py")]
        for className in classFiles:
            className = className[0:-3]
            module = importlib.import_module("USML.optimizers.simple." + className)
            classObj:type[BaseSimpleOptimizer] = getattr(module, className[0].upper() + className[1:len(className)])
            self.optimizers.append(classObj)

    def getOptimizer(self) -> list[type[BaseSimpleOptimizer]]:
        return self.optimizers

if SimpleOptimizerGetter.simpleOptimizerGetter is None:
    SimpleOptimizerGetter()