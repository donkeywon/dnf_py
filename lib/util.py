import lib.item


def extract_equ_type(it: lib.item.item):
    if not it.has_tag('equipment type'):
        return ""
    return it.get_single_tag_value(
        'equipment type').split("\t")[0].strip("`[]")


def equ_is_avatar(it: lib.item.item):
    return 'avatar' == extract_equ_type(it) or it.has_tag('avatar type select') or it.has_tag('avatar select ability')


def equ_is_title(it: lib.item.item):
    return 'title name' == extract_equ_type(it)


def equ_is_weapon(it: lib.item.item):
    return 'weapon' == extract_equ_type(it)


def equ_is_zuoyou(it: lib.item.item):
    equ_type = extract_equ_type(it)
    return 'support' == equ_type or 'magic stone' == equ_type


def equ_is_support(it: lib.item.item):
    equ_type = extract_equ_type(it)
    return 'support' == equ_type


def equ_is_magicstone(it: lib.item.item):
    equ_type = extract_equ_type(it)
    return 'magic stone' == equ_type


def equ_is_cloth(it: lib.item.item):
    equ_type = extract_equ_type(it)
    return "coat" == equ_type or "pants" == equ_type or "shoulder" == equ_type or "waist" == equ_type or "shoes" == equ_type


def equ_is_jewelry(it: lib.item.item):
    equ_type = extract_equ_type(it)
    return "amulet" == equ_type or "wrist" == equ_type or "ring" == equ_type


def equ_need_filter(name: str) -> bool:
    return "(旧)" in name or "(傀儡)" in name or "[活动" in name or "古老的" in name or "初学者的成长" in name or "茁壮冒险家的成长" in name or "APC专用" in name or "租借活动" in name or "(活动)" in name or "网吧" in name or name.startswith("84_") or name.startswith("85_") or "无限的斯特" in name or "无尽之逐神" in name or "网咖" in name or "[活動" in name or "[網咖" in name
