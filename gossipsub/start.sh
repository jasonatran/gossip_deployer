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

# IFS=$'\r\n' GLOBIGNORE='*' command eval  'COUNT=($(cat ./NODECOUNT.txt))' 
# echo ${COUNT[0]}
IFS=$'\r\n' GLOBIGNORE='*' command eval  'IP=($(cat ./IP.txt))'
# echo ${IP[@]:0:COUNT}
IFS=$'\r\n' GLOBIGNORE='*' command eval  'MADDR=($(cat ./MADDR.txt))'
# echo ${MADDR[@]:0:COUNT}
IFS=$'\r\n' GLOBIGNORE='*' command eval  'PEERS=($(cat ./peers.txt))'
# echo ${PEERS[@]:0:COUNT}

deploy_host() {
  echo "deploying host"
  tmux new -s host -d
  tmux send-keys -thost "/usr/local/go/bin/go run ./cmd/host/main.go --pem ./pk.pem --log /output.log" C-m
}

# peer() {
#   echo "peering to: " ${IP[$NODE]} ${MADDR[$NODE]}
#   retry_run go run ./cmd/client/main.go open-peers /ip4/${IP[$NODE]}/tcp/3000/ipfs/${MADDR[$NODE]}
# }

peer() {
for peer in ${PEERS[@]}
do
  # echo ${IP[peer]}
  # echo ${MADDR[peer]}
  retry_run go run ./cmd/client/main.go open-peers /ip4/${IP[peer]}/tcp/3000/ipfs/${MADDR[peer]}
done
}

start() {
  deploy_host
  peer
}

start
