#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2009 Marc Poulhiès
#
# pyqcm
#
# Plopifier is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Plopifier is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Plopifier.  If not, see <http://www.gnu.org/licenses/>.


from lxml import etree
import random

class Question:
    def __init__(self, xmlcode=None):
        self.possibilities = ['a', 'b', 'c', 'd']
        
        if xmlcode == None:
            self.qbody = None
            self.chapter = None
            self.qid = None
            self.answers = None
        else:
            self.qbody = xmlcode.find("body").text.strip()
            self.qid = xmlcode.attrib['id']
##            self.chapter = xmlcode.attrib['chapter']
            ans =  xmlcode.findall("answer")
            self.answers = {}
            for i in range(len(ans)):
                self.answers[self.possibilities[i]] = (ans[i].text.strip(),
                                                       int(ans[i].attrib['score']))

    def display(self, showScore=False):
        s = "[#%s]" %self.qid
        
        s += self.qbody.encode("utf-8")
        s += "\n"
        for c,b in self.answers.items():
            s += " [%s] %s" %(c.encode("utf-8"),b[0].encode("utf-8"))
            if showScore:
                s += " [%d]" %b[1]
            s += "\n"
        
        return s

    def __str__(self):
        return self.display()

class XmlQCM:
    def __init__(self, filename, pickable=False):
        self.filename = filename

        self.pickable = pickable
        self.nchapter = None
        
        self.length = None
        self.selected = None
        self.s_generator = None

    def get_chapters(self):
        xml = etree.parse(self.filename)
        l = [(c.attrib['id'],c.attrib['name']) for c in xml.getroot().xpath("//chapter")]
        self.nchapter = len(l)
        return l

    def get_num_chapters(self):
        if self.nchapter != None:
            return self.nchapter
        else:
            xml = etree.parse(self.filename)
            return len(xml.getroot().xpath("//chapter"))

    def get_brevets(self):
        ##xml = etree.parse(self.filename)
        ## this should be dynamic, but a bit too much for my little server.
        return [('init', u'initial'), ('pilote', u'pilote'), ('conf', u'confirmé')]

    def select(self, number=30, chapters=None, brevets=None):
        # change .findall() by correct .xpath() expression.
        #self.selected = random.sample(self.root.findall("question"), number)
        xml = etree.parse(self.filename)
        root = xml.getroot()

        if chapters != None and brevets != None :
            seqchap = ["@id='%s'" %c for c in chapters]
            seqbrev = ["@type='%s'" %c for c in brevets]
            temp = root.xpath("//chapter[%s]/brevet[%s]/question" %(" or ".join(seqchap),
                                                                    " or ".join(seqbrev)))
        elif chapters != None and brevets == None :
            seqbrev = ["@type='%s'" %c for c in brevets]
            temp = root.xpath("//brevet[%s]/question" %" or ".join(seqbrev))
        elif chapters == None and brevets != None:
            seq = ["@id='%s'" %c for c in chapters]
            temp = root.xpath("//chapter[%s]//question" %" or ".join(seq))
        elif chapters == None and brevets == None:
            temp = root.xpath("//question")

#         if chapters == None:
#             temp = root.xpath("//question")
#         else:
#             seq = ["@id='%s'" %c for c in chapters]
#             temp = root.xpath("//chapter[%s]//question" %" or ".join(seq))

        if len(temp) < number:
            number = len(temp)

        self.length = number
        self.selected = random.sample(temp, number)
        
        if self.pickable:
            self.selected = [Question(p) for p in self.selected]
        else:
            self.s_generator = self._getNext()

    def _getNext(self):
        for q in self.selected:
            yield Question(q)
        
    def getNext(self):
        if self.pickable:
            if len(self.selected) != 0:
                return self.selected.pop()
            else:
                return None
        else:
            return self.s_generator.next()
