from ner_tools.NER_spacy import ner_spacy
from ner_tools.NER_stanford import ner_stanford
from ner_tools.NER_nltk import ner_nltk
from utils import *
import os


class super_ner():
    def __init__(self, config, take_tools_as_input=True, list_of_tools=None):
        if take_tools_as_input:
            self.input_tools = list_of_tools
        else:
            self.input_tools = config["tools"]

    def initialize_tools(self, lang, config):  # create an object of each tool
        ner_tools = []
        for tool_name in self.input_tools:
            if tool_name == "spacy":
                ner = ner_spacy(lang, config)
            elif tool_name == "nltk":
                ner = ner_nltk(lang, config)
            elif tool_name == "stanford":
                ner = ner_stanford(lang, config)
            if ner.has_model:
                ner_tools.append({"ner_tool_name": tool_name, "ner_tool_object": ner})

        return ner_tools

    def majority_vote_lables(self, votes):
        labels = [vote['label'] for vote in votes]
        # label_types = list(set(labels))
        max = 0
        text = ""
        label_vote = ""
        start_char = ""
        end_char = ""
        max_len = 0

        for type, v in zip(labels, votes):

            c = labels.count(type)

            # if c > 1:
            if c > max:
                max = c
                label_vote = type
                start_char = v['start_char']
                end_char = v['end_char']
                temp_len = end_char - start_char

                if temp_len > max_len:  # take the longest text among texts associated with majority_vote_label
                    max_len = temp_len
                    text = v['text']

        return text, label_vote, start_char, end_char

    def majority_vote(self, votes):

        text, label, start_char, end_char = "", "", "", ""
        mx_count = 0
        mx_len = len(votes[0]['text'])
        vote_mx_len = votes[0]
        vote_mx = ""

        for v1 in range(len(votes) - 1):
            count = 0

            if len(votes[v1]['text']) > mx_len:
                mx_len = len(votes[v1]['text'])
                vote_mx_len = votes[v1]

            for v2 in range(v1 + 1, len(votes), 1):

                if votes[v2]['end_char'] > votes[v1]['end_char']:
                    inter = votes[v1]['end_char'] - votes[v2]['start_char']
                    un = votes[v2]['end_char'] - votes[v1]['start_char']
                else:
                    inter = votes[v2]['end_char'] - votes[v1]['start_char']
                    un = votes[v1]['end_char'] - votes[v2]['start_char']

                iou = float(inter) / float(un)

                if iou > 0.8:
                    count += 1

            if count > mx_count:
                mx_count = count
                vote_mx = votes[v1]

        if vote_mx == "":
            start_char = vote_mx_len['start_char']
            end_char = vote_mx_len['end_char']
            text = vote_mx_len['text']
            label = vote_mx_len['label']
        else:
            start_char = vote_mx['start_char']
            end_char = vote_mx['end_char']
            text = vote_mx['text']
            label = vote_mx['label']

        return text, label, start_char, end_char

    def merge(self, ners_outputs, ner_tools):

        m_len = 1000
        for nertool in ner_tools:
            le = len(ners_outputs[nertool["ner_tool_name"]])
            if le < m_len:
                m_len = le
        if m_len == 0:
            return [], []

        max_end_ind = 0
        min_start_ind = ners_outputs[ner_tools[0]["ner_tool_name"]][0]["start_char"]

        # combine continus annotaitons
        for tool in ner_tools:

            tool = tool["ner_tool_name"]
            ner_outputs = ners_outputs[tool]
            le = len(ner_outputs)
            i = 0
            while i < le - 1:
                i += 1
                annotation = ner_outputs[i]
                prev_annotation = ner_outputs[i - 1]
                a = annotation["end_char"]
                if annotation["end_char"] > max_end_ind:
                    max_end_ind = annotation["end_char"]
                if prev_annotation["start_char"] < min_start_ind:
                    min_start_ind = prev_annotation["start_char"]

                if annotation["start_char"] - prev_annotation["end_char"] == 1:
                    if prev_annotation["label"] == annotation["label"]:
                        annotation["start_char"] = prev_annotation["start_char"]
                        annotation["text"] = prev_annotation["text"] + " " + annotation["text"]
                        ner_outputs.remove(prev_annotation)
                le = len(ner_outputs)
            ners_outputs[tool] = ner_outputs

        # maximum span
        merged_longest_span = []
        ind = min_start_ind

        while ind < max_end_ind:
            # min_start_ind = ind
            max_len_annotaion = 0
            tools_labels_for_ind = []
            merged_annotation_longest_span = {}

            for tool in ner_tools:
                tool = tool["ner_tool_name"]
                ner_outputs = ners_outputs[tool]

                for annotation in ner_outputs:

                    if annotation["start_char"] <= ind < annotation["end_char"]:
                        tools_labels_for_ind.append(
                            annotation["label"])  # one annotation per tool where: start<= ind <end
                        len_annotation = annotation["end_char"] - annotation["start_char"]

                        if max_len_annotaion < len_annotation:
                            max_len_annotaion = len_annotation
                            merged_annotation_longest_span = {"text": annotation["text"], "label": annotation['label'],
                                                              "start_char": annotation["start_char"],
                                                              "end_char": annotation["end_char"]}
                            ind = annotation["end_char"]
                            break

            if merged_annotation_longest_span != {}:
                merged_longest_span.append(merged_annotation_longest_span)
            else:
                # ind = min_start_ind
                ind += 1

        # majority vote

        ind = 0
        merged_majority = []

        while ind < max_end_ind:

            tools_annos_for_ind = []
            main_text, main_label, main_start, main_end = "", "", "", ""
            tools_names = []

            for tool in ner_tools:
                tool = tool["ner_tool_name"]
                ner_outputs = ners_outputs[tool]

                for annotation in ner_outputs:

                    if annotation["start_char"] <= ind < annotation["end_char"]:
                        tools_annos_for_ind.append(annotation)  # one annotation per tool where: start<= ind <end
                        # tools_names.append(tool)

            if len(tools_annos_for_ind) > 1:
                main_text, main_label, main_start, main_end = self.majority_vote(tools_annos_for_ind)

            if main_label != "":

                merged_majority.append(
                    {"text": main_text, "label": main_label, "start_char": main_start, "end_char": main_end})
                ind = main_end
            else:
                ind += 1

        return merged_longest_span, merged_majority

    def annotate(self, input, config, output_name, lang, output_dir, do_merge, max_len=None):

        docs = input.documents
        ner_config = input.config
        languages = input.languages

        if lang not in languages:
            print("Error!! language not supported...")
            return 0


        if not self.tool_output_exists(f'neR_output__{output_name}.json', output_dir):
            print("annotating " + output_name + " ...")

            ner_tools = self.initialize_tools(lang, config)
            n_articles_processed = 0
            event_articles = docs

            for article in event_articles:

                n_articles_processed = n_articles_processed + 1
                article["ner"] = [{} if "ner" not in article.keys() else article["ner"]][0]

                for ner_tool in ner_tools:
                    article["ner"][ner_tool["ner_tool_name"]] = ner_tool["ner_tool_object"].annotate(article["body"][:])
                    print(f'for {n_articles_processed} articles NER {ner_tool["ner_tool_name"]} done!!!')

                if len(ner_tools) > 1 and do_merge == "True":  # merge body only (not title)

                    article["ner"]["merged_longest"], article["ner"]["merged_majority"] = self.merge(article["ner"],
                                                                                                     ner_tools)
                    print(f'for {n_articles_processed} articles NER merge longest and merge majority done!!!')

            self.save_file(f'neR_output__{output_name}', docs, output_dir)
            print(f'ner done for {output_name} !!')

        else:
            print("Annotated file already exists!!")

    def save_file(self, file_name, file, output_dir):
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        with open(f'{output_dir}{file_name}.json', 'w', encoding='utf8') as outfile:
            json.dump(file, outfile, ensure_ascii=False)

    def tool_output_exists(self, fileName, output_dir):
        if not os.path.isdir(output_dir):
            return False
        if fileName in os.listdir(output_dir):
            return True
        else:
            return False
