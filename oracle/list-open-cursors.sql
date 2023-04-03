select  sql_text, count(*) as "OPEN CURSORS", user_name from v$open_cursor
group by sql_text, user_name order by count(*) desc;