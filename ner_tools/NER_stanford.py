# from nltk import word_tokenize
# from nltk.tag.stanford import StanfordNERTagger
# from nltk import *
# import ner
# classifier = '\\usr\\share\\stanford-ner\\classifiers\\english.all.3class.distsim.crf.ser.gz'
# jar = '/usr/share/stanford-ner/stanford-ner.jar'

# tagger = ner.SocketNER(host='localhost', port=90)
# tagger.get_entities("University of California is located in California, United States")

# st = StanfordNERTagger(classifier, jar)
# sentence = word_tokenize("Rami Eid is studying at Stony Brook University in NY")
# print(st.tag(sentence))
import nltk.tag.stanford as st
import os
from utils import convert_tag

class ner_stanford():
    def __init__(self, language, config):

        self.config = config
        self.has_model = True
        jar = os.path.abspath("models/stanford-ner-2018-10-16/stanford-ner-2018-10-16/stanford-ner.jar")
        supported_lanugages = config['stanford']['lang'].keys()
        if language in supported_lanugages:
            model = os.path.abspath('models/'+config['stanford']['model'][language])
        else:
            model = None
            self.has_model = False
        self.tagger = None

        if model!= None:
            self.tagger = st.StanfordNERTagger(model, jar)
            # jar = "C:/Users/TahmasebzadehG/PycharmProjects/AnnotateDataset/models/stanford-ner-2018-10-16/stanford-ner-2018-10-16/stanford-ner.jar"
            # # jar = 'C:/Users/TahmasebzadehG/PycharmProjects/AnnotateDataset/models/stanford-german-corenlp-2018-10-05-models.jar'
            # model = "C:/Users/TahmasebzadehG/PycharmProjects/AnnotateDataset/models/german.conll.germeval2014.hgc_175m_600.crf.ser.gz"
            # self.tagger = st.StanfordNERTagger(model, jar)
            # m=self.annotate("Obama trifft Merkel in den USA")
            # print(m)


    def annotate(self, text):

        output = ""
        if self.tagger!=None:
           annotations = self.tagger.tag(text.split())
           output = self.wrapper(annotations, text)

        return output



    def wrapper(self, annotations_in, doc):
        # ners = self.get_neRs(text, language)
        annotations = []
        end_char = 0
        cfg = self.config

        for ent in annotations_in:
            text = ent[0]
            start_char = doc.find(text, end_char)
            end_char = start_char + len(text)
            if ent[1] != "O":
                annotations.append({
                        'text': text,
                        'label': convert_tag(ent[1], cfg),
                        'start_char': start_char,
                        'end_char': end_char,
                    })
        return annotations

import json
def main():

    text = "Obamam meets in U.S."
    with open("C:/Users/TahmasebzadehG/PycharmProjects/AnnotateDataset/configs/NER_config") as json_data:
        conf= json.load(json_data)
    n = ner_stanford("deu",conf)

    text0 = "Oppersdorf geh\u00f6rte bis 1945 zu den deutschen Gebieten und zum Regierungsbezirk Oppeln in Oberschlesien. Kreisstadt war die Stadt Neisse. Heute geh\u00f6rt Oppersdorf zu Polen, polnischer Name: Wierzbi\u0119cice. Der Ort liegt im Powiat Nyski in der Woiwodschaft Opole.\n\nOppersdorf, ein Stra\u00dfendorf im Oppelsdofer H\u00fcgelland, liegt 10 km von Neisse entfernt an der ehemaligen Reichsstra\u00dfe Nr. 115 nach Neunz, 270-300 m \u00fcber NN. Diese Stra\u00dfe, die sogenannte \"gro\u00dfe Stra\u00dfe\" war ein alter, wichtiger Handelsweg nach M\u00e4hren. Das Dorf hatte einen Bahnhof an der Kreisbahn nach Steinau; eine Postagentur - \u00fcber 60 Jahre von der Familie Teuber betreut - war im Ort.\n\nDie Gemeindeflur ist 1120 ha gro\u00df. Flurnamen sind: Galgen und Pranger (1735), Glotzberg, der Hofewoal, Keil, Mordgrund, Zienke. 1781 bestand noch eine ritterm\u00e4\u00dfige Scholtisei.\n\nIm Jahr 1937 gab es im Ort: 2 B\u00e4cker, 1 Baugesch\u00e4ft,1 Brennmaterialhandlung, 2 Fleischer, 1 Friseur, 3 Gasth\u00f6fe, 4 Gemischtwarenl\u00e4gen, 2 Maler, 1 Molkerei, 1 Schlosser, 2 Schmiede, 1 Schneider, 4 Schuhmacher, 1 Stellmacher, 3 Tischler, 1 Spar- und Darlehnskasse, 1 Arzt, 1 Hebamme. An der Hauptstra\u00dfe lag das \"Gasthaus zur Erholung\" (1848 erbaut, seit 1920 im Besitz der Familie Urbach), das in der Zeit vor dem Eisenbahnverkehr ein Umspannplatz f\u00fcr die Pferdefuhrwerke gewesen war.\n\nOppersdorf (B\u00fcrgermeister 1935: Bauergutsbesitzer Johann Eckert; 1939: Bauer Albert Hauschild; 1942:"

    n.tagger.tag(text.split())
    print("")




    n.annotate("Obamam meets in U.S.")

if __name__ == '__main__':
    main()
