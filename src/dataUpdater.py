import json

from USML.instructions.instructionLookUp import ILU

def getFormattedJson(data, depth=1, maxDepth=2):
    if type(data) not in [list, tuple, dict]:
        if type(data).__str__ is object.__str__ and type(data) not in [int, float, str]:
            return '{"' + type(data).__name__ + '" : ' +\
                getFormattedJson(
                    {attr:data.__getattribute__(attr) for attr in dir(data) if not callable(getattr(data, attr)) and not attr.startswith("__")},
                    depth,
                    maxDepth-1
                ) + "}"
        if type(data) == str:
            return '"' + data + '"'
        if type(data) == bool:
            return "true" if data else "false"
        if data is None:
            return "null"
        return str(data)
    if depth <= maxDepth:
        if type(data) == dict:
            if len(data) == 0:
                return "{}"
            string = "{\n"
            i = 1
            for key in data:
                keyStr = None
                if type(key) == str:
                    keyStr = '"' + key + '"'
                else:
                    keyStr = '"' + str(key) + '"'
                string += "    " * depth + keyStr + ": " + getFormattedJson(data[key], depth+1, maxDepth)
                if i < len(data):
                    string += ","
                string += "\n"
                i += 1
            string += "    " * (depth-1) + "}"
            return string
        else:
            if len(data) == 0:
                return "[]"
            string = "[\n"
            i = 1
            for item in data:
                string += "    " * depth + getFormattedJson(item, depth+1, maxDepth)
                if i < len(data):
                    string += ","
                string += "\n"
                i += 1
            string += "    " * (depth-1) + "]"
            return string
    else:
        if type(data) != dict and type(data) != list:
            if type(data) == str:
                return '"' + data + '"'
            if type(data) == bool:
                return "true" if data else "false"
            return str(data)
        return json.dumps(data)


if __name__ == "__main__":
    # read data
    instructionData = None
    with open("src/simpleAssembler/settings/InstructionData.json") as f:
        instructionData = json.load(f)

    # do data update here
    # ------------------------------------------------------





    # ------------------------------------------------------

    # set data to new json
    with open("src/simpleAssembler/settings/InstructionData2.json", "w") as f:
        f.write(getFormattedJson(instructionData))
    