import argparse
import json
import requests
from bs4 import BeautifulSoup
import pyperclip 

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verse", help="verse query", type=str)
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

def get_verse(book:str, chapter:str, number:str, version:int=177) -> str: 
    if number == "*":
        url = f"https://www.bible.com/bible/{version}/{book}.{chapter}"
    else:
        url = f"https://www.bible.com/bible/{version}/{book}.{chapter}.{number}"
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    
    l1 = soup.find_all("h1", class_="f6 f5-m mb3 yv-gray50") 
    for i in l1:
        heading = i.get_text()
    
    l2 = soup.find_all("div", class_="yv-gray50 lh-copy f3-m") 
    for i in l2:
        verse = i.get_text()
    return heading, verse

def convert_to_markdown(heading, bible_verse):
    return f"""# {heading}
> {bible_verse}
"""
    
def main(verse=None):
    if verse == None:
        verse = input("Enter query: ")
    
    book, chapter, number = parse_verse(verse)
    book_abbv = convert_to_keyword(book)
    print(f"book_abbv:", book_abbv)

    heading, bible_verse = get_verse(book_abbv, chapter, number)
    print(f"copied \"{bible_verse}\" to clipboard ")

    heading = " ".join(heading.split(" ")[:-1])
    md = convert_to_markdown(heading, bible_verse)
    pyperclip.copy(md)
    return 

if __name__ == "__main__":
    args = get_args()
    if args.verse:
        main(args.verse)

    while True:
        main()
