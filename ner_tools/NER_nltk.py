import nltk
from utils import convert_tag
# nltk.download()
class ner_nltk():

    def __init__(self, language, config):

        self.has_model = True
        self.config = config
        supported_lanugages = config['nltk']['lang'].keys()
        if language in supported_lanugages:
            self.language = config['nltk']['lang'][language]
        else:
            self.has_model = False


    def annotate(self, text):

        try:
            tokenized = nltk.word_tokenize(text, language=self.language)
            tagged = nltk.pos_tag(tokenized)
            namedEnt = nltk.ne_chunk(tagged)

            if namedEnt != "":
                ner_output_per_article = self.wrapper(namedEnt, text)

        except Exception as e:
            print(e)

        return ner_output_per_article





    def wrapper(self, annotations_in, doc):

        annotations = []
        end_char = 0
        cfg = self.config

        for chunk in annotations_in:

                if hasattr(chunk, 'label'):

                    annos = ([chunk.label(), ' '.join(c[0] for c in chunk)])
                    tag = annos[0]
                    text = annos[1]
                    # if text in tags:
                    #         temp = text
                    #         text = tag
                    #         tag = temp

                    start_char = doc.find(text, end_char)
                    end_char = start_char + len(text)

                    annotations.append({
                                        'text': text,
                                        'label': convert_tag(tag, cfg),
                                        'start_char': start_char,
                                        'end_char': end_char,
                                    })

        return annotations


def main():
    n = ner_nltk()

    text0 = "Oppersdorf geh\u00f6rte bis 1945 zu den deutschen Gebieten und zum Regierungsbezirk Oppeln in Oberschlesien. Kreisstadt war die Stadt Neisse. Heute geh\u00f6rt Oppersdorf zu Polen, polnischer Name: Wierzbi\u0119cice. Der Ort liegt im Powiat Nyski in der Woiwodschaft Opole.\n\nOppersdorf, ein Stra\u00dfendorf im Oppelsdofer H\u00fcgelland, liegt 10 km von Neisse entfernt an der ehemaligen Reichsstra\u00dfe Nr. 115 nach Neunz, 270-300 m \u00fcber NN. Diese Stra\u00dfe, die sogenannte \"gro\u00dfe Stra\u00dfe\" war ein alter, wichtiger Handelsweg nach M\u00e4hren. Das Dorf hatte einen Bahnhof an der Kreisbahn nach Steinau; eine Postagentur - \u00fcber 60 Jahre von der Familie Teuber betreut - war im Ort.\n\nDie Gemeindeflur ist 1120 ha gro\u00df. Flurnamen sind: Galgen und Pranger (1735), Glotzberg, der Hofewoal, Keil, Mordgrund, Zienke. 1781 bestand noch eine ritterm\u00e4\u00dfige Scholtisei.\n\nIm Jahr 1937 gab es im Ort: 2 B\u00e4cker, 1 Baugesch\u00e4ft,1 Brennmaterialhandlung, 2 Fleischer, 1 Friseur, 3 Gasth\u00f6fe, 4 Gemischtwarenl\u00e4gen, 2 Maler, 1 Molkerei, 1 Schlosser, 2 Schmiede, 1 Schneider, 4 Schuhmacher, 1 Stellmacher, 3 Tischler, 1 Spar- und Darlehnskasse, 1 Arzt, 1 Hebamme. An der Hauptstra\u00dfe lag das \"Gasthaus zur Erholung\" (1848 erbaut, seit 1920 im Besitz der Familie Urbach), das in der Zeit vor dem Eisenbahnverkehr ein Umspannplatz f\u00fcr die Pferdefuhrwerke gewesen war.\n\nOppersdorf (B\u00fcrgermeister 1935: Bauergutsbesitzer Johann Eckert; 1939: Bauer Albert Hauschild; 1942:"
    text = "Obamam meets in U.S."
    text = "America pays 9000 dollars 40% and 56 percent in 34 hours in 16 Feb 2019 for which 10000 people will come.OTTAWA (Reuters) - Canadian Foreign Minister Chrystia Freeland on Wednesday warned the United States not to politicize extradition cases, a day after President Donald Trump said he could intervene in the affair of a Chinese executive detained in Canada at Washington's request.\n\nFreeland also told reporters that a second Canadian citizen could be in trouble in China. Authorities in China are already holding former diplomat Michael Kovrig, who was detained on Monday.\n\nChina has strongly protested the arrest in Vancouver on Dec. 1 of Huawei Technologies Co Ltd Chief Financial Officer Meng Wanzhou. Meng has been accused by U.S. prosecutors of misleading multinational banks about Iran-linked transactions, putting the banks at risk of violating U.S. sanctions. She has said she is innocent.\n\nTrump told Reuters on Tuesday he would intervene https://www.reuters.com/article/us-usa-trump/trump-says-would-intervene-in-arrest-of-chinese-executive-idUSKBN1OB01P in the U.S. Justice Department's case against Meng if it would serve national security interests or help close a trade deal with China.\n\nBut the legal process should not be hijacked for political purposes, Freeland said.\n\n\"Our extradition partners should not seek to politicize the extradition process or use it for ends other than the pursuit of justice and following the rule of law,\" Freeland said when asked about Trump's comments.\n\nOthers also questioned whether Trump might be misusing the extradition request.\n\n\"This is a legal issue and one that appears properly executed but your comments can only diminish an important extradition agreement we have with our next door neighbor,\" said Bruce Heyman, an ex-U.S. ambassador to Canada who was appointed by President Barack Obama, Trump's predecessor.\n\nMeng was released on bail by a Canadian court on Tuesday.\n\nThe United States has not yet made a formal extradition petition. Once it does, if a Canadian judge rules in favor of the request, Canada's justice minister must decide whether to extradite Meng to the United States.\n\nFreeland expressed deep concern over the Kovrig case and said a second unnamed Canadian had made contact with Canadian authorities to say Chinese officials were asking him questions. Canada has not been able to make contact with him since, she added.\n\nOfficials said earlier they have no indication from Beijing that Kovrig's detention was tied to Canada's arrest of Meng.\n\nBut they have seen an uptick in anti-Canadian sentiment online and in China, an official said, and have communicated concerns about diplomatic staff safety to the Chinese government, which beefed up security in response.\n\n\"We have in general informed our personnel in Beijing and in our consulates to take extra precautions,\" an official said.\n\n(Reporting by David Ljunggren and Anna Mehler Paperny; editing by Bernadette Baum and Rosalba O'Brien"
    text = "Donald John Trump (born June 14, 1946) is the 45th and current president of the United States. Before entering politics, he was a businessman and television personality. Trump was born and raised in Queens, a borough of New York City, and received a bachelor's degree in economics from the Wharton School. He took charge of his family's real-estate business in 1971, renamed it The Trump Organization, and expanded its operations from Queens and Brooklyn into Manhattan. The company built or renovated skyscrapers, hotels, casinos, and golf courses. Trump later started various side ventures, mostly by licensing his name. He owned the Miss Universe and Miss USA beauty pageants from 1996 to 2015, and produced and hosted The Apprentice, a reality television show, from 2003 to 2015. Forbes estimates his net worth to be $3.1 billion.[a] Trump entered the 2016 presidential race as a Republican and defeated 16 other candidates in the primaries. His political positions have been described as populist, protectionist, and nationalist. Despite not being favored in most forecasts, he was elected in a surprise victory over Democratic nominee Hillary Clinton, although he lost the popular vote.[b] He became the oldest first-term U.S. president,[c] and the first without prior military or government service. His election and policies have sparked numerous protests. Trump has made many false or misleading statements during his campaign and presidency. The statements have been documented by fact-checkers, and the media have widely described the phenomenon as unprecedented in American politics. Many of his comments and actions have also been characterized as racially charged or racist.During his presidency, Trump ordered a travel ban on citizens from several Muslim-majority countries, citing security concerns; after legal challenges, the Supreme Court upheld the policy's third revision. He enacted a tax-cut package for individuals and businesses, rescinding the individual health insurance mandate. He appointed Neil Gorsuch and Brett Kavanaugh to the Supreme Court. In foreign policy, Trump has pursued an America First agenda, withdrawing the U.S. from the Trans-Pacific Partnership trade negotiations, the Paris Agreement on climate change, and the Iran nuclear deal, eventually increasing tensions with the country. He recognized Jerusalem as the capital of Israel, imposed import tariffs triggering a trade war with China, and attempted negotiations with North Korea toward its denuclearization. A special counsel investigation led by Robert Mueller found that Trump and his campaign welcomed and encouraged Russian foreign interference in the 2016 presidential election under the belief that it would be politically advantageous, but did not find sufficient evidence to press charges of criminal conspiracy or coordination with Russia. Mueller also investigated Trump for obstruction of justice, and his report neither indicted nor exonerated Trump on that count. A 2019 House impeachment inquiry found that Trump solicited foreign interference in the 2020 U.S. presidential election from Ukraine to help his re-election bid and then obstructed the inquiry itself. The inquiry reported that he withheld military aid and a White House invitation in order to influence Ukraine to publicly announce investigations into his political rivals. Trump was impeached by the House of Representatives on December 18, 2019 for abuse of power and obstruction of Congress. He is the third[d] U.S. president to be impeached. The impeachment trial began on January 16, 2020."
    y=n.annotate(text)
    print("")

if __name__ == '__main__':
    main()
