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
      /root/venv/bin/shopify_db -c mssql+pyodbc -s localhost -p ${DB_PORT:-1433} \
      -U sa -W "$SA_PASSWORD" -d "$SHOPIFY_DB_NAME" --schema "${SHOPIFY_DB_SCHEMA:-'dbo'}" \
      --db-user "$SHOPIFY_DB_USER" --db-pass "$SHOPIFY_DB_PASSWORD"
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