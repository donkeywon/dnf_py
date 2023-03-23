from __future__ import annotations

import lib.item
import lib.tag
import lib.pvf


class skl:
    __it: lib.item.item
    __dgn_lvl_info_column: int
    __pvp_lvl_info_column: int
    __dgn_lvl_info_tag: lib.tag.tag
    __pvp_lvl_info_tag: lib.tag.tag
    __dgn_lvl_info: list[list[int]]
    __pvp_lvl_info: list[list[int]]

    def __init__(self, it: lib.item.item):
        self.__it = it
        self.__dgn_lvl_info_column = 0
        self.__dgn_lvl_info = []
        self.__pvp_lvl_info_column = 0
        self.__pvp_lvl_info = []
        dgn_lvl_info = ""
        pvp_lvl_info = ""
        if it.has_tag('dungeon'):
            if it.get_single_tag('dungeon').has_sub_tag_name('level info'):
                self.__dgn_lvl_info_tag = it.get_single_tag(
                    'dungeon').get_single_sub_tag('level info')
                dgn_lvl_info = self.__dgn_lvl_info_tag.get_value()
        elif it.has_tag('level info'):
            self.__dgn_lvl_info_tag = it.get_single_tag('level info')
            dgn_lvl_info = self.__dgn_lvl_info_tag.get_value()

        if it.has_tag('pvp'):
            if it.get_single_tag('pvp').has_sub_tag_name('level info'):
                self.__pvp_lvl_info_tag = it.get_single_tag(
                    'pvp').get_single_sub_tag('level info')
                pvp_lvl_info = self.__pvp_lvl_info_tag.get_value()
        if dgn_lvl_info != "":
            res = self.parse_lvl_info(dgn_lvl_info)
            self.__dgn_lvl_info_column = res[0]
            self.__dgn_lvl_info = res[1]
        if pvp_lvl_info != "":
            res = self.parse_lvl_info(pvp_lvl_info)
            self.__pvp_lvl_info_column = res[0]
            self.__pvp_lvl_info = res[1]

    def parse_lvl_info(self, lvl_info: str) -> tuple[int, list[list[int]]]:
        lvl_info = lvl_info.replace("\n", "\t")
        lvl_info_s = list(
            filter(lambda x: x.strip() != "", lvl_info.split("\t")))
        column = int(lvl_info_s[0])
        if column == 0:
            return column, []
        lvl_info_s = lvl_info_s[1:]
        if column != 0 and len(lvl_info_s) % column != 0:
            print("invalid lvl info", self.get_item().get_filepath())

        lvl_info_lst: list[list[int]] = []
        for i in range(0, len(lvl_info_s), column):
            info: list[int] = []
            for j in range(0, column):
                info.append(int(lvl_info_s[i + j]))
            lvl_info_lst.append(info)
        return column, lvl_info_lst

    def get_item(self) -> lib.item.item:
        return self.__it

    def get_dgn_lvl_info(self) -> list[list[int]]:
        return self.__dgn_lvl_info

    def get_pvp_lvl_info(self) -> list[list[int]]:
        return self.__pvp_lvl_info

    def get_dgn_lvl_info_column(self) -> int:
        return self.__dgn_lvl_info_column

    def get_pvp_lvl_info_column(self) -> int:
        return self.__pvp_lvl_info_column

    def set_dgn_lvl_info(self, lvl_info: list[list[int]]):
        self.__dgn_lvl_info = lvl_info

    def set_pvp_lvl_info(self, lvl_info: list[list[int]]):
        self.__pvp_lvl_info = lvl_info

    def get_required_level(self) -> int:
        if not self.get_item().has_tag("required level"):
            return 0
        return int(self.get_item().get_single_tag("required level").get_value())

    def get_dgn_lvl_info_tag(self) -> lib.tag.tag:
        return self.__dgn_lvl_info_tag

    def get_pvp_lvl_info_tag(self) -> lib.tag.tag:
        return self.__pvp_lvl_info_tag

    def shrink_dgn_lvl_info(self, min_lvl: int, remain: int):
        if len(self.get_dgn_lvl_info()) > 0:
            self.set_dgn_lvl_info(self.shrink_lvl_info(
                self.get_dgn_lvl_info(), min_lvl, remain))

    def shrink_pvp_lvl_info(self, min_lvl: int, remain: int):
        if len(self.get_pvp_lvl_info()) > 0:
            self.set_pvp_lvl_info(self.shrink_lvl_info(
                self.get_pvp_lvl_info(), min_lvl, remain))

    def shrink_lvl_info(self, lvl_info: list[list[int]], min_lvl: int, remain: int) -> list[list[int]]:
        if self.get_required_level() < min_lvl or remain <= 0:
            return lvl_info

        return lvl_info[:remain]

    def lvl_info_to_str(self, column: int, lvl_info: list[list[int]]) -> str:
        strs: list[str] = []
        for info in lvl_info:
            s = "\t".join(list(map(lambda x: str(x), info)))
            strs.append(s)
        return str(column) + "\n" + "\n".join(strs)

    def overwrite(self):
        if len(self.get_dgn_lvl_info()) > 0:
            self.get_dgn_lvl_info_tag().set_value(
                self.lvl_info_to_str(self.get_dgn_lvl_info_column(), self.get_dgn_lvl_info()))
        if len(self.get_pvp_lvl_info()) > 0:
            self.get_pvp_lvl_info_tag().set_value(
                self.lvl_info_to_str(self.get_pvp_lvl_info_column(), self.get_pvp_lvl_info()))
        self.get_item().overwrite()
