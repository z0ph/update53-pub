#!/bin/sh

# Check current public IP using ifconfig.co webservice
IP=$( curl -s https://v4.ifconfig.co/ )

# Check current route 53 DNS A record
OLDIP=$( dig +short YOU_DNS_A_RECORD_NAME )
DATE=`date '+%Y-%m-%d-%H:%M:%S'`


if [ "$IP" = "$OLDIP" ]; then
        echo "$DATE - IP are the same, nothing to do: $IP"
else
        echo "$DATE - IP are not equal - Current:$IP OLD:$OLDIP - Updating..."

        HOSTED_ZONE_ID=$( aws route53 list-hosted-zones-by-name | grep -B 1 -e "YOUR_PARENT_DNS_NAME" | sed 's/.*hostedzone\/\([A-Za-z0-9]*\)\".*/\1/' | head -n 1 )
        echo "$DATE - Hosted zone being modified: $HOSTED_ZONE_ID"

        INPUT_JSON=$( cat ./update-route53-A.json | sed "s/127\.0\.0\.1/$IP/" )

        INPUT_JSON="{ \"ChangeBatch\": $INPUT_JSON }"

        aws route53 change-resource-record-sets --hosted-zone-id "$HOSTED_ZONE_ID" --cli-input-json "$INPUT_JSON"

fi