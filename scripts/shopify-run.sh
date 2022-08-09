#!/bin/bash

while [[ $# -gt 0 ]]; do
  case $1 in
    -d|--days)
      DAYS="$2"
      shift
      shift
      ;;
    -c|--config)
      CONF="$2"
      if [ ! -f "$CONF" ]; then
        echo "Config file $CONF does not exist"
        unset CONF
      fi
      shift
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

if [ $# -eq 0 ]; then

  (cd /root && exec "$VIRTUAL_ENV"/bin/shopify_cli --sql-out -d 5)
  exit 0
fi

if [[ -n "$DAYS" && -n "$CONF" ]]; then
  (cd /root && exec "$VIRTUAL_ENV"/bin/shopify_cli --sql-out -d "$DAYS" --config "$CONFIG")
  exit 0
fi

if [ -n "$CONF" ]; then
  (cd /root && exec "$VIRTUAL_ENV"/bin/shopify_cli -d 5 --sql-out --config "$CONF")
  exit 0
else
  (cd /root && exec "$VIRTUAL_ENV"/bin/shopify_cli -d "$DAYS" --sql-out)
  exit 1
fi