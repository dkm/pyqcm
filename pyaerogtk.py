#!/usr/bin/env python

## Copyright (C) 2006 Marc Poulhies <marc.poulhies@pouicpouic dot info>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published
## by the Free Software Foundation; version 2 only.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.


from pyqcm import XmlQCM
import pygtk
pygtk.require ('2.0')
import gtk.glade
import gtk.gdk
import gobject
import sys
import os

interface_file = "pyaero.glade"

class PyAeroGUI:
    def gtk_main_quit(self, widget):
        gtk.main_quit()

class PyAeroStartupGUI (PyAeroGUI):
    def __init__(self, qcmxml):
        self.qcmxml = qcmxml
        
        filename = os.path.join(os.path.dirname(__file__), interface_file)

        self.start_xml = gtk.glade.XML(filename, root="startup_window")

        self.startup_window = self.start_xml.get_widget("startup_window")
        self.spin_btn = self.start_xml.get_widget("nb_questions")
        self.chapter_table = self.start_xml.get_widget("chapter_table")

        self.qcm = XmlQCM(qcmxml)
        c_size = self.qcm.get_num_chapters()

        self.chapter_table.resize(c_size/2, 2)

        self.c_buttons = {}
        for i in range(1, c_size+1):
            btn = gtk.ToggleButton("%d" %i)
            btn.show()
            btn.set_active(True)
            self.c_buttons["%d" %i] = btn
            print "%d, %d, %d, %d" %(i%2, i%2+1, i/2, i/2+1)
            self.chapter_table.attach(btn, (i-1)%2, (i-1)%2+1, (i-1)/2, (i-1)/2+1)
            
        self.start_xml.signal_autoconnect(self)

    def on_start_button_clicked(self, widget):
        length = int(self.spin_btn.get_value())

        self.startup_window.destroy()
        chapters=[]

        for name,btn in self.c_buttons.items():
            if btn.get_active():
                chapters += [name]
                
        main_gui = PyAeroMainGUI(self.qcm, length, chapters=chapters)

class PyAeroMainGUI (PyAeroGUI):
    def __init__(self, qcm=None, length=30, start=True, chapters=[]):

        if isinstance(qcm, str):
            self.playing = True
            self.qcm = XmlQCM(qcm)
            self.length = -1
        elif isinstance(qcm, XmlQCM):
            self.playing = True
            self.qcm = qcm
            self.length = qcm.length
        elif isinstance(qcm, dict):
            self.playing = False
            self.qcm = qcm.items()
            self.length = len(qcm)
            start = False
        else:
            print "unknwon type: ", type(qcm)
            
        filename = os.path.join(os.path.dirname(__file__), interface_file)

        self.xml = gtk.glade.XML(filename, root="pymachin_window")
        self.xml.signal_autoconnect(self)

        self.main_window = self.xml.get_widget("pymachin_window")
        
        self.qbody_txtview = self.xml.get_widget("q_textview")

        self.labels = {}
        self.chkbox = {}

        self.qcount = 0
        self.score = 0
        self.qcurrent = None

        self.qfailed = {}
        
        self.qpossibilities = ['a', 'b', 'c', 'd']
		
        for name in self.qpossibilities:
            self.labels[name] = self.xml.get_widget("label_%s" %name)
            self.chkbox[name] = self.xml.get_widget("chkbtn_%s" %name)

        if self.playing:
            self.qcm.select(number=length, chapter=chapters)
            self.length = self.qcm.length
            if start:
                self.display_next_question()
        else:
            self.replayed_idx = 0
            self.replay_questions()

    def replay_questions(self):
        quest = self.qcm[self.replayed_idx]
        self.replayed_idx += 1
        self.display_question(quest[0], True)

        for name in quest[1]:
            self.chkbox[name].set_active(True)

        
        
    def display_question(self, question=None, displayScore=False):
        if question == None:
            question = self.qcurrent

        self.clear_answers()
        self.qbody_txtview.get_buffer().set_text(question.qbody)

        k = self.labels.keys()[:len(question.answers)]

        for idx,ans in question.answers.items():
            if displayScore:
                self.labels[idx].set_text("%s [%d]" %(ans[0], ans[1]))
            else:
                self.labels[idx].set_text(ans[0])
        

    def display_next_question(self):
        self.qcount += 1

        self.qcurrent = self.qcm.getNext()
        self.display_question()
        

    def clear_answers(self):
        for name in self.qpossibilities:
            self.labels[name].set_text("")
            self.chkbox[name].set_active(False)
        

    def on_ok_button_clicked(self, widget):
        if self.playing :
            if self.qcurrent != None:
                t_score = 0
                answered_idx = []
            
                for idx,ans in self.qcurrent.answers.items() :
                    if self.chkbox[idx].get_active():
                        t_score += ans[1]
                        answered_idx += [idx]
                    

                # negative score not possible. At most 6, at least 0 :)
                if t_score > 0:
                    self.score += t_score

                if t_score != 6 :
                    self.qfailed[self.qcurrent] = answered_idx

                if self.qcount != self.length:
                    self.display_next_question()
                else:
                    disp_score = PyAeroDisplayScore(self.score, self.qcount, self.qfailed)
                    self.main_window.destroy()

        else: ## not playing, replaying
            if self.replayed_idx != len(self.qcm):
                self.replay_questions()
            else:
                self.main_window.destroy()

class PyAeroDisplayScore (PyAeroGUI):
    def __init__(self, score, qcount, failed={}):
        self.score = score
        self.qcount = qcount
        self.failed = failed
        
        filename = os.path.join(os.path.dirname(__file__), interface_file)

        self.xml = gtk.glade.XML(filename, root="display_score_window")
        self.xml.signal_autoconnect(self)

        self.main_window = self.xml.get_widget("display_score_window")
        self.score_label_2 = self.xml.get_widget("score_label_2")

        success_score = (qcount * 6) * 3/4

        if score <= success_score:
            self.score_label_2.set_text(" failed with %d (min is %d) (%d questions)" %(score,
                                                                                       int(success_score),
                                                                                       qcount))
        else:
            self.score_label_2.set_text(" success with %d (min is %d) (%d questions)" %(score,
                                                                                        int(success_score),
                                                                                        qcount))

    def on_sumup_button_clicked(self, widget):
        if len(self.failed) > 0:
            p = PyAeroMainGUI(self.failed, len(self.failed), start=False)
        else:
            self.gtk_main_quit(widget)
    

q = PyAeroStartupGUI(sys.argv[1])
gtk.main()

