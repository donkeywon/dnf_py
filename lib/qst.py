import lib.item


def flat_list(s: str) -> str:
    return s.strip().replace("\n", "\t").replace("\r\n", "\t").replace("\t\t", "\t")


def flat_list_to_list(s: str) -> list[str]:
    return list(filter(lambda x: x != "", flat_list(s).split("\t")))


def flat_list_to_list_int(s: str) -> list[int]:
    return list(map(lambda x: int(x), flat_list_to_list(s)))


class qst:
    _it: lib.item.item
    _reward_type: str
    _reward_items: list[int]
    _reward_items_map: dict[int, int]
    _reward_sel_items: list[int]
    _reward_sel_items_map: dict[int, int]

    def __init__(self, it: lib.item.item):
        self._it = it
        self._reward_items = []
        self._reward_items_map = {}
        self._reward_sel_items = []
        self._reward_sel_items_map = {}
        if it.has_tag('reward_type'):
            self._reward_type = it.get_single_tag_value(
                'reward type').strip("`[]")
        self.init_reward_items()
        self.init_selection_reward_items()

    def parse_line(self, s: str) -> tuple[int, int]:
        ss = s.strip().split("\t")
        if len(ss) == 1:
            return (int(ss[0]), 1)
        elif len(ss) == 2:
            return (int(ss[0]), int(ss[1]))
        elif len(ss) == 5:
            return (int(ss[0]), int(ss[4]))
        else:
            return (0, 0)

    def init_reward_items(self):
        it = self._it
        if not it.has_tag('reward int data'):
            return
        reward_lines = list(filter(lambda x: x != "", it.get_single_tag_value(
            'reward int data').strip().split("\n")))
        for line in reward_lines:
            item, count = self.parse_line(line)
            self._reward_items.append(item)
            self._reward_items_map[item] = count

            # reward_items = flat_list_to_list_int(
            #     it.get_single_tag_value('reward int data'))
            # if len(reward_items) % 2 != 0:
            #     print("!!!!!!!!!! invalid quest reward int data",
            #           it.get_internal_path())
            #     return
            # self._reward_items = reward_items
            # self._reward_items_map = {}
            # for i in range(0, len(self._reward_items), 2):
            #     self._reward_items_map[self._reward_items[i]
            #                            ] = self._reward_items[i+1]

    def init_selection_reward_items(self):
        it = self._it
        if not it.has_tag('reward selection int data'):
            return
        reward_lines = list(filter(lambda x: x != "", it.get_single_tag_value(
            'reward selection int data').strip().split("\n")))
        for line in reward_lines:
            item, count = self.parse_line(line)
            self._reward_sel_items.append(item)
            self._reward_sel_items_map[item] = count

        # reward_sel = flat_list_to_list(
        #     it.get_single_tag_value('reward selection int data'))
        # if len(reward_sel) == 0:
        #     return
        # self._reward_sel_items = []
        # self._reward_sel_items_map = {}
        # if reward_sel[1].startswith("`"):
        #     if len(reward_sel) % 5 != 0:
        #         print("!!!!!!!!!! invalid quest reward int data",
        #               it.get_internal_path())
        #     for i in range(0, len(reward_sel), 5):
        #         item = int(reward_sel[i])
        #         count = int(reward_sel[i+4])
        #         self._reward_sel_items.append(item)
        #         self._reward_sel_items_map[item] = count
        # else:
        #     if len(reward_sel) % 2 != 0:
        #         print("!!!!!!!!!! invalid quest reward int data",
        #               it.get_internal_path())
        #     for i in range(0, len(reward_sel), 2):
        #         item = int(reward_sel[i])
        #         count = int(reward_sel[i+1])
        #         self._reward_sel_items.append(item)
        #         self._reward_sel_items_map[item] = count

    def has_reward_item(self, item: int) -> bool:
        return item in self._reward_items_map

    def has_reward_sel_item(self, item: int) -> bool:
        return item in self._reward_sel_items_map

    def has_item(self, item: int) -> bool:
        return self.has_reward_item(item) or self.has_reward_sel_item(item)

    def get_reward_item_count(self, item: int) -> int:
        return self._reward_items_map[item]

    def get_reward_sel_item_count(self, item: int) -> int:
        return self._reward_sel_items_map[item]

    def get_reward_items_map(self) -> dict[int, int]:
        return self._reward_items_map

    def get_reward_sel_items_map(self) -> dict[int, int]:
        return self._reward_sel_items_map
