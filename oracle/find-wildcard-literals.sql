set escape '\\'

select *
from user_source
where lower(text) like '%\\_to\\_%' escape '\\'
order by name, line
;

select *
from user_source
where lower(text) like '%\\%%' escape '\\'
order by name, line
;

select *
from user_source
where lower(text) like '%''%'\\'
order by name, line
;