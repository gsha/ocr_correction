#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import xml.etree.cElementTree as ET
import xml.dom.minidom
import sys

def usage():
    print("Usage:", sys.argv[0], "-i INFILE -o OUTDIR")


def main():
    if not len(sys.argv) == 2:
        usage()
        sys.exit(2)
    out_dir = os.path.dirname(sys.argv[1])
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()
    for doc in root:
        output = open(os.path.join(out_dir,doc.attrib['newspaper'] + '.xml'), 'ab')
        string = ET.tostring(doc,encoding='utf8')
        output.write(string)


    # global xml_root
    # xml_root = ET.Element("root")
    # first_article_line = parse_line()
    # while first_article_line:
    #     first_article_line = handle_article(first_article_line)
    #
    # tree = ET.ElementTree(xml_root)
    # xml_outfile =
    # tmp_xml_path = xml_outfile + ".tmp"
    # tree.write(tmp_xml_path)
    #
    # xml_format = xml.dom.minidom.parseString(open(tmp_xml_path, "r+", encoding="utf-8").read())
    # os.remove(tmp_xml_path)
    # pretty_xml_as_string = xml_format.toprettyxml()
    # pretty_xml_file = open(xml_outfile, "w+", encoding="utf-8")
    # pretty_xml_file.write(pretty_xml_as_string)


if __name__ == "__main__":
    main()