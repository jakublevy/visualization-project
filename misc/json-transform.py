import json

def main():
    transform_json('../data/poem-kanji.json')
    transform_json('../data/poem-words.json')
    transform_json('../data/poem-morae.json')
    # transform_json_morae('poem-morae.json')

def transform_json(path):
    out_dic = {}
    with open(path) as f:
        dic = json.load(f)
    for k in dic:
        value_dic = dic[k]
        name = value_dic['name']
        del value_dic['name']
        out_dic[name] = value_dic
    
    with open(path, 'w') as f:
        json.dump(out_dic, f, ensure_ascii=False)

# def transform_json_morae(path):
#     out_dic = {}
#     with open(path) as f:
#         dic = json.load(f)
#     for k in dic:
#         value_dic = dic[k]
#         name = value_dic['name']
#         out_dic[name] = value_dic['morae']
    
#     with open(path, 'w') as f:
#         json.dump(out_dic, f, ensure_ascii=False)

if __name__ == "__main__":
    main()