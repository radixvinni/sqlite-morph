#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""перенос тегов из opencorpora.sqlite в ru.sqlite
происходит в два захода. на первом строится 
соответствие между группами сравненением нормальных форм, 
на втором копируются теги"""
from __future__ import unicode_literals, division, print_function

import sqlite3
ru = sqlite3.connect('ru.sqlite')
oc = sqlite3.connect('opencorpora.sqlite')

#v1.matching rule forms
#for rule in ru
# 1.find matching rule forms. diff forms
# 2.diff stems
#comment. hard to diff stem\form letters. many similar groups

#v2. matching normal forms words
#for rule in ru
# 1.find_similar_oc_rule by norm words. diff words
# 2.for form in rule find tag

def find_similar_oc_rule(words, oc_rules, transform, i, threshold=0.5):
    "find matching word group in oc_rules with \
    more then threshold percent of words in \
    words and append its id to transform by key i"
    
    for j,tag in oc_rules:
        ocr = oc_rules[(j,tag)]
        rate=len(ocr&words)/len(words)
        if (rate>threshold):
            #if rate < 1:
             #   print(i,"->",j,rate)
            #внимание. i должен давать ограничение на часть речи! особенно если len(rur) маленький.
            if i < 450 and ("VERB" in tag or "INFN" in tag)\
            or i >= 450 and i < 500 and "plur" in tag\
            or i >= 500 and i < 600 and "femn" in tag\
            or i >= 600 and i < 750 and ("masc" in tag or "Ms-f" in tag)\
            or i >= 750 and i < 800 and "neut" in tag\
            or i >= 800 and i < 900 and ("ADJ" in tag or "PRT" in tag)\
            or i >= 900 and i < 950 and "VERB" not in tag and "NOUN" not in tag\
            or i >= 950 and i < 970 and "anim" in tag\
            or i >= 970 and "NUMR" in tag:
                try:
                    transform[i].append(j)
                except KeyError:
                    transform[i]=[j]
            else: print("Filtered by rule number:",i,tag)
            
import os.path
import json
if not os.path.isfile("transform"):
    # можно ускорить это, если читать сразу все слова, а группировать в python
    
    print("reading ru.sqlite")
    rules = ru.execute("SELECT * FROM norm ORDER BY rule").fetchall()
    ru_rules = [set()]*1000
    words = ru.execute("SELECT prefix||suffix, norm.rule FROM stem JOIN norm ON stem.rule=norm.rule").fetchall()
    print("scanning ru.sqlite")
    for rule, suff in rules:
        #words = ru.execute("SELECT prefix||suffix FROM stem JOIN norm ON stem.rule=norm.rule WHERE norm.rule = ?", (rule,)).fetchall()
        ru_rules[rule] = set([word[0] for word in words if word[1]==rule])#set(list(zip(*words))[0])
        if not len(ru_rules[rule]): print(rule,"has no words")

    print("reading oc.sqlite")
    oc_rules = dict()
    words = oc.execute("SELECT prefix||suffix, norm.rule, norm.tag FROM stem JOIN norm ON stem.rule=norm.rule").fetchall()
    print("scanning oc.sqlite")
    for word,rule,tag in words:
        try:
            oc_rules[(rule,tag)].add(word)
        except KeyError:
            oc_rules[(rule,tag)] = set([word])
    print("finding matches")
    #now diff oc_rules and ru_rules
    transform = dict()
    for rule, suff in rules:
        rur=ru_rules[rule]
        i=rule
        if(len(rur)):
            find_similar_oc_rule(rur, oc_rules, transform, i, threshold=0.5)
            if i not in transform: 
                find_similar_oc_rule(rur, oc_rules, transform, i, threshold=0.3)
            if i not in transform: 
                find_similar_oc_rule(rur, oc_rules, transform, i, threshold=0.2)
            if i not in transform: 
                print(i,"no match found, word count: ",len(rur))
    print("success:", 100* len(transform) / len(rules),"%")
    with open("transform", "w") as outfile: json.dump(transform, outfile, indent=4)
    exit(0)

with open("transform", "r") as infile: transform=json.loads(infile.read())
print("writing tags")
good=0
total=0
for i in transform:
    rule=int(i)
    #надо: контроллировать буквы. 
    # если все формы начинаются с одной буквы, делать перенос буквы в стем
    #надо: сливать тэги! объединять по j или пересекать, если ничего не найдено. 
    if len(transform[i])==1:
        sufs_dict = oc.execute("SELECT suffix,tag FROM form WHERE rule = ?",(transform[i][0],)).fetchall()
    else:
        sufs_dict = oc.execute("SELECT suffix,tag FROM form WHERE rule in "+str(tuple(transform[i]))).fetchall()
    sufs = set(list(zip(*sufs_dict))[0])
    rufs = ru.execute("SELECT suffix FROM form WHERE rule=?",(rule,)).fetchall()
    letter=rufs[0][0];
    rufs = set(list(zip(*rufs))[0])
    while len(letter) and all(len(data) for data in rufs) and all(data[0]==letter[0] for data in rufs):
            #move letter from forms to stem
            print ("---moving letter from forms to stem", rufs)
            ru.execute("UPDATE stem SET prefix = prefix||'%s' WHERE rule = %s" % (letter[0],rule))
            ru.execute("UPDATE form SET suffix = substr(suffix,2) WHERE rule = ?", (rule,))
            ru.execute("UPDATE norm SET suffix = substr(suffix,2) WHERE rule = ?", (rule,))
            rufs = ru.execute("SELECT suffix FROM form WHERE rule=?",(rule,)).fetchall()
            letter=rufs[0][0];
            rufs = set(list(zip(*rufs))[0])
            
    total+=len(rufs)
    good+=len(sufs&rufs)
    #if len(sufs-rufs): print("oc group",j,"has",sufs-rufs)
    #if len(rufs-sufs): print("oc group",j,"doesn't have",rufs-sufs)
    if len(sufs-rufs): print("group",i,"doesn't have",sufs-rufs)
    if len(rufs-sufs): print("group",i,"has",rufs-sufs)
    for suff in sufs&rufs:
        ru.execute('DELETE FROM form WHERE rule=? and suffix=?', (rule,suff))
    for suff, tag in sufs_dict:
        if suff in rufs:
            ru.execute('INSERT INTO form VALUES (?,?,?)',(rule,suff,tag))

print("sccess:",100*good/total,"%")
ru.commit()
ru.close()
oc.close()
