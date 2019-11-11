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

IFS=$'\r\n' GLOBIGNORE='*' command eval  'IP=($(cat ./IP.txt))'
# echo ${IP[@]:0:COUNT}
IFS=$'\r\n' GLOBIGNORE='*' command eval  'MADDR=($(cat ./MADDR.txt))'
# echo ${MADDR[@]:0:COUNT}
IFS=$'\r\n' GLOBIGNORE='*' command eval  'PEERS=($(cat ./peers.txt))'
# echo ${PEERS[@]:0:COUNT}
IFS=$'\r\n' GLOBIGNORE='*' command eval  'SELF=($(cat ./self.txt))'
# echo ${PEERS[@]:0:COUNT}

deploy_host() {
  echo "deploying host"
  tmux new -s host -d
  tmux send-keys -thost "/usr/local/go/bin/go run ./cmd/host/main.go --pem ./pk.pem --log /output.log" C-m
}

# LINEAR PEERING TOPOLOGY
# peer() {
#   echo "peering to: " ${IP[$NODE]} ${MADDR[$NODE]}
#   retry_run go run ./cmd/client/main.go open-peers /ip4/${IP[$NODE]}/tcp/3000/ipfs/${MADDR[$NODE]}
# }

peer() {
  for peer in ${PEERS[@]}
  do
    index=$((peer-1))
    # echo [ "$index" -eq "$SELF" ]
    if [ "$index" -ne "$SELF" ]; then
      retry_run go run ./cmd/client/main.go open-peers /ip4/${IP[index]}/tcp/3000/ipfs/${MADDR[index]}
    else
      continue
    fi
  done
}

start() {
  deploy_host
  peer
}

start
