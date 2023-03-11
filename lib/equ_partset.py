import lib.item
import lib.tag
import lib.pvf


class equ_partset(lib.item.item):
    __partset_dict: dict[str, lib.tag.tag]
    __partset_path_dict: dict[str, str]

    def __init__(self, filepath: str, pvf_path: str = ""):
        super().__init__(pvf_path, lib.pvf.ETC, filepath, False)
        self.__partset_dict = {}
        self.__partset_path_dict = {}
        for t in super().get_tag_arr():
            tv = t.get_value()
            if tv == '':
                continue
            id = ''
            i = 0
            while i < len(tv):
                if tv[i] < '0' or tv[i] > '9':
                    break
                id += tv[i]
                i += 1
            if id == '':
                raise Exception("Invalid equ partset value: %s", tv)
            partset_path = ''
            while i < len(tv):
                if tv[i] == '`':
                    for j in range(i+1, len(tv)):
                        if tv[j] == '`':
                            break
                        partset_path += tv[j]
                    break
                i += 1
            if partset_path == '':
                raise Exception("Invalid equ partset value: %s", tv)
            if id in self.__partset_dict:
                raise Exception("重复的partset id: %s", id)
            self.__partset_dict[id] = t
            self.__partset_path_dict[id] = partset_path

    def get_path_by_id(self, id: str) -> str:
        return self.__partset_path_dict[id]
    
    def has_id(self, id: str) -> bool:
        return id in self.__partset_dict

    def get_by_id(self, id: str) -> lib.tag.tag:
        return self.__partset_dict[id]

    def get_partset_dict(self) -> dict[str, lib.tag.tag]:
        return self.__partset_dict

    def get_partset_path_dict(self) -> dict[str, str]:
        return self.__partset_path_dict

    def to_string(self) -> str:
        out = lib.item.PVF_ITEM_START
        for k in sorted(map(int, self.get_partset_dict().keys())):
            out += self.get_partset_dict()[str(k)].to_string() + "\n\n"
        return out