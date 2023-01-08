import os
import math
import opencc

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

# d = pvf.read_dir(
#     "D:\\workspace\\code\\other\\pvf_1031\\equipment\\character", lib_item.EXT_EQU)
# for i in d.values():
#     if 'avatar' not in i.get_filepath():
#         continue
#     if i.has_tag('set item master'):
#         print(i.get_filepath())

# l = lib_lst.lst(
#     "D:\\workspace\\code\\other\\pvf_1031\\equipment\\equipment.lst")
# l.overwrite()

# pvf = lib_pvf.pvf("D:\\workspace\\code\\other\\pvf_1031\\",
#                   init_type=[lib_pvf.STK], skip_item_not_exists=True)


# equ_ps = lib_equ_partset.equ_partset(
#     "D:\\workspace\\code\\other\\pvf_1031\\etc\\equipmentpartset.etc")
# equ_ps.overwrite()

stk_lst = lib_lst.lst(
    "D:\\workspace\\code\\other\\pvf_1031\\stackable\\stackable.lst")
cashshop = lib_cashshop.cashshop("D:\\workspace\\code\\other\\pvf_1031\\",
                                 "D:\\workspace\\code\\other\\pvf_1031\\etc\\newcashshop.etc")
for id, p in cashshop.get_package_dict().items():
    if not stk_lst.has_id(id):
        print(p)
