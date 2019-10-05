#!/usr/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup
from translate import Translator


def is_language_code(language):
    '''
    Check language argument against list of language codes scraped from 
    https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes; e.g., es, en, de, etc.
    '''

    URL = 'https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes'
    r = requests.get(URL)

    soup = BeautifulSoup(r.text, 'html.parser')

    for anchor_tag in soup.find_all('a'):
        if anchor_tag.string and len(anchor_tag.string) == 2:
            if anchor_tag.string == language:
                return True
    return False


def main():
    print(is_language_code)
    # make sure correct command-line arguments were supplied
    try:
        in_filename = sys.argv[1]
        language = sys.argv[2]

        if not is_language_code(language):
            raise Exception(
                'Please enter a valid two-letter language code. '
                'See https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes for a list.'
            )
    except (Exception, IndexError) as e:
        print(f'{e}\nUsage: {sys.argv[0]} [filename] [language code]')
        sys.exit()

    translator = Translator(to_lang=language)

    # read in file and output translated file;
    # e.g., in: stuff.txt  ->  out: stuff-translated-es.txt
    try:
        with open(in_filename) as in_file:
            text = in_file.read()
            translation = translator.translate(text)

            out_filename = f"{in_filename.split('.')[0]}-translated-{language}.txt"

            with open(out_filename, mode='w') as out_file:
                out_file.write(translation + '\n')
    except (FileNotFoundError, IOError) as e:
        print(e)


if __name__ == '__main__':
    main()
