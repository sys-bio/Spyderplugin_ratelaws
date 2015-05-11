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



from spyderlib.qt.QtGui import (QHBoxLayout, QWidget, QVBoxLayout,QLabel)
from spyderlib.qt.QtCore import QTextCodec
locale_codec = QTextCodec.codecForLocale()

import sys

#def is_helloworld_installed():
#    from spyderlib.utils.programs import is_module_installed
#    return is_module_installed('cProfile') and is_module_installed('pstats')


class HelloWorldWidget(QWidget):
    """
    HelloWorld widget
    """
    
    def __init__(self, parent, max_entries=100):
        """ Creates a very basic window with some text """
        
        HELLO_WORLD_MESSAGE = \
            "The Plugins for Spyder consists out of three main classes: \n\n" \
            "1. HelloWorld\n\n" \
            "\tThe HelloWorld class inherits all its methods from\n" \
            "\tSpyderPluginMixin and the HelloWorldWidget and performs all\n" \
            "\tthe processing required by the GUI. \n\n" \
            "2. HelloWorldConfigPage\n\n" \
            "\tThe HelloWorldConfig class inherits all its methods from\n" \
            "\tPluginConfigPage to create a configuration page that can be\n" \
            "\tfound under Tools -> Preferences\n\n" \
            "3. HelloWorldWidget\n\n" \
            "\tThe HelloWorldWidget class inherits all its methods from\n" \
            "\tQWidget to create the actual plugin GUI interface that \n" \
            "\tdisplays this message on screen\n\n"

        QWidget.__init__(self, parent)
        
        self.setWindowTitle("HelloWorld")
        
        self.output = None
        self.error_output = None
        
        self._last_wdir = None
        self._last_args = None
        self._last_pythonpath = None
        
        self.textlabel = QLabel(HELLO_WORLD_MESSAGE)        

        hlayout1 = QHBoxLayout()
        hlayout1.addWidget(self.textlabel)
        hlayout1.addStretch()
          
        layout = QVBoxLayout()
        layout.addLayout(hlayout1)
        self.setLayout(layout)
            

def test():
    """Run HelloWorld widget test"""
    from spyderlib.utils.qthelpers import qapplication
    app = qapplication()
    widget = HelloWorldWidget(None)
    widget.resize(400, 300)
    widget.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    test()