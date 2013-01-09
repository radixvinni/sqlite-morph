# -*- coding: utf-8 -*-
"""
Module for OpenCorpora XML dictionaries parsing.
"""
from __future__ import absolute_import, unicode_literals, division

import logging
import collections

import json

def json_write(filename, obj, **json_options):
    """ Create file ``filename`` with ``obj`` serialized to JSON """

    json_options.setdefault('ensure_ascii', False)
    with codecs.open(filename, 'w', 'utf8') as f:
        json.dump(obj, f, **json_options)


def json_read(filename):
    """ Read an object from a json file ``filename`` """
    with codecs.open(filename, 'r', 'utf8') as f:
        return json.load(f)


logger = logging.getLogger()

ParsedDictionary = collections.namedtuple('ParsedDictionary', 'lemmas links grammemes version revision')


def load_json_or_xml_dict(filename):
    """
    Load (parse) raw OpenCorpora dictionary either from XML or from JSON
    (depending on file extension) and return a ParsedDictionary.
    """
    if filename.endswith(".json"):
        logger.info('loading json...')
        data = json_read(filename)
    else:
        logger.info('parsing xml...')
        data = parse_opencorpora_xml(filename)

    return ParsedDictionary(*data)


def parse_opencorpora_xml(filename):
    """
    Parse OpenCorpora dict XML and return a tuple

        (lemmas_list, links, grammemes, version, revision)

    """
    from lxml import etree

    links = []
    lemmas = {}
    grammemes = []
    version, revision = None, None

    def _clear(elem):
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]

    for ev, elem in etree.iterparse(filename):

        if elem.tag == 'grammeme':
            name = elem.find('name').text
            parent = elem.get('parent')
            alias = elem.find('alias').text
            description = elem.find('description').text

            grameme = (name, parent, alias, description)
            grammemes.append(grameme)
            _clear(elem)

        if elem.tag == 'dictionary':
            version = elem.get('version')
            revision = elem.get('revision')
            _clear(elem)

        if elem.tag == 'lemma':
            lemma_id, lemma_forms = _lemma_forms_from_xml_elem(elem)
            lemmas[lemma_id] = lemma_forms
            _clear(elem)

        elif elem.tag == 'link':
            link_tuple = (
                elem.get('from'),
                elem.get('to'),
                elem.get('type'),
            )
            links.append(link_tuple)
            _clear(elem)

    return lemmas, links, grammemes, version, revision


def xml_dict_to_json(xml_filename, json_filename):
    """
    Convert XML dictionary to JSON for faster loading.
    It may be useful while developing dictionary preparation routines.
    """
    logger.info('parsing xml...')
    parsed_dct = parse_opencorpora_xml(xml_filename)

    logger.info('writing json...')
    json_write(json_filename, parsed_dct)


def _lemma_forms_from_xml_elem(elem):
    """
    Return a list of (word, tags) pairs given an XML element with lemma.
    """
    def _tags(elem):
        return ",".join(g.get('v') for g in elem.findall('g'))

    lemma = []
    lemma_id = elem.get('id')

    if len(elem) == 0:  # deleted lemma
        return lemma_id, lemma

    base_info = elem.findall('l')

    assert len(base_info) == 1
    base_tags = _tags(base_info[0])

    for form_elem in elem.findall('f'):
        tags = _tags(form_elem)
        form = form_elem.get('t').lower()
        lemma.append(
            (form, " ".join([base_tags, tags]).strip())
        )

    return lemma_id, lemma
