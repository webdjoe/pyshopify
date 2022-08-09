#!/bin/bash

touch /etc/profile.d/mssql.sh
chmod +x /etc/profile.d/mssql.sh

if [[ -z "$SHOPIFY_DB_NAME" ]]; then
    SHOPIFY_DB_NAME="shop_rest";
    export SHOPIFY_DB_NAME
    sed -i '/SHOPIFY_DB_NAME/d' /etc/profile.d/mssql.sh
    echo export SHOPIFY_DB_NAME="$SHOPIFY_DB_NAME" >> /etc/profile.d/mssql.sh
fi

if [[ -z "$SHOPIFY_DB_SCHEMA" ]]; then
    SHOPIFY_DB_SCHEMA="dbo";
    export SHOPIFY_DB_SCHEMA
    sed -i '/SHOPIFY_DB_SCHEMA/d' /etc/profile.d/mssql.sh
    echo SHOPIFY_DB_SCHEMA="$SHOPIFY_DB_SCHEMA" >> /etc/profile.d/mssql.sh
fi

if [[ -z "$STARTING_DATE" ]]; then
    STARTING_DATE="20190101";
    export STARTING_DATE
    sed -i '/STARTING_DATE/d' /etc/profile.d/mssql.sh
    echo STARTING_DATE="$STARTING_DATE" >> /etc/profile.d/mssql.sh
fi

if [[ -z "$SHOPIFY_DB_USER" ]]; then
    SHOPIFY_DB_USER="shop_user"
    export SHOPIFY_DB_USER
    sed -i "/SHOPIFY_DB_USER/d" /etc/profile.d/mssql.sh
    echo SHOPIFY_DB_USER="$SHOPIFY_DB_USER" >> /etc/profile.d/mssql.sh
fi

if [[ -z "$SHOPIFY_DB_PASSWORD" ]]; then
    SHOPIFY_DB_PASSWORD="StrongerPassword1!"
    export SHOPIFY_DB_PASSWORD
    sed -i '/SHOPIFY_DB_PASSWORD/d' /etc/profile.d/mssql.sh
    echo SHOPIFY_DB_PASSWORD="$SHOPIFY_DB_PASSWORD" >> /etc/profile.d/mssql.sh
fi

/usr/scripts/configure-db.sh &
/opt/mssql/bin/sqlservr
