def pokemon_to_dict(file: str, d:dict) -> dict:
    with open(file, "r+") as f:
        ret = d
        line = f.readline().strip()
        # print(line)
        depth = 0
        while line != "Moth says end of file":
            # print(line)
            # print(currdict)
            # print(depth)
            if not line.startswith("//"):
                if "{" in line and depth == 1:
                    move = line.split(":", maxsplit=1)[0]
                    ret[move] = {}
                    #print(move)
                if depth == 2 and ":" in line:
                    key = line.split(":")[0]
                    element = line.split(":", maxsplit=1)[1].strip()
                    if key in ["num", "name", "types", "baseStats", "abilities", "heightm", "weightkg", "color",
                               "eggGroups", "sanctum", "inherit"]:
                        if key == "types":
                            ret[move][key] = list(eval(element[1:-2]))
                        elif key == "abilities" or key == "baseStats":
                            element = element.replace("{","{\"")
                            element = element.replace(":", "\":")
                            element = element.replace(", ",", \"")
                            ret[move][key] = eval(element[0:-1])
                        else:
                            ret[move][key] = element[0:-1]
                    # print(key, element)
            depth += line.count("{")
            depth -= line.count("}")
            line = f.readline().strip()
            # print(line)
        return ret

def learnset_to_dict(file: str, d:dict) -> dict:
    with open(file, "r+") as f:
        ret = d
        line = f.readline().strip()
        # print(line)
        depth = 0
        learnset = ""
        while line != "Moth says end of file":
            if not line.startswith("//"):
                # print(line)
                # print(currdict)
                # print(depth)
                if "{" in line and depth == 1:
                    mon = line.split(":", maxsplit=1)[0]
                    ret[mon] = []
                    # print(move)
                if depth == 2 and ":" in line:
                    learnset = line.split(":")[0]
                if learnset == "learnset" and depth == 3 and ":" in line:
                    element = line.split(":", maxsplit=1)[0].strip()
                    ret[mon].append(element)
                    #print(mon, element)
            depth += line.count("{")
            depth -= line.count("}")
            line = f.readline().strip()
            # print(line)
        return ret

def moves_to_dict(file: str, d:dict) -> dict:
    with open(file, "r+") as f:
        ret = d
        line = f.readline().strip()
        # print(line)
        depth = 0
        while line != "Moth says end of file":
            if not line.startswith("//"):
                # print(line)
                # print(currdict)
                # print(depth)
                if "{" in line and depth == 1:
                    move = line.split(":", maxsplit=1)[0]
                    ret[move] = {}
                    # print(move)
                if depth == 2 and ":" in line:
                    key = line.split(":")[0]
                    element = line.split(":", maxsplit=1)[1].strip()
                    if key in ["accuracy", "basePower", "category", "name", "pp", "priority", "flags", "secondary",
                               "target", "type", "boosts", "critRatio", "self"]:
                        if key == "secondary" or key == "self":
                            ret[move][key] = "TODO"
                        elif key == "flags" and element != "{},":
                            #print(element)
                            #print(move)
                            element = element.replace("{", "{\"")
                            element = element.replace(":", "\":")
                            element = element.replace(", ", ", \"")
                            try:
                                ret[move][key] = eval(element[0:-1])
                            except SyntaxError:
                                ret[move][key] = "TODO"
                        else:
                            ret[move][key] = element[0:-1]
                    # print(key, element)
            depth += line.count("{")
            depth -= line.count("}")
            line = f.readline().strip()
            # print(line)
        return ret


def abilities_to_dict(file: str, d:dict) -> dict:
    with open(file, "r+") as f:
        ret = d
        line = f.readline().strip()
        # print(line)
        depth = 0
        while line != "Moth says end of file":
            if not line.startswith("//"):
                # print(line)
                # print(currdict)
                # print(depth)
                if "{" in line and depth == 1:
                    ability = line.split(":", maxsplit=1)[0]
                    ret[ability] = {}
                    # print(ability)
                if depth == 2 and ":" in line:
                    key = line.split(":")[0]
                    element = line.split(":", maxsplit=1)[1].strip()
                    if key in ["name", "flags", "rating", "shortDesc"]:
                        if key == "secondary" or key == "self":
                            ret[ability][key] = "TODO"
                        else:
                            ret[ability][key] = element[:-1]
                    # print(key, element)
            depth += line.count("{")
            depth -= line.count("}")
            line = f.readline().strip()
            # print(line)
        return ret