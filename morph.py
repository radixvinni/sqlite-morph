#coding: utf-8
import sqlite3

class MorphDict(object):
    "A dictionary that stores its data in sqlite3 database"

    def __init__(self, db='ru.sqlite'):
        self.conn = sqlite3.connect(db)
        self.conn.text_factory = str
        self.GET_ITEM = 'SELECT stem.rule FROM stem join form ON form.rule=stem.rule WHERE prefix||suffix = ?'
        self.ADD_ITEM = 'REPLACE INTO stem (rule, prefix) VALUES (?,?)'
        self.SIMILAR = 'SELECT prefix||suffix FROM form JOIN stem ON stem.rule = form.rule WHERE form.rowid = (SELECT form FROM word WHERE word = ?) order by random() limit 1'
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
