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



from spyderlib.qt.QtGui import (QPushButton, QHBoxLayout, QListWidget, QStackedWidget, QSplitter,
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
        """ Creates a very basic window with some text """
        """
        RATE_LAW_MESSAGE = \
            "The Plugins for Spyder consists out of three main classes: \n\n" \
            "1. HelloWorld\n\n" \
            "\tThe HelloWorld class inherits all its methods from\n" \
            "\tSpyderPluginMixin and the HelloWorldWidget and performs all\n" \
            "\tthe processing required by the GU. \n\n" \
            "2. HelloWorldConfigPage\n\n" \
            "\tThe HelloWorldConfig class inherits all its methods from\n" \
            "\tPluginConfigPage to create a configuration page that can be\n" \
            "\tfound under Tools -> Preferences\n\n" \
            "3. HelloWorldWidget\n\n" \
            "\tThe HelloWorldWidget class inherits all its methods from\n" \
            "\tQWidget to create the actual plugin GUI interface that \n" \
            "\tdisplays this message on screen\n\n"
        """
        #Testing access editor on plugin initialization
        
        
        RATE_LAW_MESSAGE = ""
        h = 0
        testtext = ""
        foo = ""
        displaynamelist = []
        #displaylist = []
        infixmod = []
        infixlist = []
        desclist = []
        parameterstringlist = []
        buttonlist  = []
        xmldoc = minidom.parse('C:\\Users\\Jayit\\.spyder2\\ratelaw2_0_3.xml')
        #xmldoc = minidom.parse('%\\Downloads\\ratelaw2_0_3.xml')
        
        lawlistxml = xmldoc.getElementsByTagName('law')
        #i is the number of laws currently in the xml file
        i = 0
        
        """
        Parsing xml: Acquiring rate law name, description, and list of parameter information
        """
        for s in lawlistxml:
            #RATE_LAW_MESSAGE += s.getAttribute('displayName') + "\n"
            RATE_LAW_MESSAGE += s.getAttribute('display') + "\n"
            #displaynamelist[i] = s.getAttribute('displayName')
            #displaylist[i] = s.getAttribute('display')
            displaynamelist.append(s.getAttribute('displayName'))
            #displaylist.append(s.getAttribute('display'))
            infixlist.append(s.getAttribute('infixExpression'))
            desclist.append(s.getAttribute('description'))
            parameterlist = s.getElementsByTagName('listOfParameters')[0]
            #for p in parameterlist    
            parameters = parameterlist.getElementsByTagName('parameter')
            parameterstring = ""
            for param in parameters:
                parametername = param.attributes['name'].value
                parameterdesc = param.attributes['description'].value
                parameterstring = parameterstring + '\t' + parametername + ":" + '\t' + "  " + parameterdesc + "\n"
                """Creates "description" string"""
                #print('\t' + parametername + ":" + '\t' + parameterdesc)
            parameterstringlist.append(parameterstring)    
            i = i + 1
            
        
        QWidget.__init__(self, parent)
        
        self.setWindowTitle("Rate Law Library")
        
        self.output = None
        self.error_output = None
        
        self._last_wdir = None
        self._last_args = None
        self._last_pythonpath = None
        
        self.textlabel = QLabel(RATE_LAW_MESSAGE)
        
        
        

        self.lawlist = QListWidget()
        self.lawpage = QStackedWidget()
        index = 0
        #Adding displayName items to lawlist
        for j in range(i):
            item = QListWidgetItem(displaynamelist[j])
            self.lawlist.addItem(item)
            self.lawdetailpage = QWidget()
            # Page layout will become its own function
            setup_group = QGroupBox(displaynamelist[j])
            #infixmod = infixlist[j].replace("___"," ")      
            #setup_label = QLabel(infixmod)
            infixmod.append(infixlist[j].replace("___"," "))      
            setup_label = QLabel(infixmod[j])
            setup_label.setWordWrap(True)
            
            desc_group = QGroupBox("Description")
            desc_label = QLabel(desclist[j])
            desc_label.setWordWrap(True)
            param_label = QLabel(parameterstringlist[j])
            param_label.setWordWrap(True)
            
            #self.button = QPushButton(self)
            #self.button.setText("Insert rate law")
            #self.button.setText("button %s" % j )
            #self.button.clicked.connect(lambda: self.insertText(infixmod[index]))
            
            
            self.button = QPushButton(self)
            buttonlist.append(self.button)
            buttonlist[j].setText("button for rate law %s" % j)
            testtext = infixmod[j]
            #buttonlist[j].clicked.connect(lambda: self.insertText(testtext))
            
            
        # Warning: do not try to regroup the following QLabel contents with 
        # widgets above -- this string was isolated here in a single QLabel
        # on purpose: to fix Issue 863
            setup_layout = QVBoxLayout()
            setup_layout.addWidget(setup_label)
            setup_group.setLayout(setup_layout)
            
            desc_layout = QVBoxLayout()
            desc_layout.addWidget(desc_label)
            desc_layout.addWidget(param_label)
            desc_group.setLayout(desc_layout)

            vlayout = QVBoxLayout()
            vlayout.addWidget(setup_group)
            vlayout.addWidget(desc_group)
            #vlayout.addWidget(self.button)
            vlayout.addWidget(buttonlist[j])
            vlayout.addStretch(1)
            self.lawdetailpage.setLayout(vlayout)
            
            
            #self.button.clicked.connect(lambda: self.insertText(infixmod[j]))
            
            self.lawpage.addWidget(self.lawdetailpage)
        
        #self.connect(self.lawlist, SIGNAL(self.lawlist.currentRowChanged(int)),self.lawpage,SLOT(self.lawpage.setCurrentIndex(int)))
        
        #for h in range(i):
        #    foo = h 
        #    buttonlist[h].clicked.connect(lambda: self.insertText("text for button %s" % h))
        
        #for h,infix in enumerate(infixmod):
        #    buttonlist[h].clicked.connect(lambda: self.pressbutton(infix))
        
        
        buttonlist[0].clicked.connect(lambda: self.insertText(infixmod[0]))
        buttonlist[1].clicked.connect(lambda: self.insertText(infixmod[1]))
        buttonlist[2].clicked.connect(lambda: self.insertText(infixmod[2]))
        buttonlist[3].clicked.connect(lambda: self.insertText(infixmod[3]))
        buttonlist[4].clicked.connect(lambda: self.insertText(infixmod[4]))
        buttonlist[5].clicked.connect(lambda: self.insertText(infixmod[5]))
        buttonlist[6].clicked.connect(lambda: self.insertText(infixmod[6]))
        buttonlist[7].clicked.connect(lambda: self.insertText(infixmod[7]))
        buttonlist[8].clicked.connect(lambda: self.insertText(infixmod[8]))
        buttonlist[9].clicked.connect(lambda: self.insertText(infixmod[9]))
        
        buttonlist[10].clicked.connect(lambda: self.insertText(infixmod[10]))
        buttonlist[11].clicked.connect(lambda: self.insertText(infixmod[11]))
        buttonlist[12].clicked.connect(lambda: self.insertText(infixmod[12]))
        buttonlist[13].clicked.connect(lambda: self.insertText(infixmod[13]))
        buttonlist[14].clicked.connect(lambda: self.insertText(infixmod[14]))
        buttonlist[15].clicked.connect(lambda: self.insertText(infixmod[15]))
        buttonlist[16].clicked.connect(lambda: self.insertText(infixmod[16]))
        buttonlist[17].clicked.connect(lambda: self.insertText(infixmod[17]))
        buttonlist[18].clicked.connect(lambda: self.insertText(infixmod[18]))
        buttonlist[19].clicked.connect(lambda: self.insertText(infixmod[19]))
        
        buttonlist[20].clicked.connect(lambda: self.insertText(infixmod[20]))
        buttonlist[21].clicked.connect(lambda: self.insertText(infixmod[21]))
        buttonlist[22].clicked.connect(lambda: self.insertText(infixmod[22]))
        buttonlist[23].clicked.connect(lambda: self.insertText(infixmod[23]))
        buttonlist[24].clicked.connect(lambda: self.insertText(infixmod[24]))
        buttonlist[25].clicked.connect(lambda: self.insertText(infixmod[25]))
        buttonlist[26].clicked.connect(lambda: self.insertText(infixmod[26]))
        buttonlist[27].clicked.connect(lambda: self.insertText(infixmod[27]))
        buttonlist[28].clicked.connect(lambda: self.insertText(infixmod[28]))
        buttonlist[29].clicked.connect(lambda: self.insertText(infixmod[29]))
        
        buttonlist[30].clicked.connect(lambda: self.insertText(infixmod[30]))
        buttonlist[31].clicked.connect(lambda: self.insertText(infixmod[31]))
        buttonlist[32].clicked.connect(lambda: self.insertText(infixmod[32]))
        buttonlist[33].clicked.connect(lambda: self.insertText(infixmod[33]))
        buttonlist[34].clicked.connect(lambda: self.insertText(infixmod[34]))
        buttonlist[35].clicked.connect(lambda: self.insertText(infixmod[35]))
        buttonlist[36].clicked.connect(lambda: self.insertText(infixmod[36]))
        buttonlist[37].clicked.connect(lambda: self.insertText(infixmod[37]))
        buttonlist[38].clicked.connect(lambda: self.insertText(infixmod[38]))
        buttonlist[39].clicked.connect(lambda: self.insertText(infixmod[39]))
        
        buttonlist[40].clicked.connect(lambda: self.insertText(infixmod[40]))
        buttonlist[41].clicked.connect(lambda: self.insertText(infixmod[41]))
        buttonlist[42].clicked.connect(lambda: self.insertText(infixmod[42]))
        buttonlist[43].clicked.connect(lambda: self.insertText(infixmod[43]))
        buttonlist[44].clicked.connect(lambda: self.insertText(infixmod[44]))
        buttonlist[45].clicked.connect(lambda: self.insertText(infixmod[45]))
        buttonlist[46].clicked.connect(lambda: self.insertText(infixmod[46]))
        
            
            
        self.lawlist.currentRowChanged.connect(self.lawpage.setCurrentIndex)
        #h = self.lawlist.currentRow
        
        '''
        self.lawpage = QWidget()
        '''
        self.lawlist.setCurrentRow(0)
        
        hsplitter = QSplitter()
        hsplitter.addWidget(self.lawlist)
        
        
        
        '''
        hlayout1 = QHBoxLayout()
        hlayout1.addWidget(self.textlabel)
        hlayout1.addStretch()
        self.lawpage.setLayout(hlayout1)
        '''
        hsplitter.addWidget(self.lawpage)
        
        layout = QVBoxLayout()
        layout.addWidget(hsplitter)
        self.setLayout(layout)
        
    #def insertText(self):
    #    print(self.main.editor.get_current_editor().insert_text('string'))    
        
        
'''        
def create_law_page(displayname,display):
    setup_group = QGroupBox(_(displayname))
    setup_label = QLabel(_(display))
    setup_label.setWordWrap(True)

        # Warning: do not try to regroup the following QLabel contents with 
        # widgets above -- this string was isolated here in a single QLabel
        # on purpose: to fix Issue 863
    setup_layout = QVBoxLayout()
    setup_layout.addWidget(setup_label)
    setup_group.setLayout(setup_layout)

    vlayout = QVBoxLayout()
    vlayout.addWidget(setup_group)
    vlayout.addStretch(1)
    self.setLayout(vlayout)
'''            
#def pressbutton(string):
#    self.insertText(string)

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