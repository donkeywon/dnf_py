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


# path = "D:\\workspace\\code\\other\\pvf_1031_s\\"
# # path = "C:\\Users\\donkeywon\\Desktop\\86\\"

# d = pvf.read_dir(os.path.join(
#     path, "equipment\\character\\thief\\weapon"), lib_item.EXT_EQU, True)

# for fpath, i in d.items():
#     if 'avatar\\' in i.get_filepath() or \
#         '\\etc\\' in i.get_filepath() or \
#         '\\title\\' in i.get_filepath() or \
#             'pvp' in i.get_filepath() or \
#         '(舊)' in i.get_tag('name')[0].get_value() or \
#             '(旧)' in i.get_tag('name')[0].get_value():
#         continue

#     if not i.has_tag('grade'):
#         continue

#     grade = int(i.get_tag('grade')[0].get_value())
#     new_path = os.path.join("C:\\Users\\donkeywon\\Desktop\\pvf_1031_s\\", "new", i.get_tag(
#         'rarity')[0].get_value(), fpath.removeprefix(path))
#     dir = os.path.split(new_path)[0]
#     if not os.path.exists(dir):
#         os.makedirs(dir)
#     i.write(new_path)


sj_path = "C:\\Users\\donkeywon\\Desktop\\sj"
my_pvf = "D:\\workspace\\code\\other\\pvf_1031"
new_path = "C:\\Users\\donkeywon\\Desktop\\merge"
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

# l = lib_lst.lst(
#     "D:\\workspace\\code\\other\\pvf_1031\\passiveobject\\passiveobject.lst")
# l.overwrite()

# pvf = lib_pvf.pvf("D:\\workspace\\code\\other\\pvf_1031\\",
#                   init_type=[lib_pvf.STK], skip_item_not_exists=True)


# equ_ps = lib_equ_partset.equ_partset(
#     "D:\\workspace\\code\\other\\pvf_1031\\etc\\equipmentpartset.etc")
# equ_ps.overwrite()


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


# it = lib_item.item(
#     "", "D:\\workspace\\code\\other\\pvf_1031\\stackable\\cash\\2019springfestival\\90121195.stk")
# tags = it.get_tag('booster select category')
# ids = set[str]()
# for t in tags:
#     avatar = t.get_sub_tags()[0].get_value().split("\t")
#     for i in range(0, len(avatar), 5):
#         ids.add(avatar[i])

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
                it.add_tag(lib_tag.tag('avatar type select', tag_value, True))
            else:
                it.get_single_tag('avatar type select').set_value(tag_value)
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


# d = lib_pvf.pvf.read_dir(
#     "D:\\workspace\\code\\other\\pvf_1031\\equipment\\character", lib_item.EXT_EQU, "D:\\workspace\\code\\other\\pvf_1031", lib_pvf.EQU)
# equ_lst = lib_lst.lst(
#     "D:\\workspace\\code\\other\\pvf_1031\\equipment\\equipment.lst")
# id_rare_list: list[str] = []
# id_normal_list: list[str] = []

# for it in d.values():
#     if 'avatar/' not in it.get_internal_path() or 'weapon/' in it.get_internal_path():
#         continue
#     if it.get_single_tag('name').get_value() == '``':
#         continue
#     if not equ_lst.has_path(it.get_internal_path()):
#         continue
#     name = it.get_single_tag('name').get_value()
#     tag_value = ''
#     if it.has_tag('grade') and it.get_single_tag('grade').get_value() == '3':
#         id_rare_list.append(equ_lst.get_id_by_path(it.get_internal_path()))
#         tag_value = '''7	0	0	100	0
# 	30	0	0	300	0
# 	0	0	0	1000	0'''
#     else:
#         id_normal_list.append(equ_lst.get_id_by_path(it.get_internal_path()))
#         tag_value = '''7	0	0	50	0
# 	30	0	0	150	0
# 	0	0	0	500	0'''
#     if not it.has_tag('avatar type select'):
#         it.add_tag(lib_tag.tag('avatar type select', tag_value, True))
#     else:
#         it.get_single_tag('avatar type select').set_value(tag_value)
#     it.overwrite()

# f = open('avatar.txt', mode='w', encoding='utf-8')
# idx = 1000000
# for id in id_normal_list:
#     f.write(str(idx) + "\t" + id + "\t3\t0\t0\t-1\t-1\t" + id + "\t4\t0\t0\t-1\n")
#     idx += 1
# for id in id_rare_list:
#     f.write(str(idx) + "\t" + id + "\t3\t0\t0\t-1\t-1\t" + id + "\t4\t0\t0\t-1\n")
#     idx += 1
# f.close()
