-- патч тегов после синхронизации для удобства. опционально.
delete from form where rule = 903 and suffix = 'о';

insert into form values (903, 'о', 'NPRO,neut sing,nomn');
insert into form values (903, 'о', 'NPRO,neut sing,accs');
