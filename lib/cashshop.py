import lib.pvf
import lib.item


class cashshop(lib.item.item):
    __avatar: dict[str, list[str]]
    __package: dict[str, list[str]]

    def __init__(self, pvf_path: str, filepath: str):
        super().__init__(pvf_path, lib.pvf.ETC, filepath, False)
        self.__avatar = {}
        self.__package = {}
        if self.has_tag('avatar'):
            avatar = self.get_single_tag('avatar')
            avatar_list = avatar.get_value().split('\n')
            for a in avatar_list:
                a_splitted = a.strip().split('\t')
                id = a_splitted[1]
                if id in self.__avatar:
                    raise Exception("重复的avatar id: %s", id)
                self.__avatar[id] = a_splitted
        if self.has_tag('package'):
            package = self.get_single_tag('package')
            package_list = package.get_value().split('\n')
            for p in package_list:
                p_splitted = p.strip().split('\t')
                id = p_splitted[1]
                if id in self.__package:
                    raise Exception("重复的package id: %s", id)
                self.__package[id] = p_splitted

    def get_avatar_dict(self) -> dict[str, list[str]]:
        return self.__avatar

    def get_package_dict(self) -> dict[str, list[str]]:
        return self.__package

    def get_avatar_by_id(self, id: str) -> list[str]:
        return self.__avatar[id]

    def get_package_by_id(self, id: str) -> list[str]:
        return self.__package[id]

    def has_avatar(self, id: str) -> bool:
        return id in self.__avatar

    def has_package(self, id: str) -> bool:
        return id in self.__package
