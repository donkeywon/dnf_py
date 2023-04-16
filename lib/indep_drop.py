import os

import lib.lst
import lib.item
import lib.pvf


def flat_drop_list(s: str) -> str:
    return s.strip().lstrip(
        "[list]").rstrip("[/list]").replace("\n", "\t").replace("\r\n", "\t").replace("\t\t", "\t")


def flat_drop_list_to_list(s: str) -> list[int]:
    return list(map(lambda x: int(x), list(filter(lambda x: x != "", flat_drop_list(s).split("\t")))))


class indep_drop_list_item:
    item: int
    prob: int

    def __init__(self, item: int, prob: int):
        self.item = item
        self.prob = prob


class indep_drop_info:
    info: list[int]
    monster_type: int
    monster: int
    item: int
    drop_type: int
    raw_drop_list: str
    drop_list: list[int]
    drop_list_info: dict[int, indep_drop_list_item]

    def __init__(self, drop_info: list[int], raw_drop_list: str = ""):
        self.info = drop_info
        self.monster = int(drop_info[1])
        self.monster_type = int(drop_info[0])
        self.item = int(drop_info[2])
        self.drop_type = int(drop_info[-1])
        if raw_drop_list != "":
            self.raw_drop_list = raw_drop_list
            self.drop_list = flat_drop_list_to_list(raw_drop_list)
            if self.drop_type == 1:
                self.drop_list_info = {}
                for i in range(0, len(self.drop_list), 2):
                    self.drop_list_info[self.drop_list[i]] = indep_drop_list_item(
                        self.drop_list[i], self.drop_list[i+1])
            # elif self.drop_type == 2:
            #     for extra_drop_list_id, extra_drop_list_item in self.extra_drop_list.items():
            #         extra_drop_info = list(map(lambda x: int(x), flat_drop_list_to_list(extra_drop_list_item.get_single_tag(
            #             'list').get_value())))
            #         extra_drop_info_dict: dict[int, indep_drop_list_item] = {}
            #         for i in range(0, len(extra_drop_info), 2):
            #             if extra_drop_info[i] not in extra_drop_info_dict:
            #                 extra_drop_info_dict[extra_drop_info[i]] = indep_drop_list_item(
            #                     extra_drop_info[i], extra_drop_info[i+1])
            #             else:
            #                 extra_drop_info_dict[extra_drop_info[i]
            #                                      ].prob += extra_drop_info[i+1]
            #         self.extra_drop_item[extra_drop_list_id] = extra_drop_info_dict


class indep_drop:
    _path: str
    _pvf_dir: str
    _drop_infos: list[indep_drop_info]
    _drop_lst: lib.lst.lst
    _drop_lst_item: dict[int, lib.item.item]
    _drop_lst_item_info_dict: dict[int, dict[int, indep_drop_list_item]]

    _item_monster_map: dict[int, list[int]]
    _item_drop_infos: dict[int, list[indep_drop_info]]
    _monster_drop_map: dict[int, list[int]]
    _monster_drop_infos: dict[int, list[indep_drop_info]]

    def __init__(self, path: str, pvf_dir: str):
        self._path = path
        self._pvf_dir = pvf_dir
        self._drop_infos = []
        self._drop_lst_item = {}
        self._item_monster_map = {}
        self._item_drop_infos = {}
        self._monster_drop_map = {}
        self._monster_drop_infos = {}

        self.init_drop_lst()

        with open(path, mode='r', encoding='utf-8') as f:
            content = f.read()

            drop_str = content[content.index(
                "[independent drop]") + 18:content.index("[/independent drop]")].strip()
            single_drop_info: list[int] = []
            num = ""
            i = 0
            while i < len(drop_str):
                s = drop_str[i]
                if s >= "0" and s <= "9" or s == "-":
                    num += s
                    i += 1
                    continue

                if s == ".":
                    i += 1
                    continue

                if num == "":
                    i += 1
                    continue

                single_drop_info.append(int(num))
                num = ""
                if len(single_drop_info) < 17:
                    i += 1
                    continue

                monster = single_drop_info[1]
                item = single_drop_info[2]
                if item != 0 and item not in self._item_monster_map:
                    self._item_monster_map[item] = []
                if item != 0 and item not in self._item_drop_infos:
                    self._item_drop_infos[item] = []
                if monster not in self._monster_drop_map:
                    self._monster_drop_map[monster] = []
                if monster not in self._monster_drop_infos:
                    self._monster_drop_infos[monster] = []

                if item != 0:
                    drop_info = indep_drop_info(single_drop_info)
                    self._drop_infos.append(drop_info)
                    self._item_monster_map[item].append(monster)
                    self._item_drop_infos[item].append(drop_info)
                    self._monster_drop_map[monster].append(item)
                    self._monster_drop_infos[monster].append(drop_info)
                elif single_drop_info[-1] == 1:
                    j = i
                    for j in range(i, len(drop_str)):
                        if drop_str[j-7:j] == "[/list]":
                            break
                    raw_drop_list = drop_str[i:j]
                    drop_info = indep_drop_info(
                        single_drop_info, raw_drop_list)
                    self._monster_drop_infos[monster].append(drop_info)

                    drop_item_list = flat_drop_list_to_list(raw_drop_list)
                    i = j
                    for k in range(0, len(drop_item_list), 2):
                        item = drop_item_list[k]
                        self._monster_drop_map[monster].append(item)
                        if item not in self._item_monster_map:
                            self._item_monster_map[item] = []
                        if item not in self._item_drop_infos:
                            self._item_drop_infos[item] = []
                        self._item_monster_map[item].append(monster)
                        self._item_drop_infos[item].append(drop_info)
                elif single_drop_info[-1] == 2:
                    j = i
                    for j in range(i, len(drop_str)):
                        if drop_str[j-7:j] == "[/list]":
                            break
                    raw_drop_list = drop_str[i:j]
                    drop_info = indep_drop_info(
                        single_drop_info, raw_drop_list)
                    self._monster_drop_infos[monster].append(drop_info)

                    drop_item_list = flat_drop_list_to_list(raw_drop_list)
                    i = j
                    for lst_id in drop_item_list:
                        if lst_id not in self._drop_lst_item_info_dict:
                            print("drop lst not exists", lst_id)
                            continue
                        drop_lst_item_list = self._drop_lst_item_info_dict[lst_id]
                        for item, indep_drop_list_it in drop_lst_item_list.items():
                            self._monster_drop_map[monster].append(item)
                            if item not in self._item_monster_map:
                                self._item_monster_map[item] = []
                            if item not in self._item_drop_infos:
                                self._item_drop_infos[item] = []
                            self._item_monster_map[item].append(monster)
                            self._item_drop_infos[item].append(drop_info)
                else:
                    print("invalid indep drop", single_drop_info)

                i += 1
                single_drop_info = []

    def init_drop_lst(self):
        self._drop_lst = lib.lst.lst(os.path.join(
            self._pvf_dir, "etc/independentdrop.lst"))
        self._drop_lst_item_info_dict = {}
        for id, drop_list_path in self._drop_lst.get_item_dict().items():
            it = lib.item.item(
                self._pvf_dir, lib.pvf.ETC, os.path.join(self._pvf_dir, lib.pvf.ETC, drop_list_path))
            self._drop_lst_item[int(id)] = it

            list_tag_content = list(map(lambda x: int(x), flat_drop_list_to_list(it.get_single_tag(
                'list').get_value())))
            drop_lst_item_list: dict[int, indep_drop_list_item] = {}
            for i in range(0, len(list_tag_content), 2):
                if list_tag_content[i] not in drop_lst_item_list:
                    drop_lst_item_list[list_tag_content[i]] = indep_drop_list_item(
                        list_tag_content[i], list_tag_content[i+1])
                else:
                    drop_lst_item_list[list_tag_content[i]
                                       ].prob += list_tag_content[i+1]
            self._drop_lst_item_info_dict[int(id)] = drop_lst_item_list

    def has_item(self, item_id: int) -> bool:
        return item_id in self._item_monster_map

    def get_item_drop_monsters(self, item_id: int) -> list[int]:
        return self._item_monster_map[item_id]

    def has_monster(self, monster_id: int) -> bool:
        return monster_id in self._monster_drop_map[monster_id]

    def get_monster_drop_items(self, monster_id: int) -> list[int]:
        return self._monster_drop_map[monster_id]
