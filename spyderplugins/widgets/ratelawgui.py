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



from spyderlib.qt.QtGui import (QHBoxLayout, QListWidget, QStackedWidget, QSplitter,
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
        displaynamelist = []
        #displaylist = []
        infixlist = []
        desclist = []
        parameterstringlist = []
        xmldoc = minidom.parse('\\.spyder2\\ratelaw2_0_3.xml')
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
        #Adding displayName items to lawlist
        for j in range(i):
            item = QListWidgetItem(displaynamelist[j])      """Creates list entry for each rate law"""
            self.lawlist.addItem(item)                      """Adds rate law to list"""
            self.lawdetailpage = QWidget()                  """Creates page for each rate law"""
            # Page layout will become its own function
            setup_group = QGroupBox(displaynamelist[j])     """Creates box with rate law name as title"""
            infixmod = infixlist[j].replace("___"," ")      
            setup_label = QLabel(infixmod)
            setup_label.setWordWrap(True)                   """types rate law expression, removing underscores"""
            
            desc_group = QGroupBox("Description")           """creates box for description"""
            desc_label = QLabel(desclist[j])
            desc_label.setWordWrap(True)
            param_label = QLabel(parameterstringlist[j])
            param_label.setWordWrap(True)

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
            vlayout.addStretch(1)
            self.lawdetailpage.setLayout(vlayout)
            
            self.lawpage.addWidget(self.lawdetailpage)      """Formats the page shown when a rate law is selected"""
        
        #self.connect(self.lawlist, SIGNAL(self.lawlist.currentRowChanged(int)),self.lawpage,SLOT(self.lawpage.setCurrentIndex(int)))
        self.lawlist.currentRowChanged.connect(self.lawpage.setCurrentIndex)     """When a rate law in the list is clicked, its corresponding page is shown"""       
        '''
        self.lawpage = QWidget()
        '''
        self.lawlist.setCurrentRow(0)
        
        hsplitter = QSplitter()
        hsplitter.addWidget(self.lawlist)                   "Adds list to left side of window"
        
        
        
        
        hlayout1 = QHBoxLayout()
        hlayout1.addWidget(self.textlabel)
        hlayout1.addStretch()
        self.lawpage.setLayout(hlayout1)
        
        hsplitter.addWidget(self.lawpage)                   """Adds law page to left side of window"""
        
        layout = QVBoxLayout()
        layout.addWidget(hsplitter)
        self.setLayout(layout)
        
        
        
        
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