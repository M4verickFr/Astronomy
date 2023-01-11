#!/usr/bin/env python

import os

from pymongo import MongoClient
import argparse
import requests
import json
from bs4 import BeautifulSoup

def parse_args():
    parser = argparse.ArgumentParser(description='Description')
    parser.add_argument('-c','--create', help='Description', required=False)
    parser.add_argument('-g','--get', help='Description', required=False)
    args = vars(parser.parse_args())
    return args

def parse_web():
    response = requests.get("http://www.cbat.eps.harvard.edu/lists/Supernovae.html")
    soup = BeautifulSoup(response.text, 'html.parser')
    contents = soup.find("pre").contents

    table = {}

    i = 1
    while (i < len(contents)):
        if (contents[i].name == "a" and contents[i].has_attr("name")):
            try:
                name = contents[i].attrs["name"]
                info = contents[i+1]

                ra = info[31:38].lstrip().rstrip()
                decl = info[39:45].lstrip().rstrip()

                ra_degree = str(sum(float(x)/(60^idx) for idx, x in enumerate(ra.split())))
                decl_degree = str(float(decl.split()[0]) + sum(float(x)/(60^idx) for idx, x in enumerate(decl.split()[1:])))

                if (ra != "" and decl != ""):
                    ra_list = ra.split()
                    decl_list = decl.split()
                    ra_new_list = f"{ra_list[0]}+{ra_list[1]}"
                    decl_new_list = f"{decl_list[0]}+{decl_list[1]}"
                    url = f'https://archive.stsci.edu/cgi-bin/dss_search?v=3&r={ra_new_list}&d={decl_new_list}&h=10&w=10'

                    table[name] = {
                        "name": name,
                        "galaxy": info[2:17].lstrip().rstrip(),
                        "date": info[19:29].lstrip().rstrip(),
                        "ra": ra_degree,
                        "decl": decl_degree,
                        "offset": info[46:56].lstrip().rstrip(),
                        "mag": info[57:65].lstrip().rstrip(),
                        "url": url
                    }
            except Exception as e:
                print(contents[i].attrs["name"] + " - " + str(e))
        i+=1

    return table

def create_database(table):
    client = MongoClient("mongo:27017")
    db = client.Spativis
    sn_collection = db["supernovas"]

    sn_list = []
    for name, sn in table.items():
        sn_list.append(sn)
    
    sn_collection.insert_many(sn_list)

def export_json(table):
    with open('src/Astronomy/data/table.json', 'w') as fp:
        json.dump(table, fp, indent=4)


if __name__ == "__main__":
    args = parse_args()

    if (args["create"] != None): 
        table = parse_web()
        create_database(table)
        
        if (args["create"] == "json"):
            export_json(table)



create_database(parse_web())
