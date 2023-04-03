alter user SEMANTICA identified by PASSWORD;

select username, profile from DBA_USERS;

alter profile DEFAULT limit password_life_time UNLIMITED;

select resource_name, limit from dba_profiles where profile='DEFAULT';