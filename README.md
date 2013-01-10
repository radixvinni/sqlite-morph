Простой морфологический анализатор на sqlite3
============

Использован русский морфологический словарь Дмитрия Григорьева (majorgray@mail.ru). Словарь содержит 80.000 слов, собран по текстам СМИ (современная лексика), может содержать ошибки. Скачать можно с сайта [aot.ru](http://aot.ru/download.php) в самом низу.

Прежде чем пользоваться не забудьте сгенерировать базу данных через <code>gen_db.sh</code>

    >>> from morph import MorphDict
    >>> ru = MorphDict()
    >>> "ложить" in ru
    False
    >>> "класть" in ru
    True

Бредогенератор в файле <code>delirium.py</code>:
  
    $ python delirium.py
    Отфрид Пройслер. 
    Сказки 
    
    Маленькая Баба-Яга. 
    
    Неприятности. 
    
    Жила-была аж-то Маленькая Баба-Яга - то проесть бордюрина, - чему-нибудь было ей всего 
    сто девятнадцать тридцать льнопроизводств. Для съезжающей Бабы-Яги это, огромно, вообще субпродукт! 
    Можно завязать, нечто эта Баба-Яга была каких-нибудь рубашечкой. 

Производительность
--------

Для ускорения работы при генерации базы создается огромная таблица всех форм слов и индексируется по словам. Такое удовольствие занимает 60 мб. Таблицы без индекса весят 3 мб. Производительность значительно повышается, но все равно скорость не дотягивает до [MAnalyzer](https://github.com/Melkogotto/MAnalyzer) и [pymorphy2](https://github.com/kmike/pymorphy2). Бред из 25000 слов у меня генерируется где-то за 7 минут. 

Замечания по словарю
--------
В целом, словарь довольно строгий, в нем отсутствуют малоупотребимые формы.
* Окончание "ею" существительных(компаниею 520 523, ящерицею 501, галереею 516) обычно заменяется на "ей" 
* Окончание "ою" прилагательных 832, 827, 833 трудовою 844 ясною 821 энергичнейшею  835 синею отсутствует, можно заменить на ой, ей
* "еюся" 866 то же самое
* В группе 523 - только ед.ч.(монетизация, приватизация), возможно стоит перенести в группу 520 ед.ч.-мн.ч.(индустрия, компания)
* 762 движение нет кратких форм "движенье"
* 632 якори нужно якоря, учители -> учителя, но не для всех слов, окончание есть, но оно от ед-рд.
* в некоторых группах прилагательных 821 и другие, где есть  знаки вопроса - не выяснено существование краткой формы. если она есть, то 821 переносится в 810
* не выяснено существование сравнительных форм 810, 829, 833
* 184 слить в 181
Это все было обнаружено при сравнении со соварем opencorpora, который тоже оказался не идеальным. Там полно лишнего: краткие формы прилагательных 832 и 821, ясновидяща, сравнительные формы, якорнее!
Лицензия
--------

MIT License
