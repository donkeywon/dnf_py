from __future__ import annotations


class tag:
    _name: str
    _value: str
    _has_sub_tag: bool
    _has_close_tag: bool
    _sub_tags: list[tag]

    def __init__(self, name: str, value: str, has_close_tag: bool = False):
        self._name = name
        self._value = value
        self._has_sub_tag = False
        self._has_close_tag = has_close_tag
        self._sub_tags = []

    def add_sub_tag(self, t: tag):
        self._has_sub_tag = True
        self.get_sub_tags().append(t)

    def clean_sub_tags(self):
        self._sub_tags = []

    def get_name(self) -> str:
        return self._name

    def get_value(self) -> str:
        return self._value

    def set_value(self, value: str):
        self._value = value

    def has_sub_tag(self) -> bool:
        return self._has_sub_tag

    def has_sub_tag_name(self, name: str) -> bool:
        for t in self.get_sub_tags():
            if t.get_name() == name:
                return True
        return False

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
        return self._has_close_tag

    def get_sub_tags(self) -> list[tag]:
        return self._sub_tags

    def get_sub_tag(self, tag_name: str) -> list[tag]:
        sts: list[tag] = []
        sub_tags = self.get_sub_tags()
        if len(sub_tags) == 0:
            return sts
        for t in sub_tags:
            if t.get_name() == tag_name:
                sts.append(t)
        return sts

    def get_single_sub_tag(self, tag_name: str) -> tag:
        return self.get_sub_tag(tag_name)[0]

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
