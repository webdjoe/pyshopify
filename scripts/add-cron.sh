exists=$(crontab -l | grep -q 'shopify_cli' && echo 'true' || echo 'false')

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


if [[ -z "$DAYS" ]]; then
  DAYS="-d 5"
else
  DAYS=""
fi

if [[ -n "$CONF" && -f "$CONF" ]]; then
  CONF=" --config $CONF"
else
  if [[ -n "$CONFIG_FILE" && -f "$CONFIG_FILE" ]]; then
    CONF=" --config $CONFIG_FILE"
  fi
  CONF=""
fi

if [[ $exists == 'false' ]]; then

    echo "Adding cron job"
    (crontab -l; echo "0 4 * * * /usr/scripts/shopify_run.sh $DAYS$CONF") | crontab -
  else
    echo "Cron job already exists"
fi