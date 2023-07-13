create or replace TYPE KEY_VALUE_PAIR AS OBJECT
( key    varchar2(255)
, value  varchar2(32767)
);

create or replace TYPE KEY_VALUE_PAIRS as TABLE of KEY_VALUE_PAIR;