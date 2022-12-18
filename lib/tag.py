class tag:
    name: str
    value: str
    has_sub_tag: bool
    has_close_tag: bool
    sub_tags: list
    sub_tag_dict: dict
    def __init__(self, name, value, has_close_tag = False):
        self.name = name
        self.value = value
        self.has_sub_tag = False
        self.has_close_tag = has_close_tag
        self.sub_tags = []
        self.sub_tag_dict = {}
    def add_sub_tag(self, t):
        self.has_sub_tag = True
        self.sub_tags.append(t)
        self.sub_tag_dict[t.name] = t
    def to_string(self, depth=0):
        depth_prefix = ''
        for i in range(0, depth):
            depth_prefix += '\t'

        str = '%s[%s]' % (depth_prefix, self.name)
        if self.value != '':
            str += '\n%s\t%s' % (depth_prefix, self.value)
        if self.has_sub_tag:
            for sub_tag in self.sub_tags:
                str += '\n'
                str += sub_tag.to_string(depth+1)
        if self.has_close_tag:
            str += '\n%s[/%s]' % (depth_prefix, self.name)
        return str