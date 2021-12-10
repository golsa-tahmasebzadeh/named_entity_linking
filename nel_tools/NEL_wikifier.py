import requests
import json

class wikifier():
    def __init__(self):
        pass

    def annotate(self, ner_outputs, text, language, config):

        langin = config['wikifier']['lang'][language]
        params_in = config['wikifier']['params']
        user_key = config['wikifier']['user_key']
        API_ENDPOINT = config['wikifier']['api_url']

        self.params = {
            'userKey': user_key,
            "text": text,
            "lang": langin,
            "secondaryAnnotLanguage": langin,
            "extraVocabularies": params_in['extraVocabularies'],
            "wikiDataClasses": params_in['wikiDataClasses'],
            "wikiDataClassIds": params_in['wikiDataClassIds'],
            "support": params_in['support'],
            "ranges": params_in['ranges'],
            "includeCosines": params_in['includeCosines'],
            "maxMentionEntropy": params_in['maxMentionEntropy'],
            "maxTargetsPerMention": params_in['maxTargetsPerMention'],
            "minLinkFrequency": params_in['minLinkFrequency'],
            "pageRankSqThreshold": params_in['pageRankSqThreshold'],
            "applyPageRankSqThreshold": params_in['applyPageRankSqThreshold'],
            "partsOfSpeech": params_in['partsOfSpeech'],
            "verbs": params_in['verbs'],
            "nTopDfValuesToIgnore": params_in['nTopDfValuesToIgnore']
        }

        out0 = requests.get(API_ENDPOINT, params=self.params)
        out = json.loads(out0.text)
        # out["text"] = text
        out_put = self.wrapper(text, out, ner_outputs)
        return out_put




    def wrapper(self,doc, named_links_in, ner_outputs):

        annotations = []
        # doc = named_links_in["text"]

        for ner in ner_outputs:
            temp = []

            for nl in named_links_in['annotations']:

                url = nl['url']
                if url[:29] == "http://en.wikipedia.org/wiki/":  # convert wikipedia to dbpedia
                    url = "http://dbpedia.org/resource/" + url[29:]

                for s in nl['support']:
                    text = doc[s['chFrom']:s['chTo']+1]
                    dic_annotation = {'uri': url, 'text': text, 'page_rank': s['pageRank'], 'start_char': s['chFrom'], 'end_char': s['chTo']+1}

                    if ner['start_char'] - 2 <= dic_annotation['start_char'] <= ner['end_char'] + 2:
                        if ner['start_char'] - 2 <= dic_annotation['end_char'] <= ner['end_char'] + 2:
                            temp.append(dic_annotation)
            bpr = 0
            if len(temp) > 0:
                annotation_main = temp[0]
                for t in temp:
                    if t['page_rank'] > bpr:
                        bpr = t['page_rank']
                        annotation_main = t
                annotations.append(annotation_main)

        return annotations


  





