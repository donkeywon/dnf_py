import lib.item


class shop:
    _it: lib.item.item
    _items: list[int]
    _items_map: dict[int, bool]

    def __init__(self, it: lib.item.item):
        self._it = it
        self._items = []
        self._items_map = {}
        if not it.has_tag('sell item'):
            return
        sell_item = list(map(lambda x: int(x), list(filter(lambda x: x != "" and x != "-1" and x != "-2", it.get_single_tag(
            'sell item').get_value().replace("\n", "\t").replace("\r\n", "\t").replace("\t\t", "\t").split("\t")))))
        self._items = sell_item
        for item in sell_item:
            self._items_map[item] = True

    def has_item(self, item: int) -> bool:
        return item in self._items_map

    def get_sell_items(self) -> list[int]:
        return self._items
