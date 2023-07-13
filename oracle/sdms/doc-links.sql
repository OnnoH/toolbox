-- Blobs in database
select count(*) from cddb_internal_parts;

-- Check with cddb_parts
select count(*) from
(select part_id from cddb_internal_parts
minus
select id from cddb_parts
where cddb_parts.batch_id is not null
)
;
-- Check for archived parts still in database
select count(*) from
(select part_id from cddb_internal_parts
minus
select id from cddb_parts
where cddb_parts.batch_id is null
)
;
-- Remove them
delete from cddb_internal_parts
where part_id in 
(select part_id from cddb_internal_parts
minus
select id from cddb_parts
where cddb_parts.batch_id is null
)
;

-- Logical documents with parts.
select ld.id, ld.current_ver_seq_in_ldoc version, ld.creation_date, p.id, p.name
from meta_logical_documents ld
, meta_versions v
, cddb_documents d
, cddb_parts p
, cddb_doc_parts dp
where ld.id = v.ldoc_id
and ld.current_ver_seq_in_ldoc = v.seq_in_ldoc
and v.doc_id = d.id
and d.id = dp.doc_id
and dp.part_id = p.id
order by ld.creation_date desc
;

-- Run load script
java -D"semantica.docsdb.home=D:\DMS" -D"log4j.configuration=file:/D:/DMS/conf/log4j.xml" -jar "D:\DMS/lib/batch.jar" save <batch-id> 0
 
-- Internal parts already archived
select count(*) from
(select part_id from cddb_internal_parts
minus
select id from cddb_parts
)
;

update cddb_storage
set online_yn = 'Y'
where batch_id >= <batch-id>
;