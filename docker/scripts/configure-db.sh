#!/bin/bash

DBSTATUS=1
ERRCODE=1
NUMDBS=0
i=0

for i in {1..50};
do
  DBSTATUS=$(/opt/mssql-tools/bin/sqlcmd -h -1 -t 1 -U sa -P "$SA_PASSWORD" -Q "SET NOCOUNT ON; Select SUM(state) from sys.databases")
  if [ "$?" -eq "0" ]
  then
    NUMDBS=$(/opt/mssql-tools/bin/sqlcmd -h -1 -t 1 -U sa -P "$SA_PASSWORD" -Q "SET NOCOUNT ON; Select COUNT(*) from sys.databases")
    if [ "$NUMDBS" -eq "4" ]; then
      /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "$SA_PASSWORD" -d master -i /usr/scripts/setup.sql
      /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "$SA_PASSWORD" -d master -i /usr/scripts/dates.sql
      echo "Database setup completed"
      break
    fi
  else
    echo "Still starting up..."
    sleep 1
  fi
done