import json


def convert_tag( tag_in, cfg):
    converted_tag = tag_in
    tag_map = cfg['tag_map']
    tag = [tm for tm in tag_map if tag_in in tag_map[tm]]
    if tag != []:
        converted_tag = tag[0]

    return converted_tag


def save_file(fileName, file):
    with open(fileName, 'w') as outfile:
        json.dump(file, outfile)


def open_json(fileName):
    try:
        with open(fileName,encoding='utf8') as json_data:
            d = json.load(json_data)
    except Exception as s:
        d=s
        print(d)
    return d