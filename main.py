from lib.pvf import pvf

# path = "D:/workspace/code/other/pvf_1031/appendage/appendage.lst"
# l = lst(path)
# with open(path, mode="w", encoding="utf-8") as f:
#     f.write(l.to_string())

path = "D:/workspace/code/other/pvf_1031"
pvf = pvf(path)

for typ, lst in pvf.get_type_lst().items():
    print(typ, lst.size())