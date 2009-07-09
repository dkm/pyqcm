import sys
from lxml import etree


xml = etree.parse(sys.argv[1])
qroot = xml.getroot()


for question in qroot.findall("question"):
    print "[%s in chap %s]" %(question.attrib['id'], question.attrib['chapter'])
    print "%s " %question.find("body").text.strip()

    for ans in question.findall("answer"):
        print " * %s [%s]" %(ans.text.strip(), ans.attrib['score'])

    print ""


