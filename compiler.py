import requests
import re
from bs4 import BeautifulSoup
import string

# Ideally, should build a json structure, {a: {word: worddef, word: worddef, ...}, {b: {word:, worddef, ...}, ...}
# Could then search for words more quickly, and definitions are available without API

def check_webster(word):
    print('webster: checking')
    r = requests.get(f'https://www.merriam-webster.com/dictionary/{word}')
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        hword = soup.find('h1', class_='hword').contents[0]
        if hword == word:
            print('webster: valid')
            return True
        elif word.endswith('s') and hword == word[0:-1]:
            print('webster: valid')
            return True
        elif word.endswith('es') and hword == word[0:-2]:
            print('webster: valid')
            return True
        elif word.endswith('ies') and hword == word[0:-3] + 'y':
            print('webster: valid')
            return True
        else:
            print('webster: hword != word')
            variations = soup.find_all('span', class_='va')
            if variations:
                print('webster: variations found')
                for variation in variations:
                    if word == variation.contents[0]:
                        print('webster: valid')
                        return True
            forms = soup.find_all('span', class_='if')
            if forms:
                print('webster: forms found')
                for form in forms:
                    if word == form.contents[0]:
                        print('webster: valid')
                        return True
    else:
        print('webster: invalid')
    return False


def check_oxford(word):
    print('oxford: checking')
    r = requests.get(f'https://www.lexico.com/definition/{word}')
    soup = BeautifulSoup(r.text, 'html.parser')
    no_exact_matches = soup.find('div', class_='no-exact-matches')
    if not no_exact_matches:
        hw = soup.find('span', class_='hw').contents[0]
        if hw == word:
            print('oxford: valid')
            return True
        elif word.endswith('s') and hw == word[0:-1]:
            print('oxford: valid')
            return True
        elif word.endswith('es') and hw == word[0:-2]:
            print('oxford: valid')
            return True
        elif word.endswith('ies') and hw == word[0:-3] + 'y':
            print('oxford: valid')
            return True
        else:
            print('oxford: hw != word')
            try:
                forms = soup.find_all('span', class_='inflection-text')
                if forms:
                    print('oxford: forms found')
                    for form in forms:
                        if form.find('span').contents[0].translate(str.maketrans('', '', string.punctuation)) == word:
                            print('oxford: valid')
                            return True
            except AttributeError:
                pass
            try:
                variants = soup.find('div', class_='variant').find_all('strong')
                if variants:
                    print('oxford: variants found')
                    for variant in variants:
                        if variant.contents[0] == word:
                            print('oxford: valid')
                            return True
            except AttributeError:
                pass
    else:
        print('oxford: no exact matches')
        similar_results = soup.find('div', class_='similar-results').a['href']
        if similar_results == word:
            print('Oxford valid')
            return True
        elif word.endswith('s') and similar_results == word[0:-1]:
            print('oxford: valid')
            return True
        elif word.endswith('es') and similar_results == word[0:-2]:
            print('oxford: valid')
            return True
        elif word.endswith('ies') and similar_results == word[0:-3] + 'y':
            print('oxford: valid')
            return True
        print(f'oxford: redirecting to {similar_results}')
        redirect = requests.get(f'https://www.lexico.com{similar_results}')
        soup = BeautifulSoup(redirect.text, 'html.parser')
        try:
            forms = soup.find_all('span', class_='inflection-text')
            if forms:
                print('oxford: forms found')
                for form in forms:
                    if form.find('span').contents[0].translate(str.maketrans('', '', string.punctuation)) == word:
                        print('oxford: valid')
                        return True
        except AttributeError:
            pass
        try:
            variants = soup.find('div', class_='variant').find_all('strong')
            if variants:
                print('oxford: variants found')
                for variant in variants:
                    if variant.contents[0] == word:
                        (print('oxford valid'))
                        return True
        except AttributeError:
            pass

    print('oxford: invalid')
    return False


def check_wiktionary(word):
    '''
    check lang of word span.mw-headline == English
    :param word:
    :return:
    '''
    r = requests.get(f'https://en.wiktionary.org/wiki/{word}')
    soup = BeautifulSoup(r.text, 'html.parser')
    english = soup.find('span', id="English")
    if english:
        match = soup.find('div', class_="mw-parser-output").find_all('ol')
        for item in match:
            print(item.get_text())


def check_word(word):
    print(word)
    if check_webster(word):
        return True
    elif check_oxford(word):
        return True
    else:
        return False

print(check_word('becky'))