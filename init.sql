CREATE TABLE stem (rule integer, prefix text);
CREATE TABLE form (rule integer, suffix text);
CREATE TABLE norm (rule integer, suffix text);
.separator ":"
.import stems stem
.import forms form
.separator " "
.import norm norm

-- Для быстрого доступа создаем индекс словоформ
CREATE TABLE word (form integer, word text);
--INSERT INTO word(form, word) SELECT form.rowid, prefix||suffix FROM stem join form ON form.rule=stem.rule;
CREATE INDEX word_word ON word(word);

-- Добавим поле для тега с информацией о форме слова
ALTER TABLE form ADD COLUMN tag text default '';

