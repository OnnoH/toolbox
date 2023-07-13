select n.usr_id, u.name, count(n.usr_id)
from meta_notifications n
, meta_users u
where u.id = n.usr_id
group by n.usr_id, u.name
;