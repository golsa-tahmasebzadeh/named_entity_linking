import spacy
from utils import convert_tag
# python -m spacy download 'fr_core_news_sm', 'it_core_news_sm' ,..
# https://spacy.io/api/annotation
class ner_spacy():

    def __init__(self, language, config):
        self.config = config
        self.has_model = True
        model = None
        supported_languages = config['spacy']['lang'].keys()
        if language in supported_languages:
            model = config['spacy']['model'][language]

        if model != None:
            self._nlp = spacy.load(model)
        else:
            self.has_model = False

    def annotate(self, text):
        doc = self._nlp(text)
        entities = doc.ents
        output = self.wrapper(entities)
        return output



    def wrapper(self, annotations_in):
        annotations = []
        cfg = self.config

        for ent in annotations_in:
            annotations.append({
                'text': ent.text,
                'label': convert_tag(ent.label_, cfg),
                'start_char': ent.start_char,
                'end_char': ent.end_char,
            })
        return annotations


