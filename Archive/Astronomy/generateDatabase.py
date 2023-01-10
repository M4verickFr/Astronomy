# coding: utf-8

import sqlite3
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
                    table[name] = {
                        "name": name,
                        "galaxy": info[2:17].lstrip().rstrip(),
                        "date": info[19:29].lstrip().rstrip(),
                        "ra": ra_degree,
                        "decl": decl_degree,
                        "offset": info[46:56].lstrip().rstrip(),
                        "mag": info[57:65].lstrip().rstrip()
                    }
            except Exception as e:
                print(contents[i].attrs["name"] + " - " + str(e))
        i+=1

    return table

def create_database(table):
    db = sqlite3.connect(f'src/Astronomy/data/database.db')

    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS supernova")
    cursor.execute(""" 
        CREATE TABLE supernova (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            name TEXT,
            galaxy TEXT,
            date TEXT,
            ra TEXT,
            decl TEXT,
            offset TEXT,
            mag TEXT
        )
    """)
    
    for name, sn in table.items():
        db.execute("INSERT INTO supernova VALUES (null, :name, :galaxy, :date, :ra, :decl, :offset, :mag)", sn) 
        
    db.commit()
    db.close()

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

        