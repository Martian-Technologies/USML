from USML.context import Context


class ContextDataGetter:
    def __init__(self, context:Context):
        self.context:Context = context

    def getVarAndLabelUsage(self) -> dict[str, dict[str, list[dict[str, int]]|int]]:
        data:dict[str, dict[str, list[dict[str, int]]|int]] = {}
        def getData(name:str, line:int, type:str, usageType:str):
            if name not in data:
                data[name] = {
                    "usage": [],
                    "count": 0,
                    "type": type
                }
            data[name]["count"] += 1
            data[name]["usage"].append({"usageType": usageType, "line": line})

        self.context.iterOverParams(getData)
        return data