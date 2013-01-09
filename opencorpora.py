#coding: utf-8
from __future__ import unicode_literals
from parse import load_json_or_xml_dict
from itertools import izip
from forms2 import seen_paradigms
import os

LEMMA_PREFIXES = ["", "по", "наи"]

parsed_dict = load_json_or_xml_dict('dict.opcorpora.xml')

#lemmas = _join_lemmas(parsed_dict.lemmas, parsed_dict.links)

lemmas = parsed_dict.lemmas

seen_tags = dict()      # tag string => id
paradigms = dict()  # form => paradigm

def longest_common_substring(data):
    """
    Return a longest common substring of a list of strings::

        >>> longest_common_substring(["apricot", "rice", "cricket"])
        'ric'
        >>> longest_common_substring(["apricot", "banana"])
        'a'
        >>> longest_common_substring(["foo", "bar", "baz"])
        ''

    See http://stackoverflow.com/questions/2892931/.
    """
    substr = ''
    if len(data) > 1 and len(data[0]) > 0:
        for i in range(len(data[0])):
            for j in range(len(data[0])-i+1):
                if j > len(substr) and all(data[0][i:i+j] in x for x in data):
                    substr = data[0][i:i+j]
    return substr

def _to_paradigm(lemma):
    """
    Extract (stem, paradigm) pair from lemma list.
    Paradigm is a list of suffixes with associated tags and prefixes.
    """
    forms, tags = list(zip(*lemma))
    prefixes = [''] * len(tags)
    stem = os.path.commonprefix(forms)
    if stem == "":
        stem = longest_common_substring(forms)
        prefixes = [form[:form.index(stem)] for form in forms]
        if any(pref not in LEMMA_PREFIXES for pref in prefixes):
            stem = ""
            prefixes = [''] * len(tags)
    suffixes = (
        form[len(pref)+len(stem):]
        for form, pref in zip(forms, prefixes)
    )
    return stem, tuple(zip(suffixes, tags, prefixes))

def get_form(para):
    return list(next(izip(*para)))

tags=0;
for lemma in lemmas.values():
    stem, paradigm = _to_paradigm(lemma) 
    form = tuple(sorted(tuple(set(get_form(paradigm)))))
    for suff, tag, pref in paradigm:
        if tag not in seen_tags:
            seen_tags[tag] = tags
            tags += 1
    if form not in paradigms:
        paradigms[form] = tuple([(suff, seen_tags[tag], pref) for suff, tag, pref in paradigm])
    if form in seen_paradigms:
        print stem,'{',', '.join(form),'}'
