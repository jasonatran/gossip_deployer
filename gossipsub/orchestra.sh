#!/bin/bash -xe

EXP=$1
RETRY_DELAY=5

retry_run() {
        set -e
        while :
        do
                $@ && break
                n=$[$n+1]
                sleep $RETRY_DELAY
        done
        set +e
}

IFS=$'\r\n' GLOBIGNORE='*' command eval  'IP=($(cat ./IP.txt))' 
# echo ${IP[@]:0:EXP}

check() {
  for i in $(seq 0 $EXP)
  do
    retry_run go run ./cmd/client/main.go -p ${IP[i]}:8080 id
  done
}

send() {
  go run ./cmd/orchestra/main.go start
}

check