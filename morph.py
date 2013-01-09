#coding: utf-8
import sqlite3

class MorphDict:
    "A dictionary that stores its data in sqlite3 database"

    def __init__(self, db='ru.sqlite'):
        self.conn = sqlite3.connect(db)
        self.conn.text_factory = str
        self.GET_ITEM = 'SELECT form.tag FROM stem join form ON form.rule=stem.rule WHERE prefix||suffix = ?'
        self.ADD_ITEM = 'REPLACE INTO stem (rule, prefix) VALUES (?,?)'
        self.SIMILAR = 'SELECT prefix||suffix FROM form JOIN stem ON stem.rule = form.rule WHERE form.rowid = (SELECT form.rowid FROM stem join form ON form.rule=stem.rule WHERE prefix||suffix = ?) order by random() limit 1'
        self.SIMILAR_FAST = 'SELECT prefix||suffix FROM form JOIN stem ON stem.rule = form.rule WHERE form.rowid = (SELECT form FROM word WHERE word = ?) order by random() limit 1'
    def __contains__(self, key):
            return self.conn.execute(self.GET_ITEM, (key,)).fetchone() is not None

    def __getitem__(self, key):
        item = self.conn.execute(self.GET_ITEM, (key,)).fetchone()
        if item is None:
            raise KeyError('Word not found')
        return item[0]

    def replace(self, key):
        item = self.conn.execute(self.SIMILAR, (key,)).fetchone()
        if item is None:
            return key
        return item[0]

    def __setitem__(self, key, value):
            self.conn.execute(self.ADD_ITEM, (key, value))

    def __del__(self):
            self.conn.close()

class MorphInfo:
    "Morphological info about a word form"
    tags = {
    "POST": "часть речи", 
    "NOUN": "имя существительное", 
    "ADJF": "имя прилагательное (полное)", 
    "ADJS": "имя прилагательное (краткое)", 
    "COMP": "компаратив", 
    "VERB": "глагол (личная форма)", 
    "INFN": "глагол (инфинитив)", 
    "PRTF": "причастие (полное)", 
    "PRTS": "причастие (краткое)", 
    "GRND": "деепричастие", 
    "NUMR": "числительное", 
    "ADVB": "наречие", 
    "NPRO": "местоимение-существительное", 
    "PRED": "предикатив", 
    "PREP": "предлог", 
    "CONJ": "союз", 
    "PRCL": "частица", 
    "INTJ": "междометие", 
    "ANim": "одушевлённость / одушевлённость не выражена", 
    "anim": "одушевлённое", 
    "inan": "неодушевлённое", 
    "GNdr": "род / род не выражен", 
    "masc": "мужской род", 
    "femn": "женский род", 
    "neut": "средний род", 
    "Ms-f": "общий род", 
    "NMbr": "число", 
    "sing": "единственное число", 
    "plur": "множественное число", 
    "Sgtm": "singularia tantum", 
    "Pltm": "pluralia tantum", 
    "Fixd": "неизменяемое", 
    "CAse": "категория падежа", 
    "nomn": "именительный падеж", 
    "gent": "родительный падеж", 
    "datv": "дательный падеж", 
    "accs": "винительный падеж", 
    "ablt": "творительный падеж", 
    "loct": "предложный падеж", 
    "voct": "звательный падеж", 
    "gen1": "первый родительный падеж", 
    "gen2": "второй родительный (частичный) падеж", 
    "acc2": "второй винительный падеж", 
    "loc1": "первый предложный падеж", 
    "loc2": "второй предложный (местный) падеж", 
    "Abbr": "аббревиатура", 
    "Name": "имя", 
    "Surn": "фамилия", 
    "Patr": "отчество", 
    "Geox": "топоним", 
    "Orgn": "организация", 
    "Trad": "торговая марка", 
    "Subx": "возможна субстантивация", 
    "Supr": "превосходная степень", 
    "Qual": "качественное", 
    "Apro": "местоименное", 
    "Anum": "порядковое", 
    "Poss": "притяжательное", 
    "V-ey": "форма на -ею", 
    "V-oy": "форма на -ою", 
    "Cmp2": "сравнительная степень на по-", 
    "V-ej": "форма компаратива на -ей", 
    "ASpc": "категория вида", 
    "perf": "совершенный вид", 
    "impf": "несовершенный вид", 
    "TRns": "категория переходности", 
    "tran": "переходный", 
    "intr": "непереходный", 
    "Impe": "безличный", 
    "Uimp": "безличное употребление", 
    "Mult": "многократный", 
    "Refl": "возвратный", 
    "PErs": "категория лица", 
    "1per": "1 лицо", 
    "2per": "2 лицо", 
    "3per": "3 лицо", 
    "TEns": "категория времени", 
    "pres": "настоящее время", 
    "past": "прошедшее время", 
    "futr": "будущее время", 
    "MOod": "категория наклонения", 
    "indc": "изъявительное наклонение", 
    "impr": "повелительное наклонение", 
    "INvl": "категория совместности", 
    "incl": "говорящий включён в действие", 
    "excl": "говорящий не включён в действие", 
    "VOic": "категория залога", 
    "actv": "действительный залог", 
    "pssv": "страдательный залог", 
    "Infr": "разговорное", 
    "Slng": "жаргонное", 
    "Arch": "устаревшее", 
    "Litr": "литературный вариант", 
    "Erro": "опечатка", 
    "Dist": "искажение", 
    "Ques": "вопросительное", 
    "Dmns": "указательное", 
    "Prnt": "вводное слово", 
    "V-be": "форма на -ье", 
    "V-en": "форма на -енен", 
    "V-ie": "отчество через -ие-", 
    "V-bi": "форма на -ьи", 
    "Fimp": "деепричастие от глагола несовершенного вида", 
    "Prdx": "может выступать в роли предикатива", 
    "Coun": "счётная форма", 
    "Coll": "собирательное числительное", 
    "V-sh": "деепричастие на -ши", 
    "Af-p": "форма после предлога", 
    "Inmx": "может использоваться как неодушевлённое", 
    "Vpre": "Вариант предлога ( со, подо, ...)"}
    def __init__(self, tag=0):
        self.tag=tag

    def __repr__(self):
        return self.tag
