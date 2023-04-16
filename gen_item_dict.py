import os

import lib.pvf
import lib.item
import lib.lst
import lib.indep_drop
import lib.util


weapon_code_map = {
    "swordman": {
        "beamsword": "10106",
        "club":      "10104",
        "hsword":    "10105",
        "katana":    "10103",
        "ssword":    "10102",
    },
    "fighter": {
        "boxglove": "10205",
        "claw":     "10204",
        "gauntlet": "10203",
        "knuckle":  "10202",
        "tonfa":    "10206",
    },
    "gunner": {
        "automatic": "10303",
        "bowgun":    "10306",
        "hcannon":   "10305",
        "musket":    "10304",
        "revolver":  "10302",
    },
    "mage": {
        "broom": "10406",
        "pole":  "10403",
        "rod":   "10404",
        "spear": "10402",
        "staff": "10405",
    },
    "priest": {
        "axe":    "10506",
        "cross":  "10502",
        "rosary": "10503",
        "scythe": "10505",
        "totem":  "10504",
    },
    "thief": {
        "dagger":    "10602",
        "twinsword": "10603",
        "wand":      "10604",
    },
}
cloth_code_map = {
    "cloth": {
        "jacket":   "11002",
        "shoulder": "11003",
        "pants":    "11004",
        "shoes":    "11005",
        "belt":     "11006",
    },
    "leather": {
        "jacket":   "11101",
        "shoulder": "11102",
        "pants":    "11103",
        "shoes":    "11104",
        "belt":     "11105",
    },
    "larmor": {
        "jacket":   "11201",
        "shoulder": "11202",
        "pants":    "11203",
        "shoes":    "11204",
        "belt":     "11205",
    },
    "harmor": {
        "jacket":   "11301",
        "shoulder": "11302",
        "pants":    "11303",
        "shoes":    "11304",
        "belt":     "11305",
    },
    "plate": {
        "jacket":   "11401",
        "shoulder": "11402",
        "pants":    "11403",
        "shoes":    "11404",
        "belt":     "11405",
    },
}
jewelry_code_map = {
    "amulet": "12001",
    "ring":   "12002",
    "wrist":  "12003",
}
spec_code_map = {
    "support": {
        "all":              "32001",
        "swordman":         "32002",
        "demonic swordman": "32003",
        "fighter":          "32004",
        "at fighter":       "32012",
        "gunner":           "32005",
        "at gunner":        "32010",
        "mage":             "32006",
        "creator mage":     "32007",
        "at mage":          "32008",
        "priest":           "32009",
        "thief":            "32011",
    },
    "magicstone": {
        "all":              "32100",
        "swordman":         "32101",
        "demonic swordman": "32102",
        "fighter":          "32103",
        "at fighter":       "32111",
        "gunner":           "32104",
        "at gunner":        "32109",
        "mage":             "32105",
        "creator mage":     "32107",
        "at mage":          "32106",
        "priest":           "32108",
        "thief":            "32110",
    },
}


def usable_jobs(it: lib.item.item) -> list[str]:
    jobs_str = it.get_single_tag_value_or_default('usable job', "")
    if jobs_str == "":
        return []
    jobs = jobs_str.strip().split("\n")
    return list(map(lambda x: x.strip().strip("`[]"), jobs))


def gen_equ_code(it: lib.item.item) -> str:
    path_s = it.get_internal_path().split("/")
    if path_s[1] == "common":
        if path_s[2] == "magicstone" or path_s[2] == "support":
            jobs = usable_jobs(it)
            job = "all"
            if len(jobs) > 0:
                job = jobs[0]
            return spec_code_map[path_s[2]][job]
        elif path_s[2] == "ring" or path_s[2] == "amulet" or path_s[2] == "wrist":
            return jewelry_code_map[path_s[2]]
        else:
            return cloth_code_map[path_s[3]][path_s[2]]
    else:
        return weapon_code_map[path_s[1]][path_s[3]]


def convert_rarity(it: lib.item.item) -> str:
    rarity = it.get_single_tag_value('rarity')
    if rarity == "0" or rarity == "1":
        return rarity

    name = it.get_single_tag_value('name').strip("`")
    if rarity == "2":
        if name.startswith("传承") or name.startswith("傳承"):
            return "3"
        else:
            return "2"

    item_category = it.get_single_tag_value_or_default("item category", "")
    if rarity == "3":
        if item_category == "`boss drop`":
            return "6"
        else:
            return "5"
    if rarity == "4":
        return "7"
    if rarity == "5":
        return "4"
    return ""


pvf_dir = "D:\\workspace\\code\\other\\pvf_1031"
equ_lst = lib.lst.lst(os.path.join(pvf_dir, "equipment\\equipment.lst"))
indep_drop = lib.indep_drop.indep_drop(os.path.join(
    pvf_dir, "etc\\independent_drop.etc"), pvf_dir)

out_f = open("item_dict.txt", mode="w", encoding="utf-8")

d = lib.pvf.pvf.read_dir(
    os.path.join(pvf_dir, "equipment\\character"), lib.item.EXT_EQU, pvf_dir, lib.pvf.EQU, filter_dir=["avatar"])
for it in d.values():
    path = it.get_internal_path()
    path_s = path.strip().split("/")
    if path_s[1] != "common":
        if path_s[1] not in ["fighter", "gunner", "mage", "priest", "swordman", "thief"]:
            continue
        else:
            if path_s[2] != "weapon":
                continue
    else:
        if path_s[2] not in ["amulet", "belt", "jacket", "magicstone", "pants", "ring", "shoes", "shoulder", "support", "wrist"]:
            continue

    if not equ_lst.has_path(path):
        continue

    item_id = equ_lst.get_id_by_path(path)
    code = gen_equ_code(it)

    in_dep_drop = 0
    in_hell = 1
    if indep_drop.has_item(int(item_id)):
        in_dep_drop = 1
        in_hell = 0

    rarity = convert_rarity(it)
    if rarity == "":
        continue
    if rarity == "6":
        in_hell = 0

    grade = it.get_single_tag_value_or_default("grade", "")
    lvl = it.get_single_tag_value_or_default("minimum level", "")
    if grade == "" and lvl == "":
        continue
    if grade == "":
        grade = lvl
    elif lvl == "":
        lvl = grade

    name = it.get_single_tag_value_or_default("name", "")
    if name == "":
        continue

    if lib.util.equ_need_filter(name):
        continue

    out_f.write(item_id + "\t")
    out_f.write(rarity + "\t")
    out_f.write(lvl + "\t")
    out_f.write(grade + "\t")
    out_f.write(code + "\t")
    out_f.write(str(in_hell) + "\t")
    out_f.write(str(in_dep_drop) + "\t")
    out_f.write("0\t0\t0\t0\t0\t")
    out_f.write(name + "\n")

out_f.close()
