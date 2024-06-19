from USML.context import Context


class BaseSimpleOptimizer:
    @staticmethod
    def run(context:Context) -> Context:
        return context