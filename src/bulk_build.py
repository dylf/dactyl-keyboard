import os
import json
import sys
import dactyl_manuform

json_template = """
{
  "ENGINE": "cadquery",
  "overrides": "",
  "override_name": "",
  "save_dir": "",
  "save_name": null,
  "show_caps": false,
  "nrows": 4,
  "ncols": 6,
  "inner_column": true,
  "plate_style": "NOTCH",
  "full_last_rows": true,
  "all_last_rows": false,
  "right_side_only": true,
  "thumb_style": "DEFAULT",
  "other_thumb": "DEFAULT",
  "ball_side": "right"
}
"""

clusters = [
    "DEFAULT", "CARBONFET", "MINI", "MINITHICC", "MINITHICC3", "MINIDOX",
    "TRACKBALL_WYLD", "TRACKBALL_THREE", "TRACKBALL_ORBYL"
]

gen_dir = sys.argv[1]

try:
    print(gen_dir)
except NameError:
    print("Must provide target directory for generating bulk models")
    sys.exit(-1)

out_file = os.path.join(gen_dir, "bulk_config")

engine = "cadquery"
default = "DEFAULT"
trackball = "TRACKBALL_WILD"
hotswap = "HS_NOTCH"
normal = "NOTCH"
run_config = os.path.join(r"src", 'run_config.json')


def write_file(file_path, data):
    if os.path.exists(file_path):
        os.remove(file_path)
    f = open(file_path, "a")
    f.write(json.dumps(data, indent=2))
    f.close()


def set_overrides(override):
    with open(run_config, mode='r') as fid:
        data = json.load(fid)
    previous_overrides = data["overrides"]
    data["overrides"] = override
    write_file(run_config, data)
    return previous_overrides


previous_overrides = set_overrides(out_file)

def finished():
    set_overrides(previous_overrides)
    sys.exit(0)


override_list = [
    {
        "name": "special",
        "iterate": [{"ncols": col, "nrows": row} for col in [6] for row in [4, 5, 6]]
    },
    # {
    #     "name": "clusters",
    #     "iterate": [{"thumb_style": c} for c in clusters]
    # },
    # {
    #     "name": "special",
    #     "iterate": [{"switch_file": f"file:switch_holes\\{style}.json"} for style in ["notch"]]
    # },
    # {
    #     "name": "row_options",
    #     "iterate": [{"ncols": col, "nrows": row, "full_last_rows": full} for col in [6, 7] for row in [5, 6] for full in [False, True]]
    # },
]

def write_config(top_dir, overrides):
    config = json.loads(json_template)
    for key in overrides:
        config[key] = overrides[key]
    rows = config["nrows"]
    cols = config["ncols"]
    plate = config["plate_style"]
    thumb = config["thumb_style"]
    row_name = "standard"
    if config["full_last_rows"]:
        row_name = "full"
    if config["all_last_rows"]:
        row_name = "all"
    name = str(rows) + "x" + str(cols) + "_" + plate + "_" + thumb + "_rows_" + row_name
    config["save_dir"] = os.path.join(gen_dir, top_dir)
    config["overrides"] = out_file
    config["save_name"] = name
    write_file(out_file + '.json', config)

# def write_config(rows, cols, engine, thumb1, plate, last_rows):
#     config = json.loads(json_template)
#     name = str(rows) + "_x_" + str(cols) + "_" + plate  + "_" + last_rows  + "_" + thumb1
#     config["save_dir"] = os.path.join(gen_dir, str(rows) + "_x_" + str(cols), plate, last_rows)
#     print("Generating: ", name)
#     config["overrides"] = out_file
#     config["save_name"] = name
#     config["override_name"] = thumb1
#     config["engine"] = engine
#     config["nrows"] = rows
#     config["ncols"] = cols
#     config["plate_style"] = "NUB" if plate == "normal" else "HS_NUB"
#     config["thumb_style"] = thumb1
#     config["other_thumb"] = thumb1
#     config["full_last_rows"] = True if last_rows == "full" else False
#     config["ball_side"] = "both"
#
#     write_file(out_file + '.json', config)


for v in override_list:
    name = v["name"]
    it = v["iterate"]
    for config in it:
        write_config(name, config)
        dactyl_manuform.make_dactyl()


finished()


