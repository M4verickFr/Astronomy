#!/usr/bin/env python

import time
#!/usr/bin/env python
import os

from pymongo import MongoClient

from operator import itemgetter

import sqlite3
import argparse
import requests
import json
from bs4 import BeautifulSoup




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
                if(name == "2015bh"):
                    print(True)
                if(name == lastName):
                    print(name)
                    break
                
                ra = info[31:38].lstrip().rstrip()
                decl = info[39:45].lstrip().rstrip()
                ra_split = ra.split()
                ra_degree = str(float(ra_split[0]) + float(ra_split[1])/60)
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
    #print(table)
    sn_list = []
    for name, sn in table.items():
        sn_list.append(sn)
    
    if(sn_list):
        sn_collection.insert_many(sn_list)

def export_json(table):
    with open('src/Astronomy/data/table.json', 'w') as fp:
        json.dump(table, fp, indent=4)


client = MongoClient("mongo:27017")
db = client.Spativis
sn_collection = db["supernovas"]


list_ex = list(sn_collection.find({},{"_id":0}))
lastName = ""
try:
    lastName = sorted(list_ex, key=lambda d: d['name'], reverse=True)[0]
except:
    ""
print(lastName)

create_database(parse_web())
    
