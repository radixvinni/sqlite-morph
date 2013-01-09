from parse import load_json_or_xml_dict
import os

parsed_dict = load_json_or_xml_dict('dict.opcorpora.xml')

#lemmas = _join_lemmas(parsed_dict.lemmas, parsed_dict.links)

gramtab = []
paradigms = []
words = []

seen_tags = dict()
seen_paradigms = dict()


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

for index, lemma in enumerate(lemmas):
    stem, paradigm = _to_paradigm(lemma)
    for suff, tag, pref in paradigm:
        if tag not in seen_tags:
            seen_tags[tag] = len(gramtab)
            gramtab.append(tag)

    # build paradigm index
    if paradigm not in seen_paradigms:
        seen_paradigms[paradigm] = len(paradigms)
        paradigms.append(
            tuple([(suff, seen_tags[tag], pref) for suff, tag, pref in paradigm])
        )

    para_id = seen_paradigms[paradigm]
    popularity[para_id] += 1

    for idx, (suff, tag, pref) in enumerate(paradigm):
        form = pref+stem+suff
        words.append(
            (form, (para_id, idx))
        )
