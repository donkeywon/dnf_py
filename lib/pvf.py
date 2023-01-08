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
    STK
]

CHARACTER_ATFIGHTER = "atfighter"
CHARACTER_ATGUNNER = "atgunner"
CHARACTER_ATMAGE = "atmage"
CHARACTER_CREATORMAGE = "creatormage"
CHARACTER_DEMONIC_SWORDMAN = "demonicswordman"
CHARACTER_FIGHTER = "fighter"
CHARACTER_GUNNER = "gunner"
CHARACTER_MAGE = "mage"
CHARACTER_PRIEST = "priest"
CHARACTER_SWORDMAN = "swordman"
CHARACTER_THIEF = "thief"

CHARACTERS = [
    CHARACTER_ATFIGHTER,
    CHARACTER_ATGUNNER,
    CHARACTER_ATMAGE,
    CHARACTER_CREATORMAGE,
    CHARACTER_DEMONIC_SWORDMAN,
    CHARACTER_FIGHTER,
    CHARACTER_GUNNER,
    CHARACTER_MAGE,
    CHARACTER_PRIEST,
    CHARACTER_SWORDMAN,
    CHARACTER_THIEF
]


class pvf:
    __path: str

    __type_lst: dict[str, lst]
    __type_item_id_dict: dict[str, dict[str, item]]
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
            for id, internal_path in l.get_item_dict().items():
                item_path = os.path.join(self.__path, typ, internal_path)
                if not os.path.exists(item_path):
                    if skip_item_not_exists:
                        print("item not exists, typ=%s, id=%s, internal_path=%s" % (
                            typ, id, internal_path))
                        continue
                    else:
                        raise Exception(
                            "item not exists, typ=%s, id=%s, internal_path=%s" % (typ, id, internal_path))
                try:
                    it = item(self.__path, os.path.join(self.__path, typ,
                              internal_path), merge_duplicate_tag)
                    typ_item_id_dict[id] = it
                    typ_item_path_dict[internal_path] = it
                except Exception as e:
                    if skip_item_init_fail:
                        print("init item fail, type=%s, id=%s, internal_path=%s" %
                              (typ, id, internal_path), e)
                    else:
                        raise Exception(
                            "init item fail, type=%s, id=%s, internal_path=%s" % (typ, id, internal_path), e)
            self.__type_item_id_dict[typ] = typ_item_id_dict
            self.__type_item_path_dict[typ] = typ_item_path_dict
        print("pvf init done")

    def get_path(self) -> str:
        return self.__path

    def get_type_lst(self) -> dict[str, lst]:
        return self.__type_lst

    def get_lst_by_type(self, type: str) -> lst:
        return self.__type_lst[type]

    def get_type_item_id_dict(self) -> dict[str, dict[str, item]]:
        return self.__type_item_id_dict

    def get_type_item_path_dict(self) -> dict[str, dict[str, item]]:
        return self.__type_item_path_dict

    def get_type_item_by_id(self, type: str, id: str) -> item:
        return self.__type_item_id_dict[type][id]

    def get_type_item_by_path(self, type: str, path: str) -> item:
        return self.__type_item_path_dict[type][path]

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

                try:
                    i = item(path, file_path, warn_duplicate_tag)
                    res[file_path] = i
                except Exception as e:
                    raise Exception(
                        "init item fail, filepath=%s" % file_path, e)
        return res
