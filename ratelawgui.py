# -*- coding: utf-8 -*-
from __future__ import with_statement
"""
Created on Sun Apr 19 18:12:51 2015

@author: Jayit
"""

"""
HelloWorld widget

    - Basic implementation of a GUI for the Hello World plugin
"""



from spyderlib.qt.QtGui import (QLineEdit, QGridLayout, QPushButton, QHBoxLayout, QListWidget, QStackedWidget, QSplitter,
                                QWidget, QVBoxLayout,QLabel,QScrollArea,QListWidgetItem,QGroupBox)
from spyderlib.qt.QtCore import *
from xml.dom import minidom
locale_codec = QTextCodec.codecForLocale()
import os
import sys

#For accessing editor
from spyderlib.plugins import SpyderPluginWidget


#def is_helloworld_installed():
#    from spyderlib.utils.programs import is_module_installed
#    return is_module_installed('cProfile') and is_module_installed('pstats')


class RateLawWidget(QWidget):
    """
    Rate Law widget
    """
    
    def __init__(self, parent, max_entries=100):
        
        "Initialize Various list objects before assignment"
        displaylist = []
        displaynamelist = []
        infixmod = []
        infixlist = []
        desclist = []
        
        parameternamelist = []
        parameterdesclist = []
        parameterstringlist = []
        paramcountlist = []
        
        
        
        buttonlist  = []
        xmldoc = minidom.parse('C:\\Users\\Jayit\\.spyder2\\ratelaw2_0_3.xml')
        #xmldoc = minidom.parse('%\\Downloads\\ratelaw2_0_3.xml')
        
        lawlistxml = xmldoc.getElementsByTagName('law')
        
        o = 0
        for s in lawlistxml:
            o = o + 1
        
        parameternamelistlist = [0 for x in range(o)]
        parameterdesclistlist = [0 for x in range(o)]
        
        """i is the number of laws currently in the xml file"""
        i = 0
        
        """
        Parsing xml: Acquiring rate law name, description, and list of parameter information
        """
        for s in lawlistxml:
            #RATE_LAW_MESSAGE += s.getAttribute('displayName') + "\n"
            """Gets Latec Expression"""
            displaylist.append(s.getAttribute('display'))
            
            """Gets Rate-Law Name"""
            displaynamelist.append(s.getAttribute('displayName'))
            
            """"Gets Raw Rate-Law expression"""
            infixlist.append(s.getAttribute('infixExpression'))
            
            """Gets description statement"""
            desclist.append(s.getAttribute('description'))
            
            """Gets listOfParameters Object"""
            parameterlist = s.getElementsByTagName('listOfParameters')[0]
            
            """Gets a list of parameters within ListOfParameters object"""    
            parameters = parameterlist.getElementsByTagName('parameter')
            
            for param in parameters:
                parameternamelist.append(param.attributes['name'].value)
                #print(param.attributes['name'].value)
                parameterdesclist.append(param.attributes['description'].value)  
            
            parameternamelistlist[i] = parameternamelist
            #print("break")
            parameterdesclistlist[i] = parameterdesclist
            
            parameternamelist = []
            parameterdesclist = []
            i = i + 1
        
        SLElistlist = [ 0 for x in range(i)]
        PLElistlist = [ 0 for x in range(i)]
        ILElistlist = [ 0 for x in range(i)]
        paramLElistlist = [ 0 for x in range(i)]
        numlistlist = [ 0 for x in range(i)]
        
        QWidget.__init__(self, parent)
        
        self.setWindowTitle("Rate Law Library")
        
        self.output = None
        self.error_output = None
        self._last_wdir = None
        self._last_args = None
        self._last_pythonpath = None
        
        #self.textlabel = QLabel(RATE_LAW_MESSAGE)
        
        self.lawlist = QListWidget()
        self.lawpage = QStackedWidget()
        index = 0
        for j in range(i):            
            item = QListWidgetItem(displaynamelist[j])
            self.lawlist.addItem(item)
            self.lawdetailpage = QWidget()
            setup_group = QGroupBox(displaynamelist[j])
            infixmod.append(infixlist[j].replace("___"," "))      
            setup_label = QLabel(infixmod[j])
            setup_label.setWordWrap(True)
            
            desc_group = QGroupBox("Description")
            desc_label = QLabel(desclist[j])
            desc_label.setWordWrap(True)
                        
            param_label = QGridLayout()
            nm = QLabel("Name:")
            des = QLabel("Description:")
            repl = QLabel("Replace with:")
            param_label.addWidget(nm,0,0)
            param_label.addWidget(des,0,1)
            param_label.addWidget(repl,0,2)
            """g is the total number of alterable values"""
            g = 0
            """t is the total number of alterable non-parameters"""
            t = 1
            
            snum = 0
            pnum = 0
            inum = 0
            
            """range of N is the max number of possible substrates OR products"""
            N = 5
            for n in range(N):
                nl = n+1
                if (infixmod[j].find('S%s' % nl) > -1):
                    z = QLabel('S%s is present' % nl)
                    param_label.addWidget(z,t,0)
                    snum = snum + 1
                    t = t + 1
            
            for n in range(N):
                nl = n+1    
                if (infixmod[j].find('P%s' % nl) > -1):
                    z = QLabel('P%s is present' % nl)
                    param_label.addWidget(z,t,0)
                    pnum = pnum + 1
                    t = t + 1
                    
            for n in range(N):
                nl = n+1
                if (infixmod[j].find('I%s' % nl) > -1):
                    z = QLabel('I%s is present' % nl)
                    param_label.addWidget(z,t,0)
                    inum = inum + 1
                    t = t + 1
            
            """Initialize lists of list of parameter lineedit"""    
            length = len(parameternamelistlist[j])
            for b in range(length):
                p = QLabel("%s :" % parameternamelistlist[j][b])
                param_label.addWidget(p,b+t,0)
                d = QLabel("'%s'" % parameterdesclistlist[j][b])
                param_label.addWidget(d,b+t,1)
            
            g = t + length
            
            Slineeditlist = [0 for x in range(snum)]
            Plineeditlist = [0 for x in range(pnum)]
            Ilineeditlist = [0 for x in range(inum)]
            paramlineeditlist = [0 for x in range(length)]
            
            editcount = 1
            
            """Place lineedit widgets for parameters"""
            for s in range(snum):
                Slineeditlist[s] = QLineEdit()
                param_label.addWidget(Slineeditlist[s],editcount,2)
                editcount = editcount + 1
            
            SLElistlist[j] = Slineeditlist
            
            for s in range(pnum):
                Plineeditlist[s] = QLineEdit()
                param_label.addWidget(Plineeditlist[s],editcount,2)
                editcount = editcount + 1
            
            PLElistlist[j] = Plineeditlist
            
            for s in range(inum):
                Ilineeditlist[s] = QLineEdit()
                param_label.addWidget(Ilineeditlist[s],editcount,2)
                editcount = editcount + 1
               
            ILElistlist[j] = Ilineeditlist   
            
            for s in range(length):
                paramlineeditlist[s] = QLineEdit()
                param_label.addWidget(paramlineeditlist[s],editcount,2)
                editcount = editcount + 1
            
            paramLElistlist[j] = paramlineeditlist
            
            """Necessary lists for editable parameters. Housekeeping essentially."""
            stuff = paramlineeditlist[0].text()            
            numlistlist[j] = [snum, pnum, inum, length]
            charlist = ["S","P","I"]
            
            
            
            buttonlist.append(QPushButton(self))
            buttonlist[j].setText("Insert Rate Law: %s" % displaynamelist[j])
            
            
        # Warning: do not try to regroup the following QLabel contents with 
        # widgets above -- this string was isolated here in a single QLabel
        # on purpose: to fix Issue 863
            """Page formatting"""
            setup_layout = QVBoxLayout()
            setup_layout.addWidget(setup_label)
            setup_group.setLayout(setup_layout)
           
            desc_group.setLayout(param_label)
            
            vlayout = QVBoxLayout()
            vlayout.addWidget(setup_group)
            vlayout.addWidget(desc_group)
            vlayout.addWidget(buttonlist[j])
            vlayout.addStretch(1)
            self.lawdetailpage.setLayout(vlayout)
            self.lawpage.addWidget(self.lawdetailpage)
        
        """Set up button functionality"""
        for k in range(47):
            buttonlist[k].clicked.connect(pressbutton(self, infixmod[k], SLElistlist[k], PLElistlist[k],ILElistlist[k], paramLElistlist[k], parameternamelistlist[k], numlistlist[k], charlist,k))
            
        self.lawlist.currentRowChanged.connect(self.lawpage.setCurrentIndex)
        self.lawlist.setCurrentRow(0)
        
        
        """Set up high-level widget formatting."""
        hsplitter = QSplitter()
        hsplitter.addWidget(self.lawlist)
        hsplitter.addWidget(self.lawpage)
        
        layout = QVBoxLayout()
        layout.addWidget(hsplitter)
        self.setLayout(layout)
  
"""Testing LineEdit functionality"""    
def entertext(self, le, string, stringlist):
    
    def entertextreal():
        stuff = self.le.text()
        string = "%s" % stuff
        stringlist[0].replace("vo","%s" % string)
    
    return entertextreal    
    
"""Analyze lineedits on page, replace appropriate text, then paste text in console"""
def pressbutton(ratelaw, string, SLElist, PLElist, ILElist, paramLElist, paramlist, numlist,charlist,j):
    
    def pressbuttoninsert():
        print(string)
        stringmod = string
        for k in range(4):
            
            #print(stringmod)    
            for i in range(numlist[k]):
                print(str(numlist[k]))
                l = i + 1
                if (k == 0):
                    stuff = SLElist[i].text()
                    if (stuff.find(" ") != -1 or stuff.find('"') != -1):
                        pass
                    elif (stuff == ""):
                        pass
                    else:
                        stringmod = stringmod.replace(charlist[k] + str(l),"%s" % stuff)
                    print(stringmod)
                if (k == 1):
                    stuff = PLElist[i].text()
                    if (stuff.find(" ") != -1 or stuff.find('"') != -1):
                        pass
                    elif (stuff == ""):
                        pass
                    else:
                        stringmod = stringmod.replace(charlist[k] + str(l),"%s" % stuff)
                    print(stringmod)
                if (k == 2):
                    stuff = ILElist[i].text()
                    if (stuff.find(" ") != -1 or stuff.find('"') != -1):
                        pass
                    elif (stuff == ""):
                        pass
                    else:
                        stringmod = stringmod.replace(charlist[k] + str(l),"%s" % stuff)
                    print(stringmod)
                if (k == 3):
                    stuff = paramLElist[i].text()
                    if (stuff.find(" ") != -1 or stuff.find('"') != -1):
                        pass
                    elif (stuff == ""):
                        pass
                    else:
                        stringmod = stringmod.replace(paramlist[i],"%s" % stuff)
                    print(stringmod)
        print stringmod
        ratelaw.insertText(stringmod)
        
    return pressbuttoninsert

def test():
    """Run RateLaw widget test"""
    from spyderlib.utils.qthelpers import qapplication
    app = qapplication()
    widget = RateLawWidget(None)
    widget.resize(400, 300)
    widget.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    test()