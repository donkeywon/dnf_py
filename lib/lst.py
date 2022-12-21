import os


class lst:
    __item_dict: dict[int, str]
    __item_dict_revert: dict[str, int]
    __filepath: str

    def __init__(self, filepath: str):
        self.__filepath = filepath
        self.__item_dict = {}
        self.__item_dict_revert = {}
        if not os.path.exists(filepath):
            raise Exception("lst file not exists, filepath: %s" % filepath)
        with open(filepath, mode='r', encoding='utf-8') as f:
            content = f.read()
            item_id, item_path = '', ''
            id_done, path_done = False, False
            i = 0
            while i < len(content):
                if content[i] >= '0' and content[i] <= '9':
                    item_id += content[i]
                    for j in range(i+1, len(content)):
                        if content[j] < '0' or content[j] > '9':
                            i = j + 1
                            id_done = True
                            break
                        item_id += content[j]

                if content[i] == '`':
                    for j in range(i+1, len(content)):
                        if content[j] == '`':
                            i = j + 1
                            path_done = True
                            break
                        item_path += content[j]

                if id_done and path_done:
                    item_path = item_path.lower()
                    item_id = int(item_id)
                    if item_id in self.__item_dict:
                        raise Exception("重复id：" + item_id +
                                        ", lst: " + filepath)
                    if item_path in self.__item_dict_revert:
                        print("重复value：" + item_path + ", lst: " + filepath)
                    self.__item_dict[item_id] = item_path
                    self.__item_dict_revert[item_path] = item_id
                    id_done, path_done = False, False
                    item_id, item_path = '', ''
                i += 1

    def get_value_by_id(self, id: int) -> str:
        return self.get_item_dict()[id]

    def get_id_by_value(self, value: str) -> int:
        return self.get_item_dict_revert()[value]

    def get_item_dict(self) -> dict[int, str]:
        return self.__item_dict

    def get_item_dict_revert(self) -> dict[str, int]:
        return self.__item_dict_revert

    def get_filepath(self) -> str:
        return self.__filepath

    def size(self) -> int:
        return len(self.get_item_dict())

    def write(self, new_path: str = ''):
        path = self.get_filepath()
        if new_path != '':
            path = new_path
        f = open(path, mode='w', encoding='utf-8')
        f.write(self.to_string())
        f.close()

    def to_string(self) -> str:
        out = "#PVF_File\n\n"
        for k in sorted(self.get_item_dict().keys()):
            out += str(k) + "\n"
            out += "`%s`\n" % self.get_item_dict()[k]
        return out
