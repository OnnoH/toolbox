#!/usr/bin/env bash
 
source .env
 
sqlcmd -S ${SERVER_ADDRESS} -U ${SA_USERNAME} -P ${SA_PASSWORD} -i create_database.sql -C

# Cannot use the loop, because of constraints
# 
# ls -1 tables/*.sql | while read TABLE
# do
#     echo ${TABLE}
#     sqlcmd -S ${SERVER_ADDRESS}  -U ${SA_USERNAME} -P ${SA_PASSWORD} -d ${DB_NAME} -i ${TABLE} -C
# done
#

sqlcmd -S ${SERVER_ADDRESS}  -U ${SA_USERNAME} -P ${SA_PASSWORD} -d ${DB_NAME} -i tables/customer.sql -C
sqlcmd -S ${SERVER_ADDRESS}  -U ${SA_USERNAME} -P ${SA_PASSWORD} -d ${DB_NAME} -i tables/product.sql -C
sqlcmd -S ${SERVER_ADDRESS}  -U ${SA_USERNAME} -P ${SA_PASSWORD} -d ${DB_NAME} -i tables/invoice.sql -C