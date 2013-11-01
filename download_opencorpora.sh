#!/bin/sh
#загрузка словаря opencorpora

wget http://opencorpora.org/files/export/dict/dict.opcorpora.xml.bz2
bunzip2 dict.opcorpora.xml.bz2

sed -i 's/ё/е/g' dict.opcorpora.xml
