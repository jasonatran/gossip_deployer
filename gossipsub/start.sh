#!/bin/bash -xe

EXP=$1

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

IFS=$'\r\n' GLOBIGNORE='*' command eval  'IP=($(cat ./IP.txt))' 
# echo ${IP[@]:0:EXP}
IFS=$'\r\n' GLOBIGNORE='*' command eval  'MADDR=($(cat ./MADDR.txt))' 
# echo ${MADDR[@]:0:EXP}

deploy_host() {
  echo "deploying host"
  tmux new -s host -d
  tmux send-keys -thost "/usr/local/go/bin/go run ./cmd/host/main.go --pem ./pk.pem --log /output.log" C-m
}

peer() {
  for i in $(seq 0 $EXP)
  do
    echo "peering to: " $IP $MADDR
    retry_run go run ./cmd/client/main.go open-peers /ip4/${IP[i]}/tcp/3000/ipfs/${MADDR[i]}
  done
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