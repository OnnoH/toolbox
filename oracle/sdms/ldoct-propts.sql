select l.id, l.name, p.id, p.name, lp.*
from meta_ldoc_types l
, meta_property_types p
, meta_ldoct_propt lp
where l.id = lp.ldoct_id
and p.id = lp.propt_id
-- and l.id = 13
order by l.id, lp.seq_in_ldoct, p.name