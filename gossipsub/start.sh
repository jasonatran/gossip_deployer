#!/bin/bash -xe

RETRY_DELAY=5
RETRIES=100

retry_run() {
        n=0
        set -e
        until [ $n -ge $RETRIES ]
        do
                $@ && break
                n=$[$n+1]
                sleep $RETRY_DELAY
        done
        set +e
}

IFS=$'\r\n' GLOBIGNORE='*' command eval  'COUNT=($(cat ./NODECOUNT.txt))' 
# echo ${COUNT[0]}
command eval  'IP=($(cat ./IP.txt))' 
# echo ${IP[@]:0:COUNT}
command eval  'MADDR=($(cat ./MADDR.txt))' 
# echo ${MADDR[@]:0:COUNT}

deploy_host() {
  echo "deploying host"
  tmux new -s host -d
  tmux send-keys -thost "/usr/local/go/bin/go run ./cmd/host/main.go --pem ./pk.pem --log /output.log" C-m
}

peer() {
  echo "peering to: " ${IP[$COUNT[0]]} ${MADDR[$COUNT[0]]}
  retry_run go run ./cmd/client/main.go open-peers /ip4/${IP[$COUNT[0]]}/tcp/3000/ipfs/${MADDR[$COUNT[0]]}
}

start() {
  if [[ "$IP" = "" ]]; then
    deploy_host
  else
    deploy_host
    peer
  fi
}

start