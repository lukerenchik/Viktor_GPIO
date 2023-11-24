# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 17:00:14 2023
Updated on Sat Sep 9 23:11:00 2023
@author: Derek Joslin & Luke Renchik
"""

"""
TODO:
1.) Memories are going to need a keyword search to locate the relevant lines among large bodies of text



"""
import json

macGnome = '/Users/user/Documents/AIDev_Luke_WD/gnomes/ViktorTest.gnome'
piGnome = "/home/lukerenchik/Documents/AIDev_Luke/gnomes/ViktorTest.gnome"


def load_gnomes(gnomeFilePath):
    try:
        with open(gnomeFilePath, 'r') as gnome_json:
            gnomes = json.load(gnome_json)
            return gnomes
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        return None


class GnomeInterpreter:

    def __init__(self):
        self.keylist = []
        gnome_data = load_gnomes(macGnome)
        self.gnome_data = gnome_data
    

    def getGnome(self):
        return self.gnome_data

    def __getitem__(self, gnomeKey):
        return self.getGnome()

    def getGnomeKeys(self):
        return list(self.keylist)


if __name__ == "__main__":
    myGnome = GnomeInterpreter()
    print(myGnome.gnome_data["intro"])


