#!/bin/bash
IP=`curl -4 http://icanhazip.com`
CURRENTIP=`cat /opt/firefly/dyndns/current_ip`
echo "Current IP" $CURRENTIP
echo "Public IP" $IP
if [ ${IP} != ${CURRENTIP} ]; then
	curl -s 'https://dynamicdns.park-your-domain.com/update?host=autotrader&domain=firefly.financial&password=3ca760d50a25425bb401e6a19bf5814d&ip='$IP
	echo $IP > current_ip
fi
