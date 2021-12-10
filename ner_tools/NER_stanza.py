import stanza
from utils import *

class ner_stanza():

   def __init__(self, language, config):
       self.config = config
       self.has_model = True
       model = None
       supported_languages = config['stanza']['lang'].keys()
       if language in supported_languages:
           model = config['stanza']['model'][language]

       if model != None:
           self.nlp = stanza.Pipeline( config['stanza']["lang"][language])
       else:
           self.has_model = False

   def annotate(self, text):
       entities = self.nlp(text)
       output = self.wrapper(entities)
       return output

   def wrapper(self, annotations_in):
       annotations = []
       cfg = self.config

       for ent in annotations_in._ents:
           annotations.append({
               'text': ent.text,
               'label': convert_tag(ent.type, cfg),
               'start_char': ent.start_char,
               'end_char': ent.end_char,
           })
       return annotations