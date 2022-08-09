#!/bin/bash

DBSTATUS=1
i=0

for i in {1..50};
do
  DBSTATUS=$(/opt/mssql-tools/bin/sqlcmd -h -1 -t 1 -U sa -P "$SA_PASSWORD" -Q "SET NOCOUNT ON; Select SUM(state) from sys.databases")
  if [[ -n $DBSTATUS ]] && [[ "$DBSTATUS" -eq "0" ]];
  then
    shop=$(/opt/mssql-tools/bin/sqlcmd -h -1 -t 1 -W -U sa -P "$SA_PASSWORD" \
    -Q "SET NOCOUNT ON; Select DB_ID('$SHOPIFY_DB_NAME')")
    if [[ "NULL" -eq "$shop" ]]; then
      echo "Creating Shopify DB"
      /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "$SA_PASSWORD" -d master \
      -v StartDate="$STARTING_DATE" -v DBName="$SHOPIFY_DB_NAME" \
      -v SchemaName="$SHOPIFY_DB_SCHEMA" -v DBUser="$SHOPIFY_DB_USER" \
      -v DBPassword="$SHOPIFY_DB_PASSWORD" \
      -i /usr/scripts/shopify.sql
      break
    else
      echo "Shopify DB already exists"
      break
    fi
  else
    echo "Still starting up..."
    sleep 2
  fi
done