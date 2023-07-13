Recreate the password file as follows:

1. Set the ORACLE_HOME and ORACLE_SID
2. connect / as sysdba from sqlplus
3. If the value of the “remote_login_passwordfile” parameter in the pfile or spfile is EXCLUSIVE, you must shutdown your instance
4. RENAME or DELETE the existing password file orapw[SID]
5. Issue the command:

$ orapwd file=[ORACLE_HOME]/dbs/orapw[SID] password=[sys_password]