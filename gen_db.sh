#!/bin/sh
# перекодировка 1251 в utf8 - уже сделал при добавлении в репозитарий
#find LexGroup -type f|while read i; do iconv -f WINDOWS-1251 -t UTF-8 "$i" >tmp; mv tmp "$i"; done 

# делаем список из окончаний
grep '{' LexGroup -r > forms        # собираем оглавление
sed -i 's/^.*lexgroup\.//gI' forms  # удаляем название и путь файла в начале строки
sed -i 's/ .\+\.//gI' forms         # удаляем лишнее в конце строки

#удаление внутренних скобок
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18
do
  sed -i 's/\([а-я]\+\){\([^{},]\+\),\?/\1\2,\1{/g' forms
  sed -i 's/,\?[а-я]\+{}//g' forms
done

#удаление внешних скобок с линеаризацией
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
do
  sed -i 's/^\([^{]*\){\([^},]*\),\?/\1\2\n\1{/g' forms
  sed -i '/^.*{}/d' forms
done

#удаление пустых строк и окончаний
sed -i '/^.*?/d' forms
sed -i 's/#//g' forms

# делаем список стемов (оснований слов)
grep -v '{' LexGroup -r > stems        
sed -i 's/^.*lexgroup\.//gI' stems  # удаляем название и путь файла в начале строки
sed -i 's/#//g' forms

#теперь собственно sqlite
if [ -f ru.sqlite ];then rm ru.sqlite; fi
sqlite3 -init init.sql ru.sqlite ''

#кончил - вытри за собой
rm stems
rm forms
