import argparse
import json
import logging
import os
from requests import HTTPError
import spotlight
import subprocess
import sys
import time


class dbpedia():

    def __init__(self, dbpedia_folder=None, port=5050, language='en', wait_sec_for_server_start=100):
        # start dbpedia spotlight
        # NOTE: building dbpedia outside this functions saves memory and time
        if dbpedia_folder is not None:
            logging.info('Starting DBpedia Spotlight in offline mode ...')

            cmd_str = 'JAVA_HOME=/usr/lib/jvm/java-8-openjdk/jre java -jar dbpedia-spotlight-1.0.0.jar'
            cmd_str += ' ' + language
            cmd_str += ' ' + 'http://localhost:' + str(port) + '/rest/'

            self._dbpedia_deamon = subprocess.Popen(cmd_str, cwd=dbpedia_folder, shell=True)
            time.sleep(wait_sec_for_server_start)
            logging.info('DBpedia Spotlight initialized!')

    @staticmethod
    def annotate(text, filters={'policy': 'whitelist'}, confidence=0.7, support=20, port=5050):
        # if not already annotated, create annotations using dbpedia spotlight
        url = 'http://localhost:' + str(port) + '/rest/annotate'
        return spotlight.annotate(url, text, filters=filters, confidence=confidence, support=support)

        '''
        try:
            url = 'http://localhost:' + str(port) + '/rest/annotate'
            return spotlight.annotate(url, text, filters=filters, confidence=confidence, support=support)
        except spotlight.SpotlightException as e:
            if 'forgot the protocol' in str(e):
                raise e
            return []  # no annotations found for given text and filters
        except HTTPError as e:
            print(e)
            return []
        '''


'''
########################################################################################################################
Main for testing
########################################################################################################################
'''


def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-v', '--info', action='store_true', help='info output')
    parser.add_argument('-vv', '--debug', action='store_true', help='debug output')
    parser.add_argument('-d', '--dbpedia', required=False, help='Path to dbpedia spotlight directory')
    parser.add_argument('-t', '--text', default='Angela Merkel meets president Obama at New York', help='test text')
    args = parser.parse_args()
    return args


def main():
    # load arguments
    args = parse_args()

    # define logging level and format
    # define logging level and format
    level = logging.ERROR
    if args.info:
        level = logging.INFO
    if args.debug:
        level = logging.DEBUG

    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=level)

    try:
        dba = dbpedia(dbpedia_folder=args.dbpedia)
        annotations = dba.get_annotations(text=args.text)
        # doc_id='test',
        print(annotations)
    finally:
        if args.dbpedia is not None:
            dba._dbpedia_deamon.terminate()

    return 0


if __name__ == '__main__':
    sys.exit(main())
