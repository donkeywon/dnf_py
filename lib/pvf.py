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
    __type_dict: dict[str, dict[int, item]]

    def __init__(self, path: str, init_type: list[str] = TYPES):
        self.__path = path
        self.__type_lst = {}
        self.__type_dict = {}
        for typ in init_type:
            dir_path = os.path.join(self.__path, typ)
            if not os.path.exists(dir_path):
                return
            lst_path = os.path.join(dir_path, typ + ".lst")
            l = lst(lst_path)
            self.__type_lst[typ] = l
            typ_dict = {}
            for id, pvf_path in l.get_item_dict().items():
                item_path = os.path.join(self.__path, typ, pvf_path)
                if not os.path.exists(item_path):
                    raise Exception("item not exists, typ=%s, id=%d, pvf_path=%s" % (typ, id, pvf_path))
                try:
                    typ_dict[id] = item(os.path.join(self.__path, typ, pvf_path))
                except Exception as e:
                    print("init item fail, type=%s, id=%d, pvf_path=%s" % (typ, id, pvf_path), e)
            self.__type_dict[typ] = typ_dict
        print("pvf init done")
    def get_path(self) -> str:
        return self.__path
    def get_type_lst(self) -> dict[str, lst]:
        return self.__type_lst
    def get_type_dict(self) -> dict[str, dict[int, item]]:
        return self.__type_dict