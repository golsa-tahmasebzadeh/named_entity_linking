from utils import open_json
from nel_super_class import super_nel
from ner_super_class import super_ner
import argparse
import re
import glob
import os

class input_init:
    def __init__(self, config, documents, languages):
        self.config = config
        self.documents = documents
        self.languages = languages



def pre_process( docs):

        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~''';
        events = docs.keys()
        for event in events:
            event_articles = docs[event]

            for article in event_articles:

                for x in article["body"].lower():

                    if x in punctuations:
                        article["body"] = article["body"].replace(x, "");

                    article["body"] = re.sub(' +', ' ', article["body"])

        return docs


def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--config', '-cp', help='config file path')
    parser.add_argument('--task', '-t', help="ner or nel")
    args = parser.parse_args()
    return args



def main():

    input_config = open_json('configs/input_config')
    input_lang = input_config['language']
    # config_of_task = open_json(input_config['config_path'])
    task = input_config['task']
    config_of_task = open_json(f"configs/{task}_config")
    do_merge = input_config['do_merge_ner']
    max_len_body_ner = 500

    neR_input_docs = glob.glob(f"{input_config['docs_dir'][input_lang]}*.json")
    neL_input_docs = glob.glob(f"{input_config['ner_dir_out'][input_lang]}*.json")

    neR_input_docs_names = [os.path.split(inpt)[1].split('.')[0] for inpt in neR_input_docs]
    neL_input_docs_names = [os.path.split(inpt)[1].split('.')[0] for inpt in neL_input_docs]

    ner = super_ner(config_of_task, take_tools_as_input=True, list_of_tools=input_config['ner_selected_tools'])
    nel = super_nel(config_of_task, take_tools_as_input=True, list_of_tools=input_config['nel_selected_tools'])

    if task == "NER":

        for doc, file_name in zip(neR_input_docs, neR_input_docs_names):
                input_obj = input_init(config_of_task, open_json(doc), open_json('configs/NER_config')['languages'])
                ner.annotate(input_obj, config_of_task,  output_name=file_name, lang=input_lang, output_dir = input_config['ner_dir_out'][input_lang], do_merge=do_merge, max_len=max_len_body_ner)

    if task == "NEL":

        for doc, file_name in zip(neL_input_docs, neL_input_docs_names):
                input_obj = input_init(config_of_task, open_json(doc), open_json('configs/NEL_config')['languages'])
                nel.annotate(input_obj, config_of_task, output_name=file_name, lang=input_lang, output_dir=input_config['nel_dir_out'][input_lang])


if __name__ == '__main__':
        main()



