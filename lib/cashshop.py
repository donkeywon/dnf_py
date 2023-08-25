import lib.pvf
import lib.item


class cashshop:
    _it: lib.item.item
    _avatar: dict[str, list[str]]
    _package: dict[str, list[str]]

    def __init__(self, it: lib.item.item):
        self._it = it
        self._avatar = {}
        self._package = {}
        if it.has_tag("avatar"):
            avatar = it.get_single_tag("avatar")
            avatar_list = avatar.get_value().split("\n")
            for a in avatar_list:
                a_splitted = a.strip().split("\t")
                id = a_splitted[1]
                if id in self._avatar:
                    raise Exception("重复的avatar id: %s", id)
                self._avatar[id] = a_splitted
        if it.has_tag("package"):
            package = it.get_single_tag("package")
            package_list = package.get_value().split("\n")
            for p in package_list:
                p_splitted = p.strip().split("\t")
                id = p_splitted[1]
                if id in self._package:
                    raise Exception("重复的package id: %s", id)
                self._package[id] = p_splitted

    def get_item(self) -> lib.item.item:
        return self._it

    def get_avatar_dict(self) -> dict[str, list[str]]:
        return self._avatar

    def get_package_dict(self) -> dict[str, list[str]]:
        return self._package

    def get_avatar_by_id(self, id: str) -> list[str]:
        return self._avatar[id]

    def get_package_by_id(self, id: str) -> list[str]:
        return self._package[id]

    def has_avatar(self, id: str) -> bool:
        return id in self._avatar

    def has_package(self, id: str) -> bool:
        return id in self._package
