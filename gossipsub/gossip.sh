#!/bin/bash -xe

IFS=$'\r\n' GLOBIGNORE='*' command eval  'COUNT=($(cat ./NODECOUNT.txt))' 
COUNT=$((COUNT + 1))
# echo ${COUNT[0]}
# echo $COUNT

COMMAND=whiteblock
WAIT_TIME=380
BANDWIDTH=1000
PACKET_LOSS=0
LATENCY=0

RETRY_DELAY=10
RETRIES=50

retry() {
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

log() {
  for i in $(seq 0 $COUNT)
  do
    docker cp whiteblock-node$i:/output.log ./$1$i
  done
}

deploy() {
  # ../gossip_deployer deploy --file ./test.yaml
  ../gossip_deployer deploy --file ./gossip.yaml
}

runtest() {
  ulimit -n 10000
  local dir=series_$1_$(date +"%FT%T"| tr -d '[:space:]')
  sudo mkdir $dir

  deploy

  $COMMAND sync

  retry $COMMAND netconfig all -d $LATENCY -l $PACKET_LOSS -b $BANDWIDTH

  retry docker exec -d whiteblock-node$COUNT ./orchestra.sh

  OUTPUT_FILE=$dir/resource.log
  tmux new -s resource_recorder -d; tmux send-keys -t resource_recorder "docker stats >> $OUTPUT_FILE" C-m

  while :
  do
  if [[ $(docker exec whiteblock-node$COUNT head /output.log | wc -l) -eq 0 ]]; then
    echo ""
  else
    break
  fi
  done

  sleep $WAIT_TIME

  retry $COMMAND netconfig clear

  log $dir/node

  tmux kill-session -t resource_recorder
}

reset() {
        # Defaults to contol case specs
        LATENCY=0
        PACKET_LOSS=0
        BANDWIDTH=1000
}

run_case() {
  for i in {1..3}
  do
    runtest $1.$i
  done
}

for i in $@; do
  reset
  case "$i" in
    1)
      # Control Case
      run_case 1a
      run_case 1b
      run_case 1c
      ;;
    2)
      # Network Latency Test
      LATENCY=50
      run_case 2a
      LATENCY=100
      run_case 2b
      LATENCY=150
      run_case 2c
      ;;
    3)
      # Packet Loss
      PACKET_LOSS=0.01
      run_case 3a
      PACKET_LOSS=0.1
      run_case 3b
      PACKET_LOSS=1
      run_case 3c
      ;;
    4)
      # Bandwidth
      BANDWIDTH=10
      run_case 4a
      BANDWIDTH=50
      run_case 4b
      BANDWIDTH=100
      run_case 4c
      ;;
    5)
      # 
      LATENCY=200
      run_case 5a
      LATENCY=300
      run_case 5b
      LATENCY=400
      run_case 5c
      ;;
    6)
      # 
      LATENCY=150
      PACKET_LOSS=0.01
      BANDWIDTH=10
      TPS=500

      run_case 6a
      run_case 6b
      run_case 6c
      ;;
    7)
      # 
      TX_SIZE=500
      run_case 7a
      TX_SIZE=750
      run_case 7b
      TX_SIZE=1000
      run_case 7c
      ;;
    8)
      # 
      LATENCY=0
      PACKET_LOSS=0

      BANDWIDTH=10
      TPS=700
      run_case 8a

      BANDWIDTH=50
      TPS=1000
      run_case 8b

      BANDWIDTH=100
      TPS=1500
      run_case 8c
      ;;
    9)
      # 
      LATENCY=0
      PACKET_LOSS=0
      BANDWIDTH=1000

      run_case20 9a
      run_case25 9b
      run_case30 9c
      ;;

    *)
            echo "Enter a valid case#"
            ;;
  esac
done
