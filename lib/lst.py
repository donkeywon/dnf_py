from lib import const

class lst:
    __item_dict: dict[int, str]
    __item_dict_revert: dict[str, int]
    def __init__(self, filepath):
        self.__item_dict = {}
        self.__item_dict_revert = {}
        with open(filepath, mode='r', encoding='utf-8') as f:
            lines = f.readlines()
            for start in range(0, len(lines)):
                if lines[start].strip(const.STRIP_CHARS).isdigit():
                    break

            for i in range(start, len(lines), 2):
                k = int(lines[i].strip(const.STRIP_CHARS))
                v = lines[i + 1].strip(const.STRIP_CHARS).lower()
                if k in self.__item_dict:
                    raise Exception("重复id：" + k + ", lst: " + filepath)
                if v in self.__item_dict_revert:
                    raise Exception("重复value：" + v + ", lst: " + filepath)
                self.__item_dict[k] = v
                self.__item_dict_revert[v] = k
    def get_value_by_id(self, id):
        return self.__item_dict[id]
    def get_id_by_value(self, value):
        return self.__item_dict_revert[value]
    def size(self):
        return len(self.__item_dict)
    def to_string(self):
        out = "#PVF_File\n\n"
        for k in sorted(self.__item_dict.keys()):
            out += str(k) + "\n"
            out += self.__item_dict[k] + "\n"
        return out

