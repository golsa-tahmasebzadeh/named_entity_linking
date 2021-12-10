from nel_tools.NEL_wikifier import wikifier
from nel_tools.NEL_agdistis import agdistis
from utils import *
import os
import copy



class super_nel():

    def __init__(self, config,  take_tools_as_input=True, list_of_tools = None):
        if take_tools_as_input:
            self.input_tools = list_of_tools
        else:
            self.input_tools = config["tools"]


    def initialize_tools(self, lang, config):
        nel_tools = []
        nel = agdistis(lang, config)
        for tool_name in self.input_tools:
            if tool_name == "wikifier":
                nel = wikifier()
            elif tool_name == "agdistis":
                nel = agdistis(lang, config)

            nel_tools.append({"nel_tool_name": tool_name, "nel_tool_object": nel})
        return nel_tools



    def majority_vote(self, votes):
        max = 0
        uri_vote, page_rank, start_char, end_char, main_text = None, None, None, None, None
        tools = [vote['tool'] for vote in votes]
        votes_uris = [vote['uri'] for vote in votes]
        set_of_tools = list(set(tools))
        le = len(set_of_tools)

        if le > 1:  # there is at least one different tool name
            if len(votes) == 2:

                if votes[0]['tool'] != votes[1]['tool']:
                    uri_vote = votes[0]['uri']
                    page_rank = votes[0]['page_rank']
                    start_char = votes[0]['start_char']
                    end_char = votes[0]['end_char']
                    main_text = votes[0]['text']

                    if votes[1]['page_rank']!= None:

                        if votes[1]['page_rank'] > page_rank:
                            uri_vote = votes[1]['uri']
                            page_rank = votes[1]['page_rank']
                            start_char = votes[1]['start_char']
                            end_char = votes[1]['end_char']
                            main_text = votes[1]['text']

            elif len(votes) > 2:
                max_len = 0
                for vote in votes:
                    c = votes_uris.count(vote['uri'])
                    p_rank = None

                    for v in votes:
                        if v['uri'] == vote['uri']:
                            if v['page_rank']!= None:
                                p_rank = vote['page_rank']
                                break

                    if c > max:
                        max = c
                        uri_vote = vote['uri']
                        page_rank = p_rank
                        start_char = vote['start_char']
                        end_char = vote['end_char']

                        if len(vote['text']) > max_len:
                            max_len = len(vote['text'])
                            main_text = vote['text']

        return uri_vote, page_rank, start_char, end_char, main_text



    def merge(self, nels_outputs_orig, nel_tools, len_article):

        nels_outputs0 = copy.deepcopy(nels_outputs_orig)
        max_end_ind = len_article - 1
        ind = 0
        merged = []

        while ind < max_end_ind:
            min_len_annotaion = max_end_ind
            max_len_annotaion = 0
            main_uris = []
            exists = False
            main_text, main_end_max, main_end_min, new_ind, main_start = None, None, None, None, None

            for tool in nel_tools:
                tool = tool["nel_tool_name"]
                nels_outputs = nels_outputs0[tool]

                ners = list(nels_outputs.keys())

                for ner in ners:

                    for annotation in nels_outputs[ner]:

                        if annotation["start_char"] <= ind < annotation["end_char"]:

                            len_annotation = annotation["end_char"] - annotation["start_char"]

                            if annotation['uri'] not in main_uris:
                                 annotation['tool'] = ner + "_" + tool
                                 main_uris.append(annotation)
                                 nels_outputs[ner].remove(annotation)

                            if min_len_annotaion > len_annotation:  # take smallest span among all annotations

                                min_len_annotaion = len_annotation
                                # main_start = annotation['start_char']
                                main_end_min = annotation['end_char']
                                # main_end_max = main_end_min
                                main_text = annotation['text']
                                exists = True
                                new_ind = main_end_min


            if exists:
                main_uri, main_page_rank, main_start, main_end,main_text = self.majority_vote(main_uris)
                ind = new_ind
                if main_uri!=None:
                    merged_annotation = {
                                             "uri": main_uri, "text": main_text, "page_rank": main_page_rank,
                                              "start_char": main_start,
                                             "end_char": main_end
                                         }
                    merged.append(merged_annotation)

            else:
                ind += 1

        return merged



    def annotate(self, input, config, output_name, lang, output_dir):

            docs = input.documents
            nel_config = input.config
            languages = input.languages

            if lang not in languages:
                print("Error!! language not supported...")
                return 0

            if not self.tool_output_exists( f'neL_output__{output_name}.json', output_dir):

                print("annotating "+output_name +" ...")

                nel_tools = self.initialize_tools(lang, config)

                n_articles_processed = 0

                event_articles = docs
                for article in event_articles:

                        n_articles_processed = n_articles_processed + 1
                        article["nel"] = [{} if "nel" not in article.keys() else article["ner"]][0]

                        for nel_tool in nel_tools:

                            article["nel"][nel_tool["nel_tool_name"]] = [{} if nel_tool["nel_tool_name"] not in article["nel"].keys() else article["ner"]][0]

                            if lang in nel_config[nel_tool["nel_tool_name"]]["lang"]:

                                    ners = [list(article["ner"].keys())[0]]

                                    for ner in ners:

                                        ner_outputs = article["ner"][ner]


                                        if nel_tool["nel_tool_name"] == "agdistis":
                                            article["nel"][nel_tool["nel_tool_name"]][ner] = nel_tool["nel_tool_object"].annotate(ner_outputs)
                                            print(f'for article {n_articles_processed} {nel_tool["nel_tool_name"]} - {ner} done!!!')
                                        else:
                                            article["nel"][nel_tool["nel_tool_name"]][ner] = nel_tool["nel_tool_object"].annotate(ner_outputs, article["body"], lang, config)


                                    print(f'******* for {n_articles_processed}  articles,  {nel_tool["nel_tool_name"]} done!!!')

                self.save_file(f'neL_output__{output_name}', output_dir, docs)
                print("nel done!!")

            else:
                print("Annotated file already exists!!")



    def tool_output_exists(self, fileName, output_dir):
        ls = os.listdir(output_dir)
        if fileName in ls:
            return True
        else:
            return False


    def save_file(self, fileName, output_dir, file):
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        with open(f'{output_dir}/{fileName}.json', 'w', encoding="utf8") as outfile:
            json.dump(file, outfile, ensure_ascii=False)


