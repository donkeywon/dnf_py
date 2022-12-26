import os

from lib.item import item
from lib.lst import lst

AIC = 'aicharacter'
APD = 'appendage'
CRE = 'creature'
DUNGEON = 'dungeon'
EQU = 'equipment'
MAP = 'map'
MONSTER = 'monster'
QUEST = 'quest'
OBJ = 'passiveobject'
SKL = 'skill'
STK = 'stackable'

TYPES = [
    AIC,
    APD,
    CRE,
    DUNGEON,
    EQU,
    MAP,
    MONSTER,
    QUEST,
    OBJ,
    SKL,
    STK
]


class pvf:
    __path: str

    __type_lst: dict[str, lst]
    __type_item_id_dict: dict[str, dict[int, item]]
    __type_item_path_dict: dict[str, dict[str, item]]

    def __init__(self, path: str, init_type: list[str] = TYPES, skip_item_not_exists: bool = False, skip_item_init_fail: bool = False, merge_duplicate_tag: bool = False):
        self.__path = path
        self.__type_lst = {}
        self.__type_item_id_dict = {}
        self.__type_item_path_dict = {}
        for typ in init_type:
            dir_path = os.path.join(self.__path, typ)
            if not os.path.exists(dir_path):
                continue
            lst_path = os.path.join(dir_path, typ + ".lst")
            l = lst(lst_path)
            self.__type_lst[typ] = l
            typ_item_id_dict = {}
            typ_item_path_dict = {}
            for id, pvf_path in l.get_item_dict().items():
                item_path = os.path.join(self.__path, typ, pvf_path)
                if not os.path.exists(item_path):
                    if skip_item_not_exists:
                        continue
                    else:
                        raise Exception(
                            "item not exists, typ=%s, id=%d, pvf_path=%s" % (typ, id, pvf_path))
                try:
                    it = item(os.path.join(self.__path, typ,
                              pvf_path), merge_duplicate_tag)
                    typ_item_id_dict[id] = it
                    typ_item_path_dict[pvf_path] = it
                except Exception as e:
                    if skip_item_init_fail:
                        print("init item fail, type=%s, id=%d, pvf_path=%s" %
                              (typ, id, pvf_path), e)
                    else:
                        raise Exception(
                            "init item fail, type=%s, id=%d, pvf_path=%s" % (typ, id, pvf_path), e)
            self.__type_item_id_dict[typ] = typ_item_id_dict
            self.__type_item_path_dict[typ] = typ_item_path_dict
        print("pvf init done")

    def get_path(self) -> str:
        return self.__path

    def get_type_lst(self) -> dict[str, lst]:
        return self.__type_lst

    def get_type_dict(self) -> dict[str, dict[int, item]]:
        return self.__type_item_id_dict

    @staticmethod
    def read_dir(path: str, file_ext: str, warn_duplicate_tag: bool = True) -> dict[str, item]:
        if not os.path.exists(path):
            return {}
        res: dict[str, item] = {}
        for parent, _, filenames in os.walk(path):
            for filename in filenames:
                if not filename.endswith(file_ext):
                    continue
                file_path = os.path.join(parent, filename)

                i = item(file_path, warn_duplicate_tag)
                res[file_path] = i
        return res
