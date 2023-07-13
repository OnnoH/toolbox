$ ps -ef | grep LOCAL | grep oracle$ORACLE_SID

$ kill -9 $(ps -ef | grep LOCAL | grep oracle$ORACLE_SID | awk '{print $2}')