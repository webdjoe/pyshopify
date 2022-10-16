#!/bin/bash

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
  write_sql_ini "db_user" "root"
  write_sql_ini "db_pass" "$MYSQL_ROOT_PASSWORD"
fi

if [[ -z "$DB_PORT" ]]; then
    DB_PORT="3306"
    export DB_PORT
    sed -i '/DB_PORT/d' /etc/profile.d/mssql.sh
    echo DB_PORT="$DB_PORT" >> /etc/profile.d/mssql.sh
fi
write_sql_ini "port" "$DB_PORT"

write_sql_ini "connector" "mysql+mysqldb"

DBSTATUS=$(mysql -h "localhost" --u"root" -p"$MYSQL_ROOT_PASSWORD" -e "SHOW DATABASES;" | grep $DB_NAME)

if [ -n $DBSTATUS ]; then
    if [ -n "$STARTING_DATE" ]; then
        shopify_db -c mysql+mysqldb -s localhost -p ${MYSQL_TCP_PORT:-3306} -U root \
        -W ${MYSQL_ROOT_PASSWORD} -d ${DB_NAME:-shop_sql} --db-user ${DB_USER:-shop_user} \
        --db-pass ${DB_PASS}
    else
        shopify_db -c mysql+mysqldb -s localhost -p ${MYSQL_TCP_PORT:-3306} -U root \
        -W ${MYSQL_ROOT_PASSWORD} -d ${DB_NAME:-shop_sql} --db-user ${DB_USER:-shop_user} \
        --db-pass ${DB_PASS} --date-start ${STARTING_DATE}
    fi
fi
