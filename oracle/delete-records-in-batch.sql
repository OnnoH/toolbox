declare
    l_norec number;
    l_batch_size number := 10000;
begin
    select count(*)
    into l_norec
    from mytable
    ;
    l_nosig := trunc(l_nosig / l_batch_size) + 1;
    
    for r in 1..l_norec
    loop
        delete from mytable
        where rownum <= l_batch_size
        ;
        commit;
    end loop;
end;

-- Record count check
select count(*)
from mytable t
, jointable j
where t.name = 'Oracle'
and t.id = j.id
and j.creation_date between to_date('20201121170000', 'YYYYMMDDHH24MISS') and to_date('20201121200000', 'YYYYMMDDHH24MISS')
;

-- Delete in batches of 100
declare
    l_commitpoint number := 100;
    l_recordcount number := 0;
begin

    for r in (select t.id
        from mytable t
        , jointable j
        where t.name = 'Oracle'
        and t.id = j.id
        and j.creation_date between to_date('20201121170000', 'YYYYMMDDHH24MISS') and to_date('20201121200000', 'YYYYMMDDHH24MISS')
    )
    loop
        delete from mytable where id = r.id;
        l_recordcount := l_recordcount + 1;
        if mod(l_recordcount, l_commitpoint) = 0
        then
            commit;
        end if;
        
    end loop;
    commit;
    
end;