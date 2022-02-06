import requests
import argparse

from bs4 import BeautifulSoup


def get_page(lang_source, lang_target, word):
    url = f"https://context.reverso.net/translation/{lang_source.strip().lower()}-{lang_target.strip().lower()}/{word}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=headers)
    assert page.status_code != 404
    return page


def translation(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    translation_content = soup.find('div', id='translations-content').find_all('a')
    words = []
    for translations in translation_content:
        words.append(translations.text.strip())
    sentences_src, sentences_target = \
        soup.find_all('div', {"class": "src ltr"}), \
        soup.find_all('div', {"class": ["trg ltr", "trg rtl arabic", "trg rtl"]})
    sentences_pair = list(zip(map(lambda sent: sent.text.strip(), sentences_src),
                              map(lambda sent: sent.text.strip(), sentences_target)))
    return words, sentences_pair


def print_translation(words, sentences_pair, lang_target, word):
    print(f"\n{lang_target} Translations:")
    print(words[0])
    print(f"\n{lang_target} Examples:")
    src, trg = sentences_pair[0]
    print(src)
    print(trg)
    with open(f"{word}.txt", 'a', encoding='utf-8') as f:
        f.write(f"{lang_target} Translations:\n{words[0]}\n\n{lang_target} Examples:\n{src}\n{trg}\n\n")


def main():
    parser = argparse.ArgumentParser(description="Multilingual Online Translator")
    parser.add_argument("source", help="Source language")
    parser.add_argument("target", help="Target language")
    parser.add_argument("word", help="Type the word you want to translate. \"all\" for all languages.")
    args = parser.parse_args()
    languages = ["Arabic", "German", "English", "Spanish", "French",
                 "Hebrew", "Japanese", "Dutch", "Polish", "Portuguese",
                 "Romanian", "Russian", "Turkish"]
    lang_source = args.source
    lang_target = args.target
    word = args.word.strip().lower()

    if lang_target != "all":
        try:
            page = get_page(lang_source, lang_target, word)
            words, sentences_pair = translation(page)
            print_translation(words, sentences_pair, lang_target, word)
        except AssertionError:
            print(f"Sorry, unable to find {word}")
        except AttributeError:
            print(f"\nSorry, the program doesn't support {lang_target}\n\n")
        except ConnectionError:
            print("Something wrong with your internet connection")
    else:
        for lang in languages:
            if lang.lower() == lang_source:
                continue
            try:
                page = get_page(lang_source, lang, word)
                words, sentences_pair = translation(page)
                print_translation(words, sentences_pair, lang, word)
            except AssertionError:
                print(f"Sorry, unable to find {word}")
            except AttributeError:
                print(f"\nSorry, the program doesn't support {lang_target}\n\n")


if __name__ == '__main__':
    main()
