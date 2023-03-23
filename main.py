import os
import math
import opencc
import shutil
import distutils.dir_util

import lib.pvf as lib_pvf
import lib.item as lib_item
import lib.lst as lib_lst
import lib.tag as lib_tag
import lib.equ_partset as lib_equ_partset
import lib.cashshop as lib_cashshop
import lib.skl as lib_skl


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
    origin_path = "C:\\Users\\donkeywon\\Desktop\\1031.origin"
    d = lib_pvf.pvf.read_dir(
        "D:\\workspace\\code\\other\\pvf_1031\\skill", lib_item.EXT_SKL, "D:\\workspace\\code\\other\\pvf_1031", "skill")
    for it in d.values():
        skl = lib_skl.skl(it)
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
        if origin_it.has_tag('dungeon') and not origin_it.get_single_tag('dungeon').has_sub_tag_name('static data'):
            continue
        if origin_it.has_tag('dungeon'):
            origin_static_data = origin_it.get_single_tag(
                'dungeon').get_single_sub_tag('static data').get_value()
            new_static_data = it.get_single_tag(
                'dungeon').get_single_sub_tag('static data').get_value()
            if origin_static_data != new_static_data:
                print(it.get_internal_path())
                # origin_it.write(os.path.join(
                #     "C:\\Users\\donkeywon\\Desktop\\1031.origin.static", origin_it.get_internal_path()))
        elif origin_it.has_tag('static data') and it.has_tag('static data'):
            origin_static_data = origin_it.get_single_tag(
                'static data').get_value()
            new_static_data = it.get_single_tag(
                'static data').get_value()
            if origin_static_data != new_static_data:
                print(it.get_internal_path())
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


gen_price_and_material()

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

# d = lib_pvf.pvf.read_dir(
#     "D:\\workspace\\code\\other\\pvf_1031\\equipment\\character", lib_item.EXT_EQU, "D:\\workspace\\code\\other\\pvf_1031", lib_pvf.EQU)
# for it in d.values():
#     for t in it.get_tag_arr():
#         sub_tags_recurse = t.get_sub_tag_recurse('appendage')
#         if len(sub_tags_recurse) == 0:
#             continue
#         for sub_tag in sub_tags_recurse:
#             apd_id = sub_tag.get_value()
#             if my_apd_lst.has_id(apd_id):
#                 continue

#             if sj_apd_lst.has_id(apd_id):
#                 internal_path = sj_apd_lst.get_path_by_id(apd_id)
#                 print(apd_id, '`' + internal_path + '`')
#                 path = os.path.join(new_path, lib_pvf.APD, internal_path)
#                 if not os.path.exists('/'.join(path.split("/")[:-1])):
#                     os.makedirs('/'.join(path.split("/")[:-1]))
#                 shutil.copy(os.path.join(
#                     sj_path, lib_pvf.APD, internal_path), path)
#             elif es_apd_lst.has_id(apd_id):
#                 internal_path = es_apd_lst.get_path_by_id(apd_id)
#                 print(apd_id, '`' + internal_path + '`')
#                 path = os.path.join(new_path, lib_pvf.APD, internal_path)
#                 if not os.path.exists('/'.join(path.split("/")[:-1])):
#                     os.makedirs('/'.join(path.split("/")[:-1]))
#                 shutil.copy(os.path.join(
#                     es_path, lib_pvf.APD, internal_path), path)

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
