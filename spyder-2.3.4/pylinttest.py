# -*- coding: utf-8 -*-
"""
Created on Sun May 03 20:58:06 2015

@author: Jayit
"""
import sys
import os
import os.path as osp
import time
import re
import subprocess
from spyderlib.utils import programs

PYLINT_PATH = programs.find_program('\\python-2.7.9\\Scripts\\pylint')
print(PYLINT_PATH)