class lst:
    item_dict: dict[int, str]
    item_dict_revert: dict[str, int]
    filepath: str
    def __init__(self, filepath):
        self.filepath = filepath
        self.item_dict = {}
        self.item_dict_revert = {}
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
                    if item_id in self.item_dict:
                        raise Exception("重复id：" + item_id + ", lst: " + filepath)
                    if item_path in self.item_dict_revert:
                        print("重复value：" + item_path + ", lst: " + filepath)
                    self.item_dict[item_id] = item_path
                    self.item_dict_revert[item_path] = item_id
                    id_done, path_done = False, False
                    item_id, item_path = '', ''
                i += 1
    def get_value_by_id(self, id):
        return self.item_dict[id]
    def get_id_by_value(self, value):
        return self.item_dict_revert[value]
    def size(self):
        return len(self.item_dict)
    def to_string(self):
        out = "#PVF_File\n\n"
        for k in sorted(self.item_dict.keys()):
            out += str(k) + "\n"
            out += "`%s`\n" % self.item_dict[k]
        return out
