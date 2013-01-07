#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from morph import MorphDict 
import re
import codecs
import sys

ru = MorphDict()

with codecs.open('test.txt', 'r' , "utf-8") as test:
    for line in test:
        for splt in line.split():
            words = re.findall(r'\w+|\W+',splt,flags=re.U)
            for i in range(0, len(words), 2):
                words[i]=ru.replace(words[i].encode('utf-8')).decode('utf-8')
            print (''.join(words)),
        print ''
