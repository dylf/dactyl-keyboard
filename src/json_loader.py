import json
import os


def load_json(filepath, merge_into=None, save_path='../things'):
    if merge_into is None:
        merge_into = {}
    with open(filepath, mode='r') as fid:
        new_data = json.load(fid)
    # for key in new_data:
    #     merge_into[key] = new_data[key]
    for key in new_data:
        value = str(new_data[key])
        if value.startswith("file:"):
            new_file_path = os.path.join(".", "src", "json", value[5:])
            print("Loading child json file: ", new_file_path)
            merge_into = load_json(new_file_path, merge_into, save_path)
        merge_into[key] = new_data[key]
        # elif value.startswith("override:"):
        #     name = value[9:]
        #     new_file_path = os.path.join(save_path, name, name + ".json")
        # if new_file_path is not None:
        #     print("Loading child json file: ", new_file_path)
        #     merge_into = load_json(new_file_path, merge_into, save_path)

    return merge_into



