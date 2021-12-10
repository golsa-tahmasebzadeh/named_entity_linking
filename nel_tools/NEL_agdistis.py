import requests
import copy

# https://github.com/dice-group/AGDISTIS/wiki/2-Asking-the-webservice
class agdistis(object):


    def __init__(self, lang,config):
        # self.agdistis_api = "http://akswnc9.informatik.uni-leipzig.de:8113/AGDISTIS"
        self.agdistis_api = config['agdistis']['api_url'][lang]
        self.default_agdistis_params = {
                    'text': '<entity>Leipzig</entity> is the capital of the world!',
                    'type': 'agdistis'
                    }

    def disambiguate(self, text):

        """
            Input: text (any arbitrary string with annotated entities -- <entity>Austria</entity>)
            Output: entities as a list [{'start': 0, 'offset': 7, 'disambiguatedURL': 'http://dbpedia.org/resource/Austria', 'namedEntity': 'Austria'}]
        """
        payload = copy.copy(self.default_agdistis_params)
        # for entity in text:
        payload['text'] = text
        r = requests.post(self.agdistis_api, data=payload)
        try:
            entities = r.json()
        except ValueError as e:
            #server failed
            entities = [{'start': 0, 'offset': 0, 'disambiguatedURL': '', 'namedEntity': ''}]
        return entities


    def annotate(self, text):
        """
            Support method to wrap entity into <entity/> tag
        """
        annotations = []
        for t in text: # text is output of a NER tool
            if t["label"]!="O":
                entity = t["text"]
                output = self.disambiguate("<entity>%s</entity>"%(entity))
                output[0]["start_char"] = t["start_char"]
                output[0]["end_char"] = t["end_char"]
                output[0]['tag'] = t['label']
                annotations.append(output)
        annos_out = self.wrapper(annotations)
        return annos_out

    def wrapper(self, named_links_in):

        annotations_of_tool = []

        for nl in named_links_in:
                url = nl[0]['disambiguatedURL']
                if url[0:26]!="http://aksw.org/notInWiki/":
                    text = nl[0]['namedEntity']
                    if url[:29] == "http://en.wikipedia.org/wiki/":  # convert wikipedia to dbpedia
                        url = "http://dbpedia.org/resource/" + url[29:]

                    dicAnnotations = {'uri': url, 'text': text, 'page_rank': None, 'start_char': nl[0]['start_char'], 'end_char': nl[0]['end_char'], 'tag':nl[0]['tag']}
                    annotations_of_tool.append(dicAnnotations)

        return annotations_of_tool



if __name__ == "__main__":
    agdistiss = agdistis("eng")
    entities = agdistiss.disambiguate('<entity>August 2012</entity>')
    entities = agdistiss.annotate("Trump was in Austria in 2018.", "eng")
    print(entities)



