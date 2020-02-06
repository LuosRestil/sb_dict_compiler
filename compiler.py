import requests
import re
from bs4 import BeautifulSoup
import string
import time

# Ideally, should build a json structure so words can be found more quickly


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
        else:
            print('webster: hword != word')
            variations = soup.find_all('span', class_='va')
            if variations:
                print('webster: variations found')
                for variation in variations:
                    contents = variation.contents[0]
                    if word == contents:
                        print('webster: valid')
                        return True
            forms = soup.find_all('span', class_='if')
            if forms:
                print('webster: forms found')
                for form in forms:
                    contents = form.contents[0]
                    if word == contents:
                        print('webster: valid')
                        return True
            other_words_from = soup.find_all('span', class_='ure')
            if other_words_from:
                print('webster: other words from found')
                for other_word in other_words_from:
                    contents = other_word.contents[0]
                    if word == contents:
                        print('webster: valid')
                        return True
            print('webster: invalid')
    else:
        print('webster: invalid')
    return False


def check_oxford(word):
    print('oxford: checking')
    # built-in delay so I don't get shut down by anti-scraping measures
    time.sleep(5)
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
                        stripped = form.find('span').contents[0].translate(
                            str.maketrans('', '', string.punctuation))
                        if stripped == word:
                            print('oxford: valid')
                            return True
            except AttributeError:
                pass
            try:
                variants = soup.find(
                    'div', class_='variant').find_all('strong')
                if variants:
                    print('oxford: variants found')
                    for variant in variants:
                        if variant.contents[0] == word:
                            (print('oxford valid'))
                            return True
            except AttributeError:
                pass
    else:
        print('oxford: no exact matches')
        similar_results = soup.find('div', class_='similar-results').a['href']
        if similar_results == word:
            print('oxford: valid')
            return True
        elif word.endswith('s') and similar_results == word[0:-1]:
            print('oxford: valid')
            return True
        elif word.endswith('es') and similar_results == word[0:-2]:
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
                    stripped = form.find('span').contents[0].translate(
                        str.maketrans('', '', string.punctuation))
                    if stripped == word:
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


def check_word(word):
    print(word)
    if check_webster(word):
        return True
    elif check_oxford(word):
        return True
    else:
        return False


with open('filtered_dict.txt', 'r') as infile:
    with open('valid.txt', 'w') as valid:
        with open('invalid.txt', 'w') as invalid:
            with open('possible_plural_or_3ps.txt', 'w') as pp:
            for line in infile:
                word = line[0:-1]
                if check_word(word):
                    print(f'{word}: VALID')
                    valid.write(line)
                else:
                    print(f'{word}: INVALID')
                    if word.endswith('s'):
                        pp.write(line)
                    else:
                        invalid.write(line)


# print(check_word('cancelable'))
