import argparse
import json

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verse", help="verse snippet", type=str)
    args = parser.parse_args()
    return args

def get_keywords():
    with open('keywords.json', 'r') as se_json:
        keywords = json.load(se_json)
    return keywords

KEYWORDS = get_keywords()
def convert_to_keyword(raw: str) -> str: 
    for abbv in KEYWORDS:
        for keyword in KEYWORDS[abbv]:
            if raw.lower() == keyword.lower() or\
                raw.lower() == abbv.lower():
                return abbv
    return ""

def parse_verse(verse: str) -> str:
    v = verse.split(" ")
    book = v[0]

    if ":" in v[1]:
        n = v[1].split(":")
        chapter = n[0]
        number = n[1]
    else:
        chapter = v[1]
        number = "*"

    print(f"book: {book}")
    print(f"chapter: {chapter}")
    print(f"no: {number}")

    return (book, chapter, number)

def get_verse(book:str, chapter:str, number:str, version:int=1) -> str: 
    # URL = [http: // [version]/[book].[verses]]
    # docu = getDocument(url)
    # bible_verse = findclass(docu)
    return "bible verse"

def main(verse=None):
    if verse == None:
        verse = input("Enter query: ")
    
    book, chapter, number = parse_verse(verse)
    book_abbv = convert_to_keyword(book)
    print(f"book_abbv:", book_abbv)
    bible_verse = get_verse(book_abbv, chapter, number)

    # copy bible verse to clipboard 
    return 


if __name__ == "__main__":
    args = get_args()
    if args.verse:
        main(args.verse)

    while True:
        main()
