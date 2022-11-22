#!/usr/bin/python3
import requests as re
from bs4 import BeautifulSoup
import argparse
import os
import pyinputplus as pyip
import sys

# Add StatusCodes Here
STATUS_CODES = [200,404]

BANNER = """ _      __________       _          _______        ________________ _______ _______________________ _______ 
( \     \__   __( (    /| \    /\  (  ____ \\     /\__   __(  ____ |  ___  |  ____ \__   __(  ___  |  ____ )
| (        ) (  |  \  ( |  \  / /  | (    \( \   / )  ) (  | (    )| (   ) | (    \/  ) (  | (   ) | (    )|
| |        | |  |   \ | |  (_/ /   | (__    \ (_) /   | |  | (____)| (___) | |        | |  | |   | | (____)|
| |        | |  | (\ \) |   _ (    |  __)    ) _ (    | |  |     __)  ___  | |        | |  | |   | |     __)
| |        | |  | | \   |  ( \ \   | (      / ( ) \   | |  | (\ (  | (   ) | |        | |  | |   | | (\ (   
| (____/\__) (__| )  \  |  /  \ \  | (____/( /   \ )  | |  | ) \ \_| )   ( | (____/\  | |  | (___) | ) \ \__
(_______|_______//    )_)_/    \/  (_______//     \|  )_(  |/   \__//     \(_______/  )_(  (_______)/   \__/

                                                                                               -By EXCEPTIONAL             
                                                                                                            """


print(BANNER)


USAGE = """

 Download Source page
 extract links  
"""



parser = argparse.ArgumentParser(USAGE)
parser.add_argument('-u', '--url',  type=str,metavar="", required=True,
                    help='example = https://www.example.com')
parser.add_argument('-o', '--out',metavar="", default="sample", type=str, required=True,
                    help='example = output.txt')

parser.add_argument('-p', '--print', required=False, action='store_true'
                    )
parser.add_argument('-x', '--extract_urls', required=False, action='store_true'
                    )




args = parser.parse_args()



URL = args.url
OUTPUT_FILE = args.out

response = re.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

def defaultFileName(OUTPUT_FILE):
    remove_chars = ["", "http:", "https:"]
    final_url = ""
    url = str(OUTPUT_FILE).split('/')
    for i in url:
        if i in remove_chars:
            url.remove(i)

    for ele in url:
        final_url += f"{ele}_"

    return final_url


def writeTofile(content):
    if os.path.exists(OUTPUT_FILE):
        promptMSG = f"File ({OUTPUT_FILE}) already exists \n would you like to overWrite? \n1)yes\n2)no\n"
        option = pyip.inputChoice(
            prompt=promptMSG, choices=['1', '2'])
        print("\nSelected Option: " + option)
        if option == '1':
            print(f"File ({OUTPUT_FILE}) over Written!!")
            with open(OUTPUT_FILE, 'w')as f:
                f.write(content)
        else:
            print("\nMSG: No Changes made to file")
    else:
        with open(OUTPUT_FILE, 'w')as f:
            f.write(content)


def overWrite():
    """
    Overwrite a file Option
    Returns option
    """
    promptMSG = f"\nWould you like to overwrite the existing File ?\n1)yes\n2)no ?   "
    option = pyip.inputChoice(prompt=promptMSG, choices=['1', '2'])
    return option


def writeURLS(filename):
    """
    Writes Data urls From Lists to a file"""
    URLS = []
    for link in soup.find_all('a'):
        URLS.append(link.get('href'))
    with open(filename, 'w') as f:
        for i in URLS:
            url = f"{i}\n"
            f.write(url)


def extract_urls(filename):
    filename = f"EXTRACTED_URLS_{defaultFileName(OUTPUT_FILE)}.txt"
    if os.path.exists(filename):
        print(f"{filename} Exists")
        option = overWrite()
        if option == "yes":
            writeURLS(filename)
        else: 
            print(f"No Changes made to {filename}")
    else:
        writeURLS(filename)

        # Write To File
        # URL = "http://ptl-65dde18e-5c2240ac.libcurl.so/"
def myprog():
    if response.status_code in STATUS_CODES:
       
        if args.out:
            writeTofile(str(soup.prettify()))
        if args.extract_urls:
            extract_urls(URL)
        if args.print:
            print(soup.prettify())

    else:
        print(response.status_code, " : ", response.content)

if __name__ == "__main__":
   myprog()

# BY EXCEPTIONAL
