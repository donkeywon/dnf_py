import os


class lst:
    _item_dict: dict[str, str]
    _item_dict_revert: dict[str, str]
    _filepath: str

    def __init__(self, filepath: str):
        self._filepath = filepath
        self._item_dict = {}
        self._item_dict_revert = {}
        if not os.path.exists(filepath):
            raise Exception("lst file not exists, filepath: %s" % filepath)
        with open(filepath, mode="r", encoding="utf-8") as f:
            content = f.read()
            item_id, item_path = "", ""
            id_done, path_done = False, False
            i = 0
            while i < len(content):
                if content[i] >= "0" and content[i] <= "9":
                    item_id += content[i]
                    for j in range(i + 1, len(content)):
                        if content[j] < "0" or content[j] > "9":
                            i = j + 1
                            id_done = True
                            break
                        item_id += content[j]

                if content[i] == "`":
                    for j in range(i + 1, len(content)):
                        if content[j] == "`":
                            i = j + 1
                            path_done = True
                            break
                        item_path += content[j]

                if id_done and path_done:
                    if (
                        item_id in self._item_dict
                        and item_path not in self._item_dict_revert
                    ):
                        raise Exception("重复id：" + item_id + ", lst: " + filepath)
                    if (
                        item_path in self._item_dict_revert
                        and item_id not in self._item_dict
                    ):
                        print("重复value：" + item_path + ", lst: " + filepath)
                    self._item_dict[item_id] = item_path
                    self._item_dict_revert[item_path] = item_id
                    id_done, path_done = False, False
                    item_id, item_path = "", ""
                i += 1

    def get_path_by_id(self, id: str) -> str:
        return self.get_item_dict()[id]

    def get_id_by_path(self, path: str) -> str:
        return self.get_item_dict_revert()[path]

    def get_item_dict(self) -> dict[str, str]:
        return self._item_dict

    def get_item_dict_revert(self) -> dict[str, str]:
        return self._item_dict_revert

    def get_filepath(self) -> str:
        return self._filepath

    def has_id(self, id: str) -> bool:
        return id in self._item_dict

    def has_path(self, path: str) -> bool:
        return path in self._item_dict_revert

    def size(self) -> int:
        return len(self.get_item_dict())

    def write(self, new_path: str):
        f = open(new_path, mode="w", encoding="utf-8")
        f.write(self.to_string())
        f.close()

    def overwrite(self):
        self.write(self.get_filepath())

    def to_string(self) -> str:
        out = "#PVF_File\n\n"
        for k in sorted(map(int, self.get_item_dict().keys())):
            out += str(k) + "\n"
            out += "`%s`\n" % self.get_item_dict()[str(k)]
        return out
