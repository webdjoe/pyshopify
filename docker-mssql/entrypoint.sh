#!/bin/bash

touch /etc/profile.d/mssql.sh
chmod +x /etc/profile.d/mssql.sh

write_sql_ini ()
{
  if [ -f "$CONFIG_FILE" ]; then
    echo "Setting envar $1 to $2"
    section="SQL"
    crudini --inplace --set "$CONFIG_FILE" sql "$1" "$2"
  fi
}

if [[ -z "$CONFIG_FILE" ]]; then
  CONFIG_FILE="/root/config.ini"
fi
if [[ -f "$CONFIG_FILE" ]]; then
  export CONFIG_FILE
  sed -i '/CONFIG_FILE/d' /etc/profile.d/mssql.sh
  echo CONFIG_FILE="$CONFIG_FILE" >> /etc/profile.d/mssql.sh
else
  unset CONFIG_FILE
  sed -i '/CONFIG_FILE/d' /etc/profile.d/mssql.sh
fi

if [[ -z "$SHOPIFY_DB_NAME" ]]; then
    SHOPIFY_DB_NAME="shop_rest"
    export SHOPIFY_DB_NAME
    sed -i '/SHOPIFY_DB_NAME/d' /etc/profile.d/mssql.sh
    echo export SHOPIFY_DB_NAME="$SHOPIFY_DB_NAME" >> /etc/profile.d/mssql.sh
fi
write_sql_ini "database" "$SHOPIFY_DB_NAME"

if [[ -z "$SHOPIFY_DB_SCHEMA" ]]; then
    SHOPIFY_DB_SCHEMA="dbo"
    export SHOPIFY_DB_SCHEMA
    sed -i '/SHOPIFY_DB_SCHEMA/d' /etc/profile.d/mssql.sh
    echo SHOPIFY_DB_SCHEMA="$SHOPIFY_DB_SCHEMA" >> /etc/profile.d/mssql.sh
fi
write_sql_ini "schema" "$SHOPIFY_DB_SCHEMA"

if [[ -z "$STARTING_DATE" ]]; then
    STARTING_DATE="20190101"
    export STARTING_DATE
    sed -i '/STARTING_DATE/d' /etc/profile.d/mssql.sh
    echo STARTING_DATE="$STARTING_DATE" >> /etc/profile.d/mssql.sh
fi

if [[ -n "$SHOPIFY_DB_USER" && -n "$SHOPIFY_DB_PASSWORD" ]]; then
  write_sql_ini "db_user" "$SHOPIFY_DB_USER"
  write_sql_ini "db_pass" "$SHOPIFY_DB_PASSWORD"
else
  write_sql_ini "db_user" "sa"
  write_sql_ini "db_pass" "$SA_PASSWORD"
fi

if [[ -z "$DB_PORT" ]]; then
    DB_PORT="1433"
    export DB_PORT
    sed -i '/DB_PORT/d' /etc/profile.d/mssql.sh
    echo DB_PORT="$DB_PORT" >> /etc/profile.d/mssql.sh
fi
write_sql_ini "port" "$DB_PORT"

write_sql_ini "connector" "mssql+pyodbc"

/usr/scripts/configure-db.sh &
/opt/mssql/bin/sqlservr