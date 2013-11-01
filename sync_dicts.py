#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""перенос тегов из opencorpora.sqlite в ru.sqlite"""
from __future__ import unicode_literals, division

import sqlite3
ru = sqlite3.connect('ru.sqlite')
oc = sqlite3.connect('opencorpora.sqlite')

#v1.matching rule forms
#for rule in ru
# find matching rule in oc. diff forms
# diff stems
#comment. hard to diff stem\form letters

#v2. matching normal forms
#for rule in ru
# find matching norm words. diff
# for form in rule find tag
import os.path
import json
if not os.path.isfile("transform"):
    print("scanning ru.sqlite")
    rules = ru.execute("SELECT * FROM norm ORDER BY rule").fetchall()
    ru_rules = [set()]*1000
    for rule, suff in rules:
        words = ru.execute("SELECT prefix||suffix FROM stem JOIN norm ON stem.rule=norm.rule WHERE norm.rule = ?", (rule,)).fetchall()
        ru_rules[rule] = set(list(zip(*words))[0])
        if not len(ru_rules[rule]): print(rule,"has no words")

    print("scanning oc.sqlite")
    oc_norms = oc.execute("SELECT * FROM norm ORDER BY rule").fetchall()
    oc_rules = [set()]*len(oc_norms)
    for rule, suff in oc_norms:
        words = oc.execute("SELECT prefix||suffix FROM stem JOIN norm ON stem.rule=norm.rule WHERE norm.rule = ?", (rule,)).fetchall()
        oc_rules[rule] = set(list(zip(*words))[0])

    print("preparing transform")
    #now diff oc_rules and ru_rules
    transform = dict()
    for rule, suff in rules:
        rur=ru_rules[rule]
        i=rule
        if(len(rur)):
            for j,ocr in enumerate(oc_rules):
                rate=len(ocr&rur)/len(rur)
                if (rate>0.5):
                    if rate < 1:
                        print(i,"->",j,rate)
                    try:
                        transform[i].append(j)
                    except KeyError:
                        transform[i]=[j]
            if i not in transform: print(i,"has no analog")
    print("success:", 100* len(transform) / len(rules),"%")
    with open("transform", "w") as outfile: json.dump(transform, outfile, indent=4)
    exit(0)
with open("transform", "r") as infile: transform=json.loads(infile.read())
print("starting to transform")
good=0
total=0
for i in transform:
    rule=int(i)
    #try control letters
    if len(transform[i])==1:
        j=transform[i][0]
        sufs = oc.execute("SELECT suffix,tag FROM form WHERE rule=?",(j,)).fetchall()
        sufs_dict=dict(sufs)
        sufs = set(list(zip(*sufs))[0])
        rufs = ru.execute("SELECT suffix FROM form WHERE rule=?",(rule,)).fetchall()
        rufs = set(list(zip(*rufs))[0])
        total+=len(rufs)
        good+=len(sufs&rufs)
        #if len(sufs-rufs): print("oc group",j,"has",sufs-rufs)
        #if len(rufs-sufs): print("oc group",j,"doesn't have",rufs-sufs)
        if len(sufs-rufs): print("group",i,"doesn't have",sufs-rufs)
        if len(rufs-sufs): print("group",i,"has",rufs-sufs)
        for suff in sufs&rufs:
            tag = sufs_dict[suff]
            ru.execute('UPDATE form SET tag=? WHERE rule=? and suffix=?', (tag,rule,suff))

print("sccess:",100*good/total,"%")
ru.commit()
ru.close()
oc.close()
