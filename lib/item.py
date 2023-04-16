from __future__ import annotations

import os

from lib.tag import tag

EXT_AIC = "aic"
EXT_APD = "apd"
EXT_CRE = "cre"
EXT_DUNGEON = "dgn"
EXT_EQU = "equ"
EXT_MAP = "map"
EXT_MONSTER = "mob"
EXT_QUEST = "qst"
EXT_OBJ = "obj"
EXT_SKL = "skl"
EXT_STK = "stk"
EXT_SHP = "shp"

MERGE_TAG_KEEP_FIRST = 0
MERGE_TAG_KEEP_LAST = 1

PVF_ITEM_START = "#PVF_File\n\n"


class item:
    _tag_arr: list[tag]
    _tag_dict: dict[str, list[tag]]
    _pvf_dir_path: str
    _pvf_sub_dir: str
    _filepath: str
    _filename: str
    _ext: str
    _has_duplicate_tag: bool
    _duplicate_tags: set[str]

    def __init__(self, pvf_dir_path: str, pvf_sub_dir: str, filepath: str, warn_duplicate_tag: bool = True):
        self._pvf_dir_path = pvf_dir_path
        self._pvf_sub_dir = pvf_sub_dir
        self._ext = filepath.split(".")[-1]
        self._filename = os.path.split(filepath)[1]
        self._filepath = filepath
        self._tag_arr = []
        self._tag_dict = {}
        self._has_duplicate_tag = False
        self._duplicate_tags = set[str]()
        with open(self._filepath, mode='r', encoding='utf-8') as f:
            content = f.read()
            content_arr: list[str] = []
            value = ''
            i = 0
            while i < len(content):
                if content[i] == '[':
                    if len(content_arr) > 0:
                        content_arr.append(value)
                    value = ''
                    for j in range(i, len(content)):
                        value += content[j]
                        if content[j] == ']':
                            content_arr.append(value)
                            value = ''
                            i = j
                            break
                elif content[i] == '`':
                    value += content[i]
                    for j in range(i+1, len(content)):
                        value += content[j]
                        if content[j] == '`':
                            i = j
                            break
                else:
                    value += content[i]
                i += 1

            if value != '':
                content_arr.append(value)

            tags = self._parse_content(content_arr)
            for t in tags:
                if self.check_duplicate_tag(t):
                    self._has_duplicate_tag = True
                    self._duplicate_tags.add(t.get_name())
                    if warn_duplicate_tag:
                        print("重复的tag: %s, filepath: %s" %
                              (t.get_name(), self._filepath))
                self._tag_arr.append(t)
                if t.get_name() not in self._tag_dict:
                    self._tag_dict[t.get_name()] = []
                self._tag_dict[t.get_name()].append(t)

    def check_duplicate_tag(self, t: tag):
        tn = t.get_name()
        if self._ext == EXT_EQU:
            if tn == "layer variation" or \
                    tn == "variation" or \
                    tn == "if" or \
                    tn == "then" or \
                    tn == "equipment ani script" or \
                    tn == "animation job" or \
                    tn == "item aura" or \
                    tn == "multiple then" or \
                    tn == "icon mark" or \
                    tn == "extra icon" or \
                    tn == "skill data up" or \
                    tn == "all skill item" or \
                    tn == "level section ability" or \
                    tn == "level section ani" or \
                    tn == "piece set ability" or \
                    tn == "pvp" or \
                    tn == "active status control info" or \
                    tn == "LAYER" or \
                    tn == "expand ani" or \
                    tn == "effect" or \
                    tn.startswith("hardcoding") or \
                    "motion" in tn:
                return False
        elif self._ext == EXT_AIC:
            if tn == "targeting bonus":  # 不知道这个tag是什么意思，先不合并
                return False
        elif self._ext == EXT_STK:
            if tn == "booster select category" or \
                    tn == "package data selection" or \
                    tn == "icon mark" or \
                    tn == "booster info":
                return False
        if tn in self._tag_dict:
            return True

    def has_duplicate_tag(self) -> bool:
        return self._has_duplicate_tag

    def get_duplicate_tags(self) -> set[str]:
        return self._duplicate_tags

    def merge_duplicate_tag(self, tag_name: str, keep_first_or_last: int):
        if not self.has_tag(tag_name):
            return
        tags = self.get_tag(tag_name)
        if len(tags) == 1:
            return
        need_remove: list[tag] = []
        if keep_first_or_last == MERGE_TAG_KEEP_FIRST:
            need_remove = tags[1:]
            self.get_tag_dict()[tag_name] = [tags[0]]
        elif keep_first_or_last == MERGE_TAG_KEEP_LAST:
            need_remove = tags[:-1]
            self.get_tag_dict()[tag_name] = [tags[-1]]
        for t in need_remove:
            self.get_tag_arr().remove(t)

    def to_string(self) -> str:
        out = PVF_ITEM_START
        for i in range(len(self.get_tag_arr())):
            t = self.get_tag_arr()[i]
            out += t.to_string()
            if i == len(self.get_tag_arr()) - 1:
                out += '\n'
            else:
                out += '\n\n'
        return out

    def get_filepath(self) -> str:
        return self._filepath

    def get_pvf_dir_path(self) -> str:
        return self._pvf_dir_path

    def get_internal_path(self) -> str:
        return self._filepath[len(os.path.join(self._pvf_dir_path, self._pvf_sub_dir)):].replace("\\", "/").strip("/")

    def get_filename(self) -> str:
        return self._filename

    def get_tag_arr(self) -> list[tag]:
        return self._tag_arr

    def get_tag_dict(self) -> dict[str, list[tag]]:
        return self._tag_dict

    def get_tag(self, tag_name: str) -> list[tag]:
        return self.get_tag_dict()[tag_name]

    def get_single_tag(self, tag_name: str) -> tag:
        return self.get_tag_dict()[tag_name][0]

    def get_single_tag_value(self, tag_name: str) -> str:
        return self.get_tag_dict()[tag_name][0].get_value()

    def get_single_tag_value_or_default(self, tag_name: str, default: str) -> str:
        if not self.has_tag(tag_name):
            return default
        return self.get_single_tag_value(tag_name)

    def add_tag(self, t: tag, index: int = -1):
        if index == -1:
            index = len(self.get_tag_arr())
        self.get_tag_arr().insert(index, t)
        if t.get_name() not in self.get_tag_dict():
            self.get_tag_dict()[t.get_name()] = []
        self.get_tag_dict()[t.get_name()].append(t)

    def add_tag_after(self, t: tag, after_tag: str):
        for i in range(0, len(self.get_tag_arr())):
            if self.get_tag_arr()[i].get_name() == after_tag:
                self.add_tag(t, i+1)
                return

    def delete(self):
        os.remove(self._filepath)

    def has_tag(self, tag_name: str) -> bool:
        return tag_name in self.get_tag_dict()

    def del_tag(self, tag_name: str):
        if not self.has_tag(tag_name):
            return
        tags = self.get_tag_dict()[tag_name]
        for t in tags:
            self.get_tag_arr().remove(t)
        del self.get_tag_dict()[tag_name]

    def write(self, new_path: str):
        dir = '/'.join(new_path.replace("\\", "/").split("/")[:-1])
        if not os.path.exists(dir):
            os.makedirs(dir)
        f = open(new_path, mode='w', encoding='utf-8')
        f.write(self.to_string())
        f.close()

    def overwrite(self):
        self.write(self.get_filepath())

    @staticmethod
    def _parse_content(content_arr: list[str]) -> list[tag]:
        tags: list[tag] = []
        i = 0
        while i < len(content_arr):
            if len(content_arr[i]) > 1 and content_arr[i][0] == '[' and content_arr[i][-1] == ']':
                tag_name = content_arr[i][1:-1]
                has_close_tag = False
                has_sub_tag = False
                j = i + 1
                for j in range(i+1, len(content_arr)):
                    if content_arr[j] == '[/' + tag_name + ']':
                        has_close_tag = True
                        for k in range(i+1, j):
                            if len(content_arr[k]) > 1 and content_arr[k][0] == '[' and content_arr[k][-1] == ']':
                                has_sub_tag = True
                                break
                        break
                if has_close_tag:
                    sub_content_arr = content_arr[i:j+1]
                    i = j
                else:
                    if len(content_arr[i+1]) > 1 and content_arr[i+1][0] == '[' and content_arr[i+1][-1] == ']':
                        sub_content_arr = content_arr[i:i+1]
                    else:
                        sub_content_arr = content_arr[i:i+2]
                        i += 1
                tags.append(item._parse_tag(sub_content_arr,
                            tag_name, has_close_tag, has_sub_tag))
            i += 1
        return tags

    @staticmethod
    def _parse_tag(content_arr: list[str], tag_name: str, has_close_tag: bool, has_sub_tag: bool) -> tag:
        if len(content_arr) == 1 \
                or has_close_tag and content_arr[1].find('[/') == 0 \
                or not has_close_tag and content_arr[1].find('[') == 0:
            value = ''
        else:
            value = content_arr[1]
        value = value.strip(" \n\t")
        t = tag(tag_name, value, has_close_tag)
        if has_sub_tag:
            if has_close_tag:
                sub_tags = item._parse_content(content_arr[1:-1])
            else:
                sub_tags = item._parse_content(content_arr[1:])
            for sub_tag in sub_tags:
                t.add_sub_tag(sub_tag)
        return t
