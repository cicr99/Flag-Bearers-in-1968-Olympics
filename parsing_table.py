from tableParser import *
from bs4 import BeautifulSoup
import pandas as pd
import os, re
import json


def valid(title):
    if len(title) == 2:
        return title[0] == 'wikitable' and title[1] == 'sortable'
    return False

def get_country(line):
    match = re.match(r'List of flag bearers for (.*) at the Olympics - Wikipedia', line, re.M|re.I)
    if match:
       return match.group(1)
    
    match = re.match(r'(.*) at the Olympics - Wikipedia', line, re.M|re.I)
    if match:
        return match.group(1)
    
    return line



def main():
    files = [name for name in os.listdir('./bearers')]
    path = 'bearers/'

    dic = {}
    broken = []

    for file_name in files:
        with open(path + file_name, 'r') as fd:
            html_doc = fd.read()

        html_doc = BeautifulSoup(html_doc, 'html.parser')
        country = get_country(html_doc.title.string)

        html_tables = html_doc.find_all('table')

        parser = HTMLTableParser()
        for table in html_tables:
            if valid(table['class']):
                t = parser.parse_html_table(table)
                idx = 0
                try:
                    years = t['Event year']
                    for year in years:
                        if year == 1968:
                            break
                        idx += 1
                    else:
                        break
                    dic[country] = {}
                    for col in t:
                        dic[country][col] = t[col][idx]
                
                except KeyError:
                    broken.append(country)
    with open('raw_data.json', 'w') as fd:
        fd.write(json.dumps(dic, indent=4, ensure_ascii=False))
    with open('bad_data.json', 'w') as fd:
       fd.write(json.dumps(broken, indent=4, ensure_ascii=False))



if __name__ == "__main__":
    main()