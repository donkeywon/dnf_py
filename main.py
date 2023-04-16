import os
import math
import opencc
import shutil
import distutils.dir_util

import lib.util as util
import lib.pvf as lib_pvf
import lib.item as lib_item
import lib.lst as lib_lst
import lib.tag as lib_tag
import lib.equ_partset as lib_equ_partset
import lib.cashshop as lib_cashshop
import lib.skl as lib_skl
import lib.indep_drop as lib_indep_drop
import lib.shop as lib_shop
import lib.qst


def sort_hellparty():
    it = lib_item.item(
        "", "", "D:\\workspace\\code\\other\\pvf_1031\\etc\\hellparty.etc")
    group_tag = it.get_single_tag('hellparty monster group')
    groups = group_tag.get_sub_tags()
    groups_tuple_list: list[tuple[lib_tag.tag, lib_tag.tag]] = []
    for i in range(0, len(groups), 2):
        groups_tuple_list.append((groups[i], groups[i+1]))
    groups_tuple_list = sorted(
        groups_tuple_list, key=lambda x: int(x[0].get_value()))
    group_tag.clean_sub_tags()
    for group_tuple in groups_tuple_list:
        group_tag.add_sub_tag(group_tuple[0])
        group_tag.add_sub_tag(group_tuple[1])
    it.overwrite()


def sort_lst(lst_path: str):
    l = lib_lst.lst(lst_path)
    l.overwrite()


def sort_equ_partset(pvf_dir: str, pvf_sub_dir: str, filepath: str):
    equ_ps = lib_equ_partset.equ_partset(
        lib_item.item(pvf_dir, pvf_sub_dir, filepath))
    equ_ps.get_item().overwrite()


def split_equ_by_rarity_to_new_path():
    path = "D:\\workspace\\code\\other\\pvf_1031\\"
    # path = "C:\\Users\\donkeywon\\Desktop\\86\\"

    d = lib_pvf.pvf.read_dir(os.path.join(
        path, "equipment\\character\\thief\\weapon"), lib_item.EXT_EQU, warn_duplicate_tag=True)

    for fpath, i in d.items():
        if 'avatar\\' in i.get_filepath() or \
            '\\etc\\' in i.get_filepath() or \
            '\\title\\' in i.get_filepath() or \
                'pvp' in i.get_filepath() or \
            '(舊)' in i.get_tag('name')[0].get_value() or \
                '(旧)' in i.get_tag('name')[0].get_value():
            continue

        if not i.has_tag('grade'):
            continue

        grade = int(i.get_tag('grade')[0].get_value())
        new_path = os.path.join("C:\\Users\\donkeywon\\Desktop\\pvf_1031_s\\", "new", i.get_tag(
            'rarity')[0].get_value(), fpath.removeprefix(path))
        dir = os.path.split(new_path)[0]
        if not os.path.exists(dir):
            os.makedirs(dir)
        i.write(new_path)


def fix_avatar_type_select():
    equ_lst = lib_lst.lst(
        "D:\\workspace\\code\\other\\pvf_1031\\equipment\\equipment.lst")

    avatar_dirs = ["swordman/avatar", "fighter/avatar", "fighter/at_avatar",
                   "gunner/avatar", "gunner/at_avatar", "mage/avatar",
                   "mage/at_avatar", "priest/avatar", "thief/avatar"]
    avatar_type_dirs = ["cap", "hair", "face", "neck",
                        "coat", "belt", "pants", "shoes", "skin"]

    output: list[str] = []

    idx = 1
    for avatar_dir in avatar_dirs:
        _idx = 0
        for avatar_type in avatar_type_dirs:
            id_rare_list: list[str] = []
            id_normal_list: list[str] = []
            items = lib_pvf.pvf.read_dir(os.path.join("D:\\workspace\\code\\other\\pvf_1031\\equipment\\character",
                                                      avatar_dir, avatar_type), lib_item.EXT_EQU, "D:\\workspace\\code\\other\\pvf_1031", lib_pvf.EQU)
            for it in items.values():
                if 'weapon/' in it.get_internal_path():
                    continue
                if it.get_single_tag('name').get_value() == '``':
                    continue
                if not equ_lst.has_path(it.get_internal_path()):
                    continue
                tag_value = ''
                if it.has_tag('grade') and it.get_single_tag('grade').get_value() == '3':
                    id_rare_list.append(
                        equ_lst.get_id_by_path(it.get_internal_path()))
                    tag_value = '''7	0	0	100	0
30	0	0	300	0
0	0	0	1000	0'''
                else:
                    id_normal_list.append(
                        equ_lst.get_id_by_path(it.get_internal_path()))
                    tag_value = '''7	0	0	50	0
30	0	0	150	0
0	0	0	500	0'''
                if not it.has_tag('avatar type select'):
                    it.add_tag(lib_tag.tag(
                        'avatar type select', tag_value, True))
                else:
                    it.get_single_tag(
                        'avatar type select').set_value(tag_value)
                it.overwrite()

            start_idx = 1000000 * idx + 100000 * _idx
            for id in id_normal_list:
                output.append(str(start_idx) + "\t" + id +
                              "\t3\t0\t0\t-1\t-1\t" + id + "\t4\t0\t0\t-1\n")
                start_idx += 1
            for id in id_rare_list:
                output.append(str(start_idx) + "\t" + id +
                              "\t3\t0\t0\t-1\t-1\t" + id + "\t4\t0\t0\t-1\n")
                start_idx += 1
            _idx += 1
        idx += 1

    f = open('avatar.txt', mode='w', encoding='utf-8')
    for line in output:
        f.write(line)
    f.close()


def fix_hell_map_has_no_hellparty_group():
    path = "D:\\workspace\\code\\other\\pvf_1031\\"
    # path = "C:\\Users\\donkeywon\\Desktop\\86\\"

    hellparty_item = lib_item.item(
        "", "", "D:\\workspace\\code\\other\\pvf_1031\\etc\\hellparty.etc")
    group_tag = hellparty_item.get_single_tag('hellparty monster group')
    groups = group_tag.get_sub_tags()
    groups_map = {}
    for i in range(0, len(groups), 2):
        groups_map[groups[i].get_value()] = 1

    d = lib_pvf.pvf.read_dir(os.path.join(
        path, "map"), lib_item.EXT_MAP, warn_duplicate_tag=False)

    for fpath, it in d.items():
        if not it.has_tag('special passive object'):
            continue

        spo = it.get_single_tag('special passive object').get_value()
        if '[hellparty]' not in spo:
            continue

        spos = spo.split('`[hellparty]`')
        hellparty: list[str] = spos[1].split(
            '`[/hellparty]`')[0].strip().split("\t")
        hellparty = list(filter(lambda x: x != '', list(
            map(lambda x: x.strip(), hellparty))))

        for i in range(0, len(hellparty), 3):
            if hellparty[i] not in groups_map:
                print(it.get_internal_path())


def compare_and_fix_skill_static():
    origin_path = "C:\\Users\\donkeywon\\Desktop\\86"
    pvf_path = "D:\\workspace\\code\\other\\pvf_1031"
    d = lib_pvf.pvf.read_dir(
        os.path.join(pvf_path, lib_pvf.SKL), lib_item.EXT_SKL, pvf_path, "skill")

    skl_lst = lib_lst.lst(os.path.join(
        pvf_path, lib_pvf.SKL, "gunnerskill.lst"))

    for it in d.values():
        # skl = lib_skl.skl(it)
        # if skl.get_required_level() < 10:
        #     continue

        # skl.shrink_dgn_lvl_info(80, 10)
        # skl.shrink_dgn_lvl_info(70, 20)
        # skl.shrink_dgn_lvl_info(60, 30)
        # skl.shrink_dgn_lvl_info(50, 30)
        # skl.shrink_dgn_lvl_info(40, 40)
        # skl.shrink_dgn_lvl_info(30, 50)
        # skl.shrink_dgn_lvl_info(20, 50)
        # skl.shrink_dgn_lvl_info(10, 50)

        # skl.shrink_pvp_lvl_info(80, 10)
        # skl.shrink_pvp_lvl_info(70, 20)
        # skl.shrink_pvp_lvl_info(60, 30)
        # skl.shrink_pvp_lvl_info(50, 30)
        # skl.shrink_pvp_lvl_info(40, 40)
        # skl.shrink_pvp_lvl_info(30, 50)
        # skl.shrink_pvp_lvl_info(20, 50)
        # skl.shrink_pvp_lvl_info(10, 50)

        # skl.overwrite()

        origin_skl_path = os.path.join(
            origin_path, lib_pvf.SKL, it.get_internal_path())
        if not os.path.exists(origin_skl_path):
            continue
        origin_it = lib_item.item(
            origin_path, lib_pvf.SKL, origin_skl_path, False)
        if not origin_it.has_tag('dungeon') and not origin_it.has_tag('level info'):
            continue
        for t in ['static data', 'cool time', 'consume MP']:
            if origin_it.has_tag('dungeon') and not origin_it.get_single_tag('dungeon').has_sub_tag_name(t):
                continue
            if origin_it.has_tag('dungeon'):
                origin_static_data = origin_it.get_single_tag(
                    'dungeon').get_single_sub_tag(t).get_value()
                new_static_data = it.get_single_tag(
                    'dungeon').get_single_sub_tag(t).get_value()
                if origin_static_data != new_static_data:
                    path = it.get_internal_path()
                    if skl_lst.has_path(path):
                        print(skl_lst.get_id_by_path(path), path, t)
                    else:
                        print(path, t)
                    # origin_it.write(os.path.join(
                    #     "C:\\Users\\donkeywon\\Desktop\\1031.origin.static", origin_it.get_internal_path()))
            elif origin_it.has_tag(t) and it.has_tag(t):
                origin_static_data = origin_it.get_single_tag(
                    t).get_value()
                new_static_data = it.get_single_tag(
                    t).get_value()
                if origin_static_data != new_static_data:
                    path = it.get_internal_path()
                    if skl_lst.has_path(path):
                        print(skl_lst.get_id_by_path(path), path, t)
                    else:
                        print(path, t)
                    # origin_it.write(os.path.join(
                    #     "C:\\Users\\donkeywon\\Desktop\\1031.origin.static", origin_it.get_internal_path()))


def calc_ss_need_material(level):
    if level == "45":
        return "3260\t2000"
    elif level == "50":
        return "3260\t4000"
    elif level == "55":
        return "3260\t6000"
    elif level == "60":
        return "3260\t8000"
    elif level == "65":
        return "3285\t1000"
    elif level == "70":
        return "3285\t1500"
    elif level == "75":
        return "3285\t2000"
    elif level == "80":
        return "3285\t2500"
    elif level == "85":
        return "3285\t3000"
    elif int(level) < 45:
        return "3260\t900"
    else:
        return "3285\t9999"


def calc_value(name, level, rarity):
    if rarity == "2":
        if "傳承" in name or "传承" in name:
            return str(int(level) * 30000)
        else:
            return str(int(level) * 10000)
    elif rarity == "3":
        return str(int(level) * 50000)
    elif rarity == "4":
        return str(int(level) * 100000)
    elif rarity == "5":
        return str(int(level) * 30000)
    else:
        return str(int(level) * 10000)


def calc_price(name, level, rarity):
    if rarity == "2":
        if "傳承" in name or "传承" in name or "[random option]" in name:
            return str(int(level) * 100000)
        else:
            return str(int(level) * 10000)
    elif rarity == "3":
        return str(int(level) * 1000000)
    elif rarity == "4":
        return str(int(level) * 1000000)
    elif rarity == "5":
        return str(int(level) * 100000)
    else:
        return str(int(level) * 10000)


def gen_price_and_material():
    d = lib_pvf.pvf.read_dir(
        "D:\\workspace\\code\\other\\pvf_1031\\equipment\\character", lib_item.EXT_EQU)
    for it in d.values():
        if it.has_tag('equipment type') and 'avatar' in it.get_single_tag('equipment type').get_value() or it.has_tag('avatar type select') or it.has_tag('avatar select ability') or not it.has_tag('rarity') or not it.has_tag('name') or not it.has_tag('minimum level'):
            continue

        rarity = it.get_single_tag('rarity').get_value()
        if rarity != '4' and rarity != '2' and rarity != '3' and rarity != '5':
            continue

        name = it.get_single_tag('name').get_value()
        minimum_level = it.get_single_tag('minimum level').get_value()
        if rarity == '4':
            if not it.has_tag('need material'):
                it.add_tag(lib_tag.tag("need material",
                                       calc_ss_need_material(minimum_level)))
            else:
                need_material = it.get_single_tag('need material')
                if need_material.get_value().startswith('3285') or need_material.get_value().startswith('3260'):
                    need_material.set_value(
                        calc_ss_need_material(minimum_level))
                elif not need_material.get_value().startswith('2749212'):
                    print(it.get_internal_path(),
                          it.get_single_tag('name').get_value())
        if not it.has_tag('price'):
            it.add_tag(lib_tag.tag('price', calc_price(
                name, minimum_level, rarity)))
        else:
            it.get_single_tag('price').set_value(
                calc_price(name, minimum_level, rarity))
        if not it.has_tag('value'):
            it.add_tag(lib_tag.tag('value', calc_value(
                name, minimum_level, rarity)))
        else:
            it.get_single_tag('value').set_value(
                calc_value(name, minimum_level, rarity))
        it.overwrite()


def is_not_need_creation_rate(name: str) -> bool:
    return "(旧)" in name or "(傀儡)" in name or "[活动" in name or "古老的" in name or "初学者的成长" in name or "茁壮冒险家的成长" in name or "APC专用" in name or "租借活动" in name or "(活动)" in name or "网吧" in name or name.startswith("84_") or name.startswith("85_") or "无限的斯特" in name or "无尽之逐神" in name or "网咖" in name


def fix_creation_rate():
    pvf_dir = "D:\\workspace\\code\\other\\pvf_1031"
    equ_lst = lib_lst.lst(os.path.join(pvf_dir, "equipment\\equipment.lst"))
    indep_drop = lib_indep_drop.indep_drop(os.path.join(
        pvf_dir, "etc\\independent_drop.etc"), pvf_dir)

    d = lib_pvf.pvf.read_dir(os.path.join(
        pvf_dir, "n_quest"), lib_item.EXT_QUEST, pvf_dir, lib_pvf.QUEST, False)
    qsts: list[lib.qst.qst] = []
    for it in d.values():
        qsts.append(lib.qst.qst(it))

    shop_lst = lib_lst.lst(os.path.join(pvf_dir, "itemshop\\itemshop.lst"))
    shops: dict[int, lib_shop.shop] = {}
    for shop_id, path in shop_lst.get_item_dict().items():
        shops[int(shop_id)] = lib_shop.shop(lib_item.item(
            pvf_dir, lib_pvf.SHP, os.path.join(pvf_dir, lib_pvf.SHP, path), False))

    d = lib_pvf.pvf.read_dir(
        os.path.join(pvf_dir, "equipment\\character"), lib_item.EXT_EQU, pvf_dir, lib_pvf.EQU, filter_dir=["avatar"])
    for it in d.values():
        if not it.has_tag('equipment type') or it.has_tag('equipment type') and ('avatar' in it.get_single_tag('equipment type').get_value() or 'title' in it.get_single_tag('equipment type').get_value()) or it.has_tag('avatar type select') or it.has_tag('avatar select ability') or not it.has_tag('rarity') or not it.has_tag('name') or not it.has_tag('minimum level'):
            continue

        if util.equ_is_title(it):
            continue

        name = it.get_single_tag_value('name')
        if '释魂之真灵' in name or is_not_need_creation_rate(name):
            continue

        if it.has_tag('creation rate') and it.get_single_tag('creation rate').get_value() != '0':
            continue

        if not equ_lst.has_path(it.get_internal_path()):
            continue

        item_id = int(equ_lst.get_id_by_path(it.get_internal_path()))
        if indep_drop.has_item(item_id):
            continue

        found_in_shop = False
        for shop_id, shop in shops.items():
            if shop.has_item(item_id):
                found_in_shop = True
                break
        if found_in_shop:
            continue

        found_in_qst = False
        for qst in qsts:
            if qst.has_item(item_id):
                found_in_qst = True
                break
        if found_in_qst:
            continue

        if it.get_single_tag('rarity').get_value() == "3":
            print(item_id, it.get_single_tag_value('name'),
                  it.get_single_tag_value('rarity'))


def remove_duplicate_equ():
    pvf_dir = "D:\\workspace\\code\\other\\pvf_1031"
    equ_lst = lib_lst.lst(os.path.join(pvf_dir, "equipment\\equipment.lst"))
    d = lib_pvf.pvf.read_dir(
        os.path.join(pvf_dir, "equipment\\character"), lib_item.EXT_EQU, pvf_dir, lib_pvf.EQU)
    equ_name_dict: dict[str, tuple[int, str]] = {}
    for it in d.values():
        if not it.has_tag('name'):
            continue
        if it.get_single_tag('name').get_value() == '``':
            continue
        if util.equ_is_avatar(it):
            continue
        internal_path = it.get_internal_path()
        if not equ_lst.has_path(internal_path):
            continue
        if it.has_tag('rarity') and it.get_single_tag('rarity').get_value() != "5":
            continue
        name = it.get_single_tag('name').get_value().strip("`")
        id = int(equ_lst.get_id_by_path(it.get_internal_path()))

        if name in equ_name_dict:
            print(name, equ_name_dict[name][0],
                  equ_name_dict[name][1], id, internal_path)
            continue
        equ_name_dict[name] = (id, internal_path)


def print_creation_rate():
    # rarity = "1"
    # min_lvl = 50
    # max_lvl = 60

    pvf_dir = "D:\\workspace\\code\\other\\pvf_1031"

    equ_lst = lib_lst.lst(os.path.join(pvf_dir, "equipment\\equipment.lst"))
    indep_drop = lib_indep_drop.indep_drop(os.path.join(
        pvf_dir, "etc\\independent_drop.etc"), pvf_dir)

    d = lib_pvf.pvf.read_dir(os.path.join(
        pvf_dir, "n_quest"), lib_item.EXT_QUEST, pvf_dir, lib_pvf.QUEST, False)
    qst_items: dict[int, int] = {}
    for it in d.values():
        qst = lib.qst.qst(it)
        qst_items.update(qst.get_reward_items_map())
        qst_items.update(qst.get_reward_sel_items_map())

    shop_lst = lib_lst.lst(os.path.join(pvf_dir, "itemshop\\itemshop.lst"))
    shops: dict[int, lib_shop.shop] = {}
    for shop_id, path in shop_lst.get_item_dict().items():
        shops[int(shop_id)] = lib_shop.shop(lib_item.item(
            pvf_dir, lib_pvf.SHP, os.path.join(pvf_dir, lib_pvf.SHP, path), False))

    d = lib_pvf.pvf.read_dir(
        os.path.join(pvf_dir, "equipment\\character"), lib_item.EXT_EQU, pvf_dir, lib_pvf.EQU, filter_dir=["avatar"])
    for rarity in ["1", "2", "3", "4", "5"]:
        for lvl in range(0, 90, 10):
            min_lvl = lvl
            max_lvl = lvl + 10

            out = ""
            for it in d.values():
                if util.equ_is_avatar(it) or util.equ_is_title(it):
                    continue
                if not it.has_tag('rarity') or not it.has_tag('minimum level') or not it.has_tag('name'):
                    continue

                if not it.has_tag('creation rate'):
                    continue

                if int(it.get_single_tag_value('minimum level')) <= min_lvl and int(it.get_single_tag_value('minimum level')) > max_lvl:
                    continue

                name = it.get_single_tag_value('name')
                if is_not_need_creation_rate(name):
                    continue

                if not equ_lst.has_path(it.get_internal_path()):
                    continue

                item_id = int(equ_lst.get_id_by_path(it.get_internal_path()))
                # if indep_drop.has_item(item_id):
                #     continue

                if item_id in qst_items:
                    continue

                found_in_shop = False
                for shop_id, shop in shops.items():
                    if shop.has_item(item_id):
                        found_in_shop = True
                        break
                if found_in_shop:
                    continue

                if it.get_single_tag_value('rarity') == rarity and int(it.get_single_tag_value('minimum level')) > min_lvl and int(it.get_single_tag_value('minimum level')) <= max_lvl:
                    out += it.get_single_tag_value_or_default('creation rate', "-1") + "\t" + it.get_single_tag_value(
                        'name') + "\t" + it.get_internal_path() + "\n"
            fn = "print_creation_rate_" + rarity + "_" + \
                str(min_lvl) + "_" + str(max_lvl) + ".txt"
            print(fn)
            with open(fn, mode='w', encoding='utf-8') as f:
                f.write(out)


def change_creation_rate_batch():
    pvf_dir = "D:\\workspace\\code\\other\\pvf_1031"
    equ_lst = lib_lst.lst(os.path.join(pvf_dir, "equipment\\equipment.lst"))

    d = lib_pvf.pvf.read_dir(
        os.path.join(pvf_dir, "equipment\\character"), lib_item.EXT_EQU, pvf_dir, lib_pvf.EQU, filter_dir=["avatar"])
    for it in d.values():
        if not it.has_tag('name'):
            continue

        internal_path = it.get_internal_path()
        if not equ_lst.has_path(internal_path):
            continue

        name = it.get_single_tag('name').get_value().strip("`")
        # if "羽之痕项" in name or "羽之痕戒" in name or "羽之痕手镯" in name or "光之恩赐黄金" in name or "太阳神之庇佑黄金" in name or "精灵之祝福黄金" in name:
        #     for t in it.get_tag('creation rate'):
        #         t.set_value("150")
        #     it.overwrite()
        #     print(name)
        if internal_path in [


        ]:
            # if not it.has_tag('attach type') or it.has_tag('attach type') and "sealing" not in it.get_single_tag_value("attach type"):
            #     continue

            if name.startswith("高科技") or name.startswith("84_") or name.startswith("85_"):
                continue

            cr = "200"
            if util.equ_is_weapon(it):
                cr = "200"
            if not it.has_tag('creation rate'):
                it.add_tag(lib_tag.tag('creation rate', cr))
            else:
                for t in it.get_tag('creation rate'):
                    t.set_value(cr)
            it.overwrite()
            print(name)

# change_creation_rate_batch()

# print_creation_rate()

# sort_lst("D:\\workspace\\code\\other\\pvf_1031\\creature\\creature.lst")


# compare_and_fix_skill_static()

# s = '''2747183	2747184	10006791	400960006	11805	11806	11807
# 11954	11955	11959	11956	11969	11970	11971
# 11957	11958	64015	2747170	2747179	2747180	2747181
# 2747182	2747171	2747172	2747173	2747174	2747175	2747176
# 2747177	2747178	-1	-1	-1	-1	-1
# -1	-1	-1	-1	-1	-1	-1
# 2747196	2747197	2747198	2747199	10006792	400970006	64501
# 11808	11809	11810	11972	11973	11974	11975
# 11980	11981	11982	11983	11984	2747185	2747186
# 2747187	2747188	2747189	2747190	2747191	2747192	2747193
# 2747194	2747195	10006798	-1	-1	-1	-1
# -1	-1	-1	-1	-1	-1	-1
# 2747166	2747167	2747168	2747169	10006790	10006796	400950006
# 63521	11811	11812	11813	11950	11951	11952
# 11953	11976	11977	11978	11979	11985	11986
# 11987	11988	2747155	2747156	2747157	2747158	2747159
# 2747160	2747161	2747162	2747163	2747164	2747165	-1
# -1	-1	-1'''
# shop_ids = list(filter(lambda x: x != "-1" and x != "",
#                 s.replace("\n", "\t").replace("\t\t", "\t").split("\t")))

# bag_cre_ids = []

# bag_ids = ["2747183", "2747184", "10006791", "400960006", "11805", "11806", "11807", "11954", "11955", "11959", "11956", "11969", "11970", "11971", "11957", "11958", "64015", "2747170", "2747179", "2747180", "2747181", "2747182", "2747171", "2747172", "2747173", "2747174", "2747175", "2747176", "2747177", "2747178", "2747196", "2747197", "2747198", "2747199", "10006792", "400970006", "64501", "11808", "11809", "11810", "11972", "11973", "11974", "11975", "11980", "11981", "11982", "11983",
#            "11984", "2747185", "2747186", "2747187", "2747188", "2747189", "2747190", "2747191", "2747192", "2747193", "2747194", "2747195", "10006798", "2747166", "2747167", "2747168", "2747169", "10006790", "10006796", "400950006", "63521", "11811", "11812", "11813", "11950", "11951", "11952", "11953", "11976", "11977", "11978", "11979", "11985", "11986", "11987", "11988", "2747155", "2747156", "2747157", "2747158", "2747159", "2747160", "2747161", "2747162", "2747163", "2747164", "2747165"]


# pvf_path = "D:\\workspace\\code\\other\\pvf_1031"
# lst = lib_lst.lst(
#     "D:\\workspace\\code\\other\\pvf_1031\\equipment\\equipment.lst")
# for id, path in lst.get_item_dict().items():
#     if not path.startswith("character/common/title/"):
#         continue
#     it = lib_item.item(pvf_path, lib_pvf.EQU, os.path.join(
#         pvf_path, lib_pvf.EQU, lst.get_path_by_id(id)), False)
#     name = it.get_single_tag_value('name')
#     if name.strip('` ') == "":
#         continue
#     rarity = int(it.get_single_tag_value('rarity'))
#     if rarity <= 2:
#         print(id, 1000, 1)
#     elif rarity == 3:
#         print(id, 100, 1)
#     elif rarity == 4:
#         print(id, 10, 1)


# shop_ids = ["2610039", "2610040", "2610041", "2610042", "2610043", "2610044", "2610048", "3166", "3167", "2610030", "2610031", "2610032", "2610033", "2610047", "2610034", "2610035", "2610036", "2610037", "2610038", "2610001", "2610002", "2610003", "2610004", "2610005", "2610006", "2610007", "2610008", "2610009", "2610010", "2610011", "2610012",
#             "2610013", "2610014", "2610015", "2610016", "2610017", "2610018", "2610019", "2610020", "2610021", "2610022", "2610023", "2610024", "2610025", "2610026", "2610027", "2610028", "2610029", "3227", "1150", "1151", "1153", "1154", "1156", "1157", "1159", "1160", "1162", "1163", "1165", "1166", "1168", "1169", "1192", "1193", "1021", "1020", "1022", "1023"]
# old_pvf_path = "C:\\Users\\donkeywon\\Desktop\\86"
# pvf_path = "D:\\workspace\\code\\other\\pvf_1031"
# equ_lst = lib_lst.lst(
#     os.path.join(pvf_path, "equipment\\equipment.lst"))
# stk_lst = lib_lst.lst(
#     os.path.join(pvf_path, "stackable\\stackable.lst"))
# old_equ_lst = lib_lst.lst(
#     os.path.join(old_pvf_path, "equipment\\equipment.lst"))
# old_stk_lst = lib_lst.lst(
#     os.path.join(old_pvf_path, "stackable\\stackable.lst"))

# for id in shop_ids:
#     if not stk_lst.has_id(id):
#         continue
#     internal_path = stk_lst.get_path_by_id(id)
#     it = lib_item.item(pvf_path, lib_pvf.STK,
#                        os.path.join(pvf_path, lib_pvf.STK, internal_path))
#     old_it = lib_item.item(old_pvf_path, lib_pvf.STK,
#                            os.path.join(old_pvf_path, lib_pvf.STK, internal_path))
#     for tag in ['price', 'need material']:
#         if not old_it.has_tag(tag):
#             continue
#         if not it.has_tag(tag):
#             it.add_tag(lib_tag.tag(tag, old_it.get_single_tag_value(tag)))
#         else:
#             if old_it.get_single_tag_value(tag) != it.get_single_tag_value(tag):
#                 it.get_single_tag(tag).set_value(
#                     old_it.get_single_tag_value(tag))
#         it.overwrite()

# 独立掉落添加到选图界面
# 英雄级ai
# 袖珍罐

def check_skl_column():
    skl_exp_pvf_path = "C:\\Users\\donkeywon\\Desktop\\86"
    # skl_exp_pvf_path = "C:\\Users\\donkeywon\\Desktop\\全职业动静态技能数据"
    pvf_path = "D:\\workspace\\code\\other\\pvf_1031"

    d = lib_pvf.pvf.read_dir(os.path.join(
        pvf_path, lib_pvf.SKL), lib_item.EXT_SKL, pvf_path, lib_pvf.SKL, False)

    for it in d.values():
        if not it.has_tag('level info') and not it.has_tag('dungeon'):
            continue

        path = os.path.join(skl_exp_pvf_path, lib_pvf.SKL,
                            it.get_internal_path())
        if not os.path.exists(path):
            continue
        skl_exp_it = lib_item.item(skl_exp_pvf_path, lib_pvf.SKL, os.path.join(
            skl_exp_pvf_path, lib_pvf.SKL, it.get_internal_path()), False)
        if not skl_exp_it.has_tag('level info') and not skl_exp_it.has_tag('dungeon'):
            continue

        it_column = ""
        if it.has_tag('level info'):
            lvl_info = it.get_single_tag_value('level info')
            it_column = lvl_info.split("\n")[0].strip()
        elif it.has_tag('dungeon') and it.get_single_tag('dungeon').has_sub_tag_name('level info'):
            lvl_info = it.get_single_tag(
                'dungeon').get_single_sub_tag('level info').get_value()
            it_column = lvl_info.split("\n")[0].strip()
        else:
            continue

        skl_exp_it_column = ""
        if skl_exp_it.has_tag('level info'):
            lvl_info = skl_exp_it.get_single_tag_value('level info')
            skl_exp_it_column = lvl_info.split("\n")[0].strip()
        elif skl_exp_it.has_tag('dungeon') and skl_exp_it.get_single_tag('dungeon').has_sub_tag_name('level info'):
            lvl_info = skl_exp_it.get_single_tag(
                'dungeon').get_single_sub_tag('level info').get_value()
            skl_exp_it_column = lvl_info.split("\n")[0].strip()
        else:
            continue

        if it_column != skl_exp_it_column:
            print(it.get_internal_path(), it.get_single_tag_value('name'))
        # if not it.has_tag('level property'):
        #     continue
        # path = os.path.join(skl_exp_pvf_path, lib_pvf.SKL, it.get_internal_path())
        # if not os.path.exists(path):
        #     continue
        # skl_exp_it = lib_item.item(skl_exp_pvf_path, lib_pvf.SKL, os.path.join(
        #     skl_exp_pvf_path, lib_pvf.SKL, it.get_internal_path()), False)
        # if not skl_exp_it.has_tag('level property'):
        #     continue
        # lvl_prop = skl_exp_it.get_single_tag_value('level property')
        # it.get_single_tag('level property').set_value(lvl_prop)
        # it.overwrite()

# sample_ids = ["63500", "64000", "64500"]

# pvf_path = "D:\\workspace\\code\\other\\pvf_1031"
# lst = lib_lst.lst(
#     "D:\\workspace\\code\\other\\pvf_1031\\equipment\\equipment.lst")
# ids = {
#     "artifact_red": [],
#     "artifact_green": [],
#     "artifact_blue": []
# }

# for id in bag_cre_ids:
#     if lst.has_id(id):
#         continue
#     it = lib_item.item(pvf_path, lib_pvf.EQU, os.path.join(
#         pvf_path, lib_pvf.EQU, lst.get_path_by_id(id)), False)
#     if not it.has_tag('name'):
#         continue
#     if it.get_single_tag_value('name').strip("`").strip() == "":
#         continue
#     if not lst.has_id(id):
#         print(id)

# for id, path in lst.get_item_dict().items():
#     # if path.startswith("creature/artifact_"):
#     #     if id in sample_ids:
#     #         continue
#     #     if id not in bag_ids:
#     #         it = lib_item.item(pvf_path, lib_pvf.EQU, os.path.join(
#     #             pvf_path, lib_pvf.EQU, path), False)
#     #         if int(it.get_single_tag_value('rarity')) <= 2:
#     #             print(id, 10000, 1)
#     #         elif int(it.get_single_tag_value('rarity')) == 3:
#     #             print(id, 100, 1)
#     #         elif int(it.get_single_tag_value('rarity')) == 4:
#     #             print(id, 5, 1)
#     #         # if "artifact_red" in path:
#     #         #     ids["artifact_red"].append(id)
#     #         # elif "artifact_green" in path:
#     #         #     ids["artifact_green"].append(id)
#     #         # else:
#     #         #     ids["artifact_blue"].append(id)
#     if path.startswith('creature/') and not path.startswith("creature/artifact_"):
#         if id not in bag_cre_ids:
#             it = lib_item.item(pvf_path, lib_pvf.EQU, os.path.join(
#                 pvf_path, lib_pvf.EQU, lst.get_path_by_id(id)), False)
#             if not it.has_tag('name'):
#                 continue
#             name = it.get_single_tag_value('name')
#             if name.strip("`").strip() == "":
#                 continue
#             if "有期限" in name or "时效性" in name or "宠物胶囊" in name:
#                 continue
#             if not it.has_tag('rarity'):
#                 print(id, 100, 1)
#                 continue
#             rarity = int(it.get_single_tag_value('rarity'))
#             if rarity <= 2:
#                 print(id, 100, 1)
#             if rarity > 2:
#                 print(id, 10, 1)


# fix_creation_rate()

# indep_drop = lib_indep_drop.indep_drop(
#     "D:\\workspace\\code\\other\\pvf_1031\\etc\\independent_drop.etc", "D:\\workspace\\code\\other\\pvf_1031")

# sj_path = "C:\\Users\\donkeywon\\Desktop\\sj"
# my_pvf = "D:\\workspace\\code\\other\\pvf_1031"
# new_path = "C:\\Users\\donkeywon\\Desktop\\merge"
# sj_equ_lst = lib_lst.lst(sj_path + "\\equipment\\equipment.lst")
# sj_stk_lst = lib_lst.lst(sj_path + "\\stackable\\stackable.lst")
# my_equ_lst = lib_lst.lst(my_pvf + "\\equipment\\equipment.lst")
# my_stk_lst = lib_lst.lst(my_pvf + "\\stackable\\stackable.lst")
# id_not_exists = set[str]()
# d = lib_pvf.pvf.read_dir(
#     "C:\\Users\\donkeywon\\Desktop\\sj\\stackable\\cash\\chn_20130129_new_year_package", lib_item.EXT_STK)
# for it in d.values():
#     package_data = it.get_single_tag('package data').get_value().split("\t")
#     for i in range(0, len(package_data), 2):
#         id = package_data[i]
#         if my_equ_lst.has_id(id):
#             continue
#             print("在1031equ里有，id: %s" % id)
#         elif my_stk_lst.has_id(id):
#             continue
#             print("在1031stk里有，id：%s" % id)
#         else:
#             id_not_exists.add(id)
#     package_data_selections = it.get_tag('package data selection')
#     for package_data_selection in package_data_selections:
#         selection = package_data_selection.get_value().split("\t")
#         for i in range(0, len(selection), 2):
#             id = selection[i]
#             if my_equ_lst.has_id(id):
#                 continue
#                 print("在1031equ里有，id: %s" % id)
#             elif my_stk_lst.has_id(id):
#                 continue
#                 print("在1031stk里有，id：%s" % id)
#             else:
#                 id_not_exists.add(id)
# print(id_not_exists)

# pvf = lib_pvf.pvf("D:\\workspace\\code\\other\\pvf_1031\\",
#                   init_type=[lib_pvf.STK], skip_item_not_exists=True)

# stk_lst = lib_lst.lst(
#     "D:\\workspace\\code\\other\\pvf_1031\\stackable\\stackable.lst")
# cashshop = lib_cashshop.cashshop("D:\\workspace\\code\\other\\pvf_1031\\",
#                                  "D:\\workspace\\code\\other\\pvf_1031\\etc\\newcashshop.etc")
# for id, p in cashshop.get_package_dict().items():
#     print(id, p)
# if not stk_lst.has_id(id):
#     print(p)

# new_cashshop = lib_cashshop.cashshop(
#     "", "D:\\download\\1-12期天空套+韩服天空+稀有克隆套（含特效)\\3.商城排列.txt")
# cashshop = lib_cashshop.cashshop(
#     "", "D:\\workspace\\code\\other\\pvf_1031\\etc\\newcashshop.etc")

# d = lib_pvf.pvf.read_dir(
#     "C:\\Users\\donkeywon\\Desktop\\merge\\", lib_item.EXT_STK)
# ids = set[str]()
# for it in d.values():
#     if it.has_tag('package data'):
#         package_data = it.get_single_tag(
#             'package data').get_value().split("\t")
#         for i in range(0, len(package_data), 2):
#             ids.add(package_data[i])
#     if it.has_tag('package data selection'):
#         package_data_selections = it.get_tag('package data selection')
#         for package_data_selection in package_data_selections:
#             selection = package_data_selection.get_value().split("\t")
#             for i in range(0, len(selection), 2):
#                 ids.add(selection[i])
#     if it.has_tag('booster select category'):
#         booster_select_category = it.get_tag('booster select category')
#         for t in booster_select_category:
#             avatar = t.get_sub_tags()[0].get_value().split("\t")
#             for i in range(0, len(avatar), 5):
#                 ids.add(avatar[i])
# for id in ids:
#     print(id)
#     if not my_equ_lst.has_id(id):
#         print("!!!" + id)
# continue
# path = ""
# if sj_equ_lst.has_id(id):
#     print(id + "\t`" + sj_equ_lst.get_value_by_id(id) + "`")
#     path = "equipment/" + sj_equ_lst.get_value_by_id(id)
#     shutil.copyfile(os.path.join(sj_path, path),
#                     os.path.join(my_pvf, path))
# elif sj_stk_lst.has_id(id):
#     path = "stackable/" + sj_stk_lst.get_value_by_id(id)
#     print("!!!!!!!!!" + path)

# for id in ids:
#     print(id + "\t`" + sj_equ_lst.get_value_by_id(id) + "`")
#     path = "equipment/" + sj_equ_lst.get_value_by_id(id)
#     if not os.path.exists(os.path.join(sj_path, path)):
#         print("不存在, %s" % id)
#     shutil.copy(os.path.join(sj_path, path), os.path.join(my_pvf, path))

# my_apd_lst = lib_lst.lst(
#     "D:\\workspace\\code\\other\\pvf_1031\\appendage\\appendage.lst")
# sj_apd_lst = lib_lst.lst(
#     "C:\\Users\\donkeywon\\Desktop\\sj\\appendage\\appendage.lst")
# es_apd_lst = lib_lst.lst(
#     "C:\\Users\\donkeywon\\Desktop\\86\\appendage\\appendage.lst")
# es_path = "C:\\Users\\donkeywon\\Desktop\\86"

def gen_mini_pod():
    pvf_path = "D:\\workspace\\code\\other\\pvf_1031"

    lst = lib_lst.lst(os.path.join(pvf_path, "equipment\\equipment.lst"))

    # dict[job, dict[lvl_range_left, dict[rarity, list[id]]]]
    weapon_jobs_data: dict[str, dict[int, dict[int, list[str]]]] = {}
    cloth_data: dict[str, dict[int, dict[int, list[str]]]] = {}

    # dict[lvl_range_left, dict[rarity, list[id]]]
    jew_data: dict[int, dict[int, list[str]]] = {}
    support_data: dict[int, dict[int, list[str]]] = {}
    magicstone_data: dict[int, dict[int, list[str]]] = {}

    lvl_depth = 3
    raritys = [0, 1, 2, 3]

    d = lib_pvf.pvf.read_dir(
        os.path.join(pvf_path, "equipment\\character"), lib_item.EXT_EQU, pvf_path, lib_pvf.EQU)
    for it in d.values():
        if util.equ_is_avatar(it) or util.equ_is_title(it):
            continue
        if not it.has_tag('rarity') or not it.has_tag('name') or not it.has_tag('minimum level'):
            continue

        lvl = int(it.get_single_tag_value('minimum level'))
        lvl_range_left = lvl - lvl % 10 + 1

        name = it.get_single_tag_value('name')
        if util.equ_need_filter(name):
            continue

        rarity = int(it.get_single_tag_value('rarity'))
        if rarity not in raritys:
            continue

        i_path = it.get_internal_path()
        if not lst.has_path(i_path):
            continue
        id = lst.get_id_by_path(i_path)

        if util.equ_is_weapon(it):
            job = i_path.split("/")[1]
            if not job in weapon_jobs_data:
                weapon_jobs_data[job] = {
                    lvl_range_left: {
                        rarity: []
                    }
                }
            if lvl_range_left not in weapon_jobs_data[job]:
                weapon_jobs_data[job][lvl_range_left] = {
                    rarity: []
                }
            if rarity not in weapon_jobs_data[job][lvl_range_left]:
                weapon_jobs_data[job][lvl_range_left][rarity] = []
            weapon_jobs_data[job][lvl_range_left][rarity].append(id)
        elif util.equ_is_cloth(it):
            typ = i_path.split("/")[3]
            if not typ in cloth_data:
                cloth_data[typ] = {
                    lvl_range_left: {
                        rarity: []
                    }
                }
            if lvl_range_left not in cloth_data[typ]:
                cloth_data[typ][lvl_range_left] = {
                    rarity: []
                }
            if rarity not in cloth_data[typ][lvl_range_left]:
                cloth_data[typ][lvl_range_left][rarity] = []
            cloth_data[typ][lvl_range_left][rarity].append(id)
        elif util.equ_is_jewelry(it):
            if lvl_range_left not in jew_data:
                jew_data[lvl_range_left] = {
                    rarity: []
                }
            if rarity not in jew_data[lvl_range_left]:
                jew_data[lvl_range_left][rarity] = []
            jew_data[lvl_range_left][rarity].append(id)
        elif util.equ_is_support(it):
            if lvl_range_left not in support_data:
                support_data[lvl_range_left] = {
                    rarity: []
                }
            if rarity not in support_data[lvl_range_left]:
                support_data[lvl_range_left][rarity] = []
            support_data[lvl_range_left][rarity].append(id)
        elif util.equ_is_magicstone(it):
            if lvl_range_left not in magicstone_data:
                magicstone_data[lvl_range_left] = {
                    rarity: []
                }
            if rarity not in magicstone_data[lvl_range_left]:
                magicstone_data[lvl_range_left][rarity] = []
            magicstone_data[lvl_range_left][rarity].append(id)

    if len(weapon_jobs_data) > 0:
        for job, data in weapon_jobs_data.items():
            for lvl, rarity_lines in data.items():
                write_mini_pod_data(job + "_", lvl, rarity_lines, lvl_depth)
    if len(cloth_data) > 0:
        for typ, data in cloth_data.items():
            for lvl, rarity_lines in data.items():
                write_mini_pod_data(typ + "_", lvl, rarity_lines, lvl_depth)
    if len(jew_data) > 0:
        for lvl, data in jew_data.items():
            write_mini_pod_data("jew_", lvl, data, lvl_depth)
    if len(support_data) > 0:
        for lvl, data in support_data.items():
            write_mini_pod_data("support_", lvl, data, lvl_depth)
    if len(magicstone_data) > 0:
        for lvl, data in magicstone_data.items():
            write_mini_pod_data("magicstone_", lvl, data, lvl_depth)


def write_mini_pod_data(fn_prefix: str, lvl: int, rarity_data: dict[int, list[str]], lvl_depth: int):
    rarity_prob = gen_mini_pod_rarity_prob(rarity_data, lvl_depth)
    f = open(fn_prefix + str(lvl) + ".txt", mode='w', encoding='utf-8')
    for rarity, ids in rarity_data.items():
        prob = rarity_prob[rarity]
        for id in ids:
            f.write(id + "\t" + str(prob) + "\t1\n")
    f.close()


def gen_mini_pod_rarity_prob(rarity_dict: dict[int, list[str]], lvl_depth: int) -> dict[int, int]:
    raritys = list(rarity_dict.keys())
    raritys.sort(reverse=True)
    # 例如raritys是3 2 1 0
    # lvl_depth设为4，相对概率比例分别是 1 10 100 1000
    # lvl_depth设为3，相对概率比例分别是 1 10 100 100
    # lvl_depth设为2，相对概率比例分别是 1 10 10 10
    # lvl_depth设为1，相对概率比例分别是 1 1 1 1
    # 总分母是10万

    # dict[rarity, relative_prob]
    res: dict[int, int] = {}
    for i in range(0, len(raritys)):
        prob = pow(10, i)
        if i > lvl_depth - 1:
            prob = pow(10, lvl_depth - 1)
        res[raritys[i]] = prob

    total_relative_count = 0
    for rarity in raritys:
        total_relative_count += len(rarity_dict[rarity]) * res[rarity]

    single_relative_prob = math.floor(100000 / total_relative_count)
    for rarity in res:
        res[rarity] *= single_relative_prob

    # dict[rarity, actual_prob]
    return res


d = lib_pvf.pvf.read_dir(
    "C:\\Users\\donkeywon\\Desktop\\tmp", lib_item.EXT_STK)
for it in d.values():
    if not it.has_tag('explain'):
        continue
    price = it.get_single_tag('price')
    explain = it.get_single_tag_value('explain')
    if "Lv1~" in explain:
        price.set_value('100000')
    elif "Lv11~" in explain:
        price.set_value('200000')
    elif "Lv25~" in explain or "Lv20~" in explain:
        price.set_value('300000')
    elif "Lv35~" in explain or "Lv30~" in explain:
        price.set_value('400000')
    elif "Lv45~" in explain or "Lv40~" in explain:
        price.set_value('500000')
    elif "Lv55~" in explain or "Lv50~" in explain:
        price.set_value('600000')
    elif "Lv60~" in explain:
        price.set_value('700000')
    elif "70 ~" in explain or "70级" in explain:
        price.set_value('800000')
    it.overwrite()

# for t in it.get_tag_arr():
#     sub_tags_recurse = t.get_sub_tag_recurse('appendage')
#     if len(sub_tags_recurse) == 0:
#         continue
#     for sub_tag in sub_tags_recurse:
#         apd_id = sub_tag.get_value()
#         if my_apd_lst.has_id(apd_id):
#             continue

#         if sj_apd_lst.has_id(apd_id):
#             internal_path = sj_apd_lst.get_path_by_id(apd_id)
#             print(apd_id, '`' + internal_path + '`')
#             path = os.path.join(new_path, lib_pvf.APD, internal_path)
#             if not os.path.exists('/'.join(path.split("/")[:-1])):
#                 os.makedirs('/'.join(path.split("/")[:-1]))
#             shutil.copy(os.path.join(
#                 sj_path, lib_pvf.APD, internal_path), path)
#         elif es_apd_lst.has_id(apd_id):
#             internal_path = es_apd_lst.get_path_by_id(apd_id)
#             print(apd_id, '`' + internal_path + '`')
#             path = os.path.join(new_path, lib_pvf.APD, internal_path)
#             if not os.path.exists('/'.join(path.split("/")[:-1])):
#                 os.makedirs('/'.join(path.split("/")[:-1]))
#             shutil.copy(os.path.join(
#                 es_path, lib_pvf.APD, internal_path), path)

# my_equ_partset = lib_equ_partset.equ_partset(
#     "D:\\workspace\\code\\other\\pvf_1031\\etc\\equipmentpartset.etc")
# sj_equ_partset = lib_equ_partset.equ_partset(
#     "C:\\Users\\donkeywon\\Desktop\\sj\\etc\\equipmentpartset.etc")

# d = lib_pvf.pvf.read_dir(
#     "D:\\workspace\\code\\other\\pvf_1031\\equipment\\character", lib_item.EXT_EQU, "D:\\workspace\\code\\other\\pvf_1031", lib_pvf.EQU)

# merges = set[lib_tag.tag]()

# for it in d.values():
#     if not it.has_tag('part set index'):
#         continue
#     partset_index = it.get_single_tag('part set index').get_value()
#     if not my_equ_partset.has_id(partset_index):
#         partset_path = sj_equ_partset.get_path_by_id(partset_index)
#         shutil.copy(os.path.join(sj_path, lib_pvf.EQU, partset_path),
#                     os.path.join(my_pvf, lib_pvf.EQU, partset_path))
#         merges.add(sj_equ_partset.get_by_id(partset_index))

# new_f = open("C:\\Users\\donkeywon\\Desktop\\merge.txt",
#              mode="w", encoding="utf-8")
# for t in merges:
#     new_f.write(t.to_string())
#     new_f.write("\n\n")
# new_f.close()

# d = lib_pvf.pvf.read_dir(
#     "C:\\Users\\donkeywon\\Desktop\\sj\\equipment\\character", lib_item.EXT_EQU, "C:\\Users\\donkeywon\\Desktop\\sj", lib_pvf.EQU)
# for it in d.values():
#     if it.has_tag('rarity') and int(it.get_single_tag('rarity').get_value()) == 3 and it.has_tag('minimum level') and int(it.get_single_tag('minimum level').get_value()) >= 75:
#         it.write(os.path.join(new_path, it.get_internal_path()))

# es_obj_lst = lib_lst.lst(
#     "C:\\Users\\donkeywon\\Desktop\\86\\passiveobject\\passiveobject.lst")

# sj_obj_lst = lib_lst.lst(
#     "C:\\Users\\donkeywon\\Desktop\\sj\\passiveobject\\passiveobject.lst")

# ids = ['600811', '911010', '98085', '52550', '48665', '2017122', '48729', '48664', '48705', '960408',
#        '98089', '2017123', '48670', '948117', '48636', '485151', '48730', '481541', '48626', '150851']

# for id in ids:
#     if id in es_obj_lst.get_item_dict():
#         internal_path = es_obj_lst.get_item_dict()[id]
#         src_path = "C:\\Users\\donkeywon\\Desktop\\86\\passiveobject\\" + \
#             '\\'.join(internal_path.split('/')[:-1])
#         new_path = "C:\\Users\\donkeywon\\Desktop\\merge\\passiveobject\\" + \
#             '\\'.join(internal_path.split('/')[:-1])
#         distutils.dir_util.copy_tree(src_path, new_path)
#         print(id, '`' + es_obj_lst.get_item_dict()[id] + '`')
#     elif id in sj_obj_lst.get_item_dict():
#         internal_path = sj_obj_lst.get_item_dict()[id]
#         src_path = "C:\\Users\\donkeywon\\Desktop\\sj\\passiveobject\\" + \
#             '\\'.join(internal_path.split('/')[:-1])
#         new_path = "C:\\Users\\donkeywon\\Desktop\\merge\\passiveobject\\" + \
#             '\\'.join(internal_path.split('/')[:-1])
#         distutils.dir_util.copy_tree(src_path, new_path)
#         print(id, '`' + sj_obj_lst.get_item_dict()[id] + '`')

# d = lib_pvf.pvf.read_dir(
#     "D:\\workspace\\code\\other\\pvf_1031\\equipment\\character", lib_item.EXT_EQU, "D:\\workspace\\code\\other\\pvf_1031", lib_pvf.EQU)
# obj_lst = lib_lst.lst(
#     "D:\\workspace\\code\\other\\pvf_1031\\passiveobject\\passiveobject.lst")
# for it in d.values():
#     for t in it.get_tag_arr():
#         sub_tags_recurse = t.get_sub_tag_recurse('passive object')
#         if len(sub_tags_recurse) == 0:
#             continue
#         for sub_tag in sub_tags_recurse:
#             obj_id = sub_tag.get_value().split('\t')[0]
#             if not obj_lst.has_id(obj_id):
#                 print(obj_id)
