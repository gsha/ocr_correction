#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import xml.etree.cElementTree as ET
import sys


out_dir = r'C:\Progs\solr-5.0.0\solr-5.0.0\server\data\images\Al-Hayat\31'
relative_dir = os.path.dirname(out_dir)
for file in os.listdir(out_dir):
    if file.endswith(".xml") and file.startswith("HYT"):
        parser = ET.XMLParser(encoding="utf-8")
        tree = ET.parse(os.path.join(out_dir,file), parser=parser)
        root = tree.getroot()
        for doc in root:
            if os.path.exists(out_dir + '\\' + doc.attrib['article'][0:4] + '.tif'):
                output = open(os.path.join(out_dir,doc.attrib['article'] + '.xml'), 'ab')
                string = ET.tostring(doc,encoding='utf8')
                output.write(string)