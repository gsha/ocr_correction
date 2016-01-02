#!/usr/bin/env python
# -*- coding: utf-8 -*-




ENTITY_TEMPLATE = '''        <entity name="%s"
                processor="XPathEntityProcessor"
                stream="true"
                forEach="/root/DOC/"
                url="data\%s"
                transformer="RegexTransformer,DateFormatTransformer"
                >
            <field column="id"        xpath="/root/DOC/@id" />
            <field column="newspaper"        xpath="/root/DOC/@newspaper" />
            <field column="article"        xpath="/root/DOC/@article" />
            <field column="title"     xpath="/root/DOC/headline" />
            <field column="text"    xpath="/root/DOC/text/p" />
       </entity>'''


def main():
    filenames = open("filenames.txt", 'r').read().splitlines()
    for name in filenames:
        entity = ENTITY_TEMPLATE % (name.split('.')[0], name)
        print(entity)


if __name__ == "__main__":
    main()