#!/usr/bin/python3
import requests as re
from bs4 import BeautifulSoup
import argparse
import os
import pyinputplus as pyip
import sys
import time


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

                                                                                               -By 3XCEPTIONAL             
                                                                                                            """


print(BANNER)


USAGE = """

 Download Source page
 extract links  
"""



parser = argparse.ArgumentParser(USAGE)
parser.add_argument('-u', '--url',  type=str,metavar="", required=True,
                    help='example = https://www.example.com')
parser.add_argument('-o', '--out',required=False, action='store_true',
                    help='Save web page to file : example.html')

parser.add_argument('-p', '--print', required=False, action='store_true'
                    )
parser.add_argument('-x', '--extract_urls', required=False, action='store_true'
                    )




args = parser.parse_args()



URL = args.url
def defaultFileName():
    remove_chars = ["", "http:", "https:"]
    final_url = ""
    url = str(URL).split('/')
    for i in url:
        if i in remove_chars:
            url.remove(i)

    for ele in url:
        final_url += f"{ele}_"

    return final_url

OUTPUT_FILE = defaultFileName()

response = re.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')



def writeTofile(content):
    if os.path.exists(OUTPUT_FILE):
        promptMSG = f"File ({OUTPUT_FILE}) already exists \n would you like to overWrite? (ans 1 or 2)?\n 1 = yes\n 2 = no"
        option = pyip.inputChoice(
            prompt=promptMSG, choices=['1', '2'])
        print("\nSelected Option: " + option)
        if option == '1':
            print(f"File ({OUTPUT_FILE}) over Written!!")
            with open(OUTPUT_FILE, 'w')as f:
                f.write(content)
            print(OUTPUT_FILE, "Created successfully")
        else:
            print("\nMSG: No Changes made to file ",OUTPUT_FILE)
    else:
        with open(OUTPUT_FILE, 'w')as f:
            f.write(content)
        print(OUTPUT_FILE, "Created successfully")


def overWrite():
    """
    Overwrite a file Option
    Returns option
    """
    promptMSG = f"Would you like to overwrite the existing File (ans 1 or 2)?\n 1 = yes\n 2 = no "
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
            # print(url)
            f.write(url)


def extract_urls(filename):
    default_filename = f"EXTRACTED_URLS_{defaultFileName()}.txt"
    # filename = pyip.inputFilename(prompt="FILE NAME FOR EXTRACTED Urls?",blank=True)
    # if filename == "":
    #     filename = default_filename
    filename = default_filename
    if os.path.exists(filename):
        print(f"\n{filename} Exists")
        option = overWrite()
        if option == "1":
            print (filename,": Overwritten")
            writeURLS(filename)
        else: 
            print(f"No Changes made to {filename}")
    else:
        writeURLS(filename)
        print(filename, "Created successfully")

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

# BY 3XCEPTIONAL
