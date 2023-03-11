from __future__ import annotations


class tag:
    __name: str
    __value: str
    __has_sub_tag: bool
    __has_close_tag: bool
    __sub_tags: list[tag]

    def __init__(self, name: str, value: str, has_close_tag: bool = False):
        self.__name = name
        self.__value = value
        self.__has_sub_tag = False
        self.__has_close_tag = has_close_tag
        self.__sub_tags = []

    def add_sub_tag(self, t: tag):
        self.__has_sub_tag = True
        self.get_sub_tags().append(t)

    def get_name(self) -> str:
        return self.__name

    def get_value(self) -> str:
        return self.__value
    
    def set_value(self, value: str):
        self.__value = value

    def has_sub_tag(self) -> bool:
        return self.__has_sub_tag
    
    def get_sub_tag_recurse(self, tag_name: str) -> list[tag]:
        sub_tags: list[tag] = []
        if not self.has_sub_tag():
            return sub_tags
        for sub_tag in self.get_sub_tags():
            if sub_tag.get_name() == tag_name:
                sub_tags.append(sub_tag)
            sub_tags += sub_tag.get_sub_tag_recurse(tag_name)
        return sub_tags

    def has_close_tag(self) -> bool:
        return self.__has_close_tag

    def get_sub_tags(self) -> list[tag]:
        return self.__sub_tags

    def to_string(self, depth: int = 0) -> str:
        depth_prefix = ''
        for _ in range(0, depth):
            depth_prefix += '\t'

        str = '%s[%s]' % (depth_prefix, self.get_name())
        if self.get_value() != '':
            str += '\n%s\t%s' % (depth_prefix, self.get_value())
        if self.has_sub_tag():
            for sub_tag in self.get_sub_tags():
                str += '\n'
                str += sub_tag.to_string(depth+1)
        if self.has_close_tag():
            str += '\n%s[/%s]' % (depth_prefix, self.get_name())
        return str
