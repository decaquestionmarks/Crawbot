class Filtereq:
    def __init__(self, target, thresh):
        self.target = target
        self.thresh = thresh

    def filter(self, keys: list, dic: dict) -> list:
        return [key for key in keys if dic[key][self.target] == self.thresh]


class Filterless:
    def __init__(self, target, thresh):
        self.target = target
        self.thresh = thresh

    def filter(self, keys: list, dic: dict) -> list:
        ret = []
        for key in keys:
            try:
                if float(dic[key][self.target]) <= self.thresh:
                    ret.append(key)
            except:
                pass
        return ret


class Filtermore:
    def __init__(self, target, thresh):
        self.target = target
        self.thresh = thresh

    def filter(self, keys: list, dic: dict) -> list:
        ret = []
        for key in keys:
            try:
                if float(dic[key][self.target]) >= self.thresh:
                    ret.append(key)
            except:
                pass
        return ret


def multifilter(keys: list, dic: dict, filters: list["Filter"]) -> list:
    for i in filters:
        keys = i.filter(keys, dic)
    return keys