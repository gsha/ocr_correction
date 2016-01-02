#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import xml.etree.cElementTree as ET
import xml.dom.minidom
import sys

buck2uni = {"'": "\u0621",  # hamza-on-the-line
            "|": "\u0622",  # madda
            ">": "\u0623",  # hamza-on-'alif
            "&": "\u0624",  # hamza-on-waaw
            "<": "\u0625",  # hamza-under-'alif
            "}": "\u0626",  # hamza-on-yaa'
            "A": "\u0627",  # bare 'alif
            "b": "\u0628",  # baa'
            "p": "\u0629",  # taa' marbuuTa
            "t": "\u062A",  # taa'
            "v": "\u062B",  # thaa'
            "j": "\u062C",  # jiim
            "H": "\u062D",  # Haa'
            "x": "\u062E",  # khaa'
            "d": "\u062F",  # daal
            "*": "\u0630",  # dhaal
            "r": "\u0631",  # raa'
            "z": "\u0632",  # zaay
            "s": "\u0633",  # siin
            "$": "\u0634",  # shiin
            "S": "\u0635",  # Saad
            "D": "\u0636",  # Daad
            "T": "\u0637",  # Taa'
            "Z": "\u0638",  # Zaa' (DHaa')
            "E": "\u0639",  # cayn
            "g": "\u063A",  # ghayn
            "_": "\u0640",  # taTwiil
            "f": "\u0641",  # faa'
            "q": "\u0642",  # qaaf
            "k": "\u0643",  # kaaf
            "l": "\u0644",  # laam
            "m": "\u0645",  # miim
            "n": "\u0646",  # nuun
            "h": "\u0647",  # haa'
            "w": "\u0648",  # waaw
            "Y": "\u0649",  # 'alif maqSuura
            "y": "\u064A",  # yaa'
            "F": "\u064B",  # fatHatayn
            "N": "\u064C",  # Dammatayn
            "K": "\u064D",  # kasratayn
            "a": "\u064E",  # fatHa
            "u": "\u064F",  # Damma
            "i": "\u0650",  # kasra
            "~": "\u0651",  # shaddah
            "o": "\u0652",  # sukuun
            "`": "\u0670",  # dagger 'alif
            "{": "\u0671",  # waSla
            }


def parse_line():
    line = f.readline()
    splitter = line.find(' ')
    if splitter==-1:
        line_header = line
        line_text = ""
    else:
        line_header = line[0:splitter]
        line_text = line[splitter + 1:len(line) - 1]
    title = line_header.split(':')
    if not len(title) == 3:
        return None
    header_type = title[0]
    tmp = title[1].split('.')
    newspaper = tmp[0]
    article_num = tmp[1]
    unicode_text = transliterate_str(line_text)
    return [header_type, newspaper, article_num, unicode_text]


def transliterate_str(inString):
    out = ""
    i = 0
    while i < len(inString):
        if inString[i] is '@':
            if inString[i: i + 7] == "@@LAT@@":
                j = inString.find(' ', i)
                if j is -1:
                    out = out + inString[i + 7: len(inString)]
                    break
                out = out + inString[i + 7: j]
                i = j
        out = out + buck2uni.get(inString[i], inString[i])
        i += 1

    return out


def handle_article(first_article_line):
    if first_article_line[0] == 'headline':
        doc = ET.SubElement(xml_root, "DOC", newspaper=first_article_line[1], article=first_article_line[2], id=first_article_line[1] + first_article_line[2])
        ET.SubElement(doc, "headline").text = first_article_line[3]
        next_line = parse_line()
        if next_line[0] == 'dateline':
            ET.SubElement(doc, "dateline").text = next_line[3]
            next_line = parse_line()
        text = ET.SubElement(doc, "text")
        while next_line and (next_line[0] == "p" or next_line[0]== "text"):
            ET.SubElement(text, "p").text = next_line[3]
            next_line = parse_line()
            if next_line and next_line[0] == "dateline":
                next_line = parse_line()
        return next_line
    else:
        next_line = parse_line()
        if next_line:
            return handle_article(next_line)
    return None


def usage():
    print("Usage:", sys.argv[0], "-i INFILE -o OUTDIR")


def main():
    if not len(sys.argv) == 3:
        usage()
        sys.exit(2)
    in_filepath = sys.argv[1]
    in_filename = os.path.basename(in_filepath)
    out_dir = sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    global f
    f = open(in_filepath, 'r')
    global xml_root
    xml_root = ET.Element("root")
    first_article_line = parse_line()
    while first_article_line:
        first_article_line = handle_article(first_article_line)

    tree = ET.ElementTree(xml_root)
    xml_outfile = os.path.join(out_dir, in_filename)
    tmp_xml_path = xml_outfile + ".tmp"
    tree.write(tmp_xml_path)

    xml_format = xml.dom.minidom.parseString(open(tmp_xml_path, "r+", encoding="utf-8").read())
    os.remove(tmp_xml_path)
    pretty_xml_as_string = xml_format.toprettyxml()
    pretty_xml_file = open(xml_outfile, "w+", encoding="utf-8")
    pretty_xml_file.write(pretty_xml_as_string)


if __name__ == "__main__":
    main()