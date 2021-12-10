import argparse
import json
import logging
import os
import requests
import sys
import time


class ambiverse():

    def __init__(self, language='en', port=8080):
        self._language = language
        # self._endpoint = f"http://localhost:{str(port)}/factextraction/analyze"
        self._endpoint = f"http://localhost:{str(port)}/entitylinking/analyze"
        self._headers = {'accept': 'application/json', 'content-type': 'application/json'}

    def annotate(self, text, id='test', confidence_threshold=0.075):
        data = json.dumps({
            'docId': id,
            'text': text,
            'language': self._language,
            "extractConcepts": 'true',
            'coherentDocument': 'true'
        })

        i = 0
        while True:
            i += 1
            try:
                r = requests.post(url=self._endpoint, headers=self._headers, data=data)
                response = r.json()
                annotations = {'processed': True, 'annotations': response['matches']}
                return annotations
            except KeyboardInterrupt:
                raise
            except Exception as e:
                print(e)
                # logging.error(f'Got no response from wikidata: {r}. Retry {i}')
                # logging.error('Got no response from wikidata')
                time.sleep(3)

                if i > 9:
                    return {'processed': False, 'annotations': []}


    def wrapper(self, named_links_in, article_in_uri):
        annotations = []
        for nl in named_links_in['annotations']:
            support = []
            for s in nl['support']:
                dicSupport = {'wFrom': s['wFrom'], 'wTo': s['wTo'], 'chFrom': s['chFrom'], 'chTo': s['chTo'] }
                support.append(dicSupport)
            dicAnnotations = {'url': nl['url'], 'title': nl['title'], 'pageRank': nl['pageRank'], 'linkedWords': support}
            annotations.append(dicAnnotations)
        dicFinal = {'articleURI': article_in_uri, 'annotations':annotations}
        # format:
        # [{'articleURI': "", 'annotations':['url':"",'text':"", 'wFrom': 0, 'wTo': 0, 'chFrom': 0, 'chTo': 4, 'pageRank':"", 'other':[]  ] } ]
        return dicFinal


def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-v', '--info', action='store_true', help='info output')
    parser.add_argument('-vv', '--debug', action='store_true', help='debug output')
    parser.add_argument('-l', '--language', type=str, default='en', help='specified language')
    parser.add_argument('-t', '--text', type=str, required=True, help='input text to process')
    parser.add_argument('--port', type=int, default=8080, help='docker port of ambiverse NLU')
    args = parser.parse_args()
    '''
    curl --request POST \
      --url http://localhost:8080/factextraction/analyze \
      --header 'accept: application/json' \
      --header 'content-type: application/json' \
      --data '{"docId": "doc1", "language": "en", "text": "Jack founded Alibaba with investments from SoftBank and Goldman.", "extractConcepts": "true" }'
    '''
    return args


def main():
    # # load arguments
    # args = parse_args()
    #
    # # define logging level and format
    # level = logging.ERROR
    # if args.info:
    #     level = logging.INFO
    # if args.debug:
    #     level = logging.DEBUG
    #
    # logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=level)

    argslanguage = "en"
    argsport = "8080"
    argstext = "Obama meets Merkel in U.S."
    # init wikifier
    aa = ambiverse(argslanguage, argsport)
    entities = aa.annotate(argstext)

    if entities['processed']:
        for ent in entities['annotations']:
            for key in ent.keys():
                logging.info(f"{key}: {ent[key]}")
        logging.info('################')

    return 0


if __name__ == '__main__':
    sys.exit(main())
