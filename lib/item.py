from __future__ import annotations

from lib.tag import tag

class item:
    __tag_arr: list[tag]
    __tag_dict: dict[str, tag]
    __filepath: str
    def __init__(self, filepath: str):
        self.__filepath = filepath
        self.__tag_arr = []
        self.__tag_dict = {}
        with open(filepath, mode='r', encoding='utf-8') as f:
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
                        if content[j] == ']' and j < len(content) - 1 and content[j+1] != '`':
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
                self.__tag_arr.append(t)
                self.__tag_dict[t.get_name()] = t
    def to_string(self) -> str:
        out = "#PVF_File\n\n"
        for i in range(len(self.get_tag_arr())):
            t = self.get_tag_arr()[i]
            out += t.to_string()
            if i == len(self.get_tag_arr()) - 1:
                out += '\n'
            else:
                out += '\n\n'
        return out
    def get_filepath(self) -> str:
        return self.__filepath
    def get_tag_arr(self) -> list[tag]:
        return self.__tag_arr
    def get_tag_dict(self) -> dict[str, tag]:
        return self.__tag_dict
    def get_tag(self, tag_name: str) -> tag:
        return self.get_tag_dict()[tag_name]
    def add_tag(self, t: tag):
        self.get_tag_arr().append(t)
        self.get_tag_dict()[t.get_name()] = t
    def has_tag(self, tag_name: str) -> bool:
        return tag_name in self.get_tag_dict()
    def write(self, new_path:str =''):
        path = self.get_filepath()
        if new_path != '':
            path = new_path
        f = open(path, mode='w', encoding='utf-8')
        f.write(self.to_string())
        f.close()
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
                tags.append(item._parse_tag(sub_content_arr, tag_name, has_close_tag, has_sub_tag))
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
