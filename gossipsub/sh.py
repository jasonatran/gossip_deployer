#!/usr/bin/python

import sys
import os

try:
  nodes = sys.argv[1]
except:
  print("ERROR: Nodes argument was not given.\nUsage: python sh.py <nodes>")
  exit(1)

def genYAML(edit):
  st='#node '
  st+=str(edit)
  st+='\n  -'
  st+='\n    args: {}'
  st+='\n    image: "gcr.io/whiteblock/libp2p_gossipsub"'
  st+='\n    files:'
  st+='\n      -\n        source: pems/pk-'
  st+=str(edit+1)
  st+='.pem'
  st+='\n        target: /go-libp2p-pubsub-benchmark-tools/pk.pem'
  st+='\n      -'
  st+='\n        source: NODECOUNT.txt'
  st+='\n        target: /go-libp2p-pubsub-benchmark-tools/NODECOUNT.txt'
  st+='\n      -'
  st+='\n        source: IP.txt'
  st+='\n        target: /go-libp2p-pubsub-benchmark-tools/IP.txt'
  st+='\n      -'
  st+='\n        source: MADDR.txt'
  st+='\n        target: /go-libp2p-pubsub-benchmark-tools/MADDR.txt'
  st+='\n      -'
  st+='\n        source: peers_'
  st+=str(edit)
  st+='.txt'
  st+='\n        target: /go-libp2p-pubsub-benchmark-tools/peers.txt'
  st+='\n      -'
  st+='\n        source: start.sh'
  st+='\n        target: /go-libp2p-pubsub-benchmark-tools/start.sh'
  st+='\n    launch-script: "./start.sh"\n'
  return st

def getIPs(n):
  ips=""
  f=open("IP.txt", "r")
  cont = f.readlines()
  for ip in cont[:int(n)]:
    if ip != cont[int(n)-1]:
      ip=ip.strip('\n')
      ips+='\"'+ip+':8080\",'
    else:
      ip=ip.strip('\n')
      ips+='\"'+ip+':8080\"'
  return ips

def genConf(ips):
  config='{"orchestra":{"omitSubnet":true,"hostRPCAddressesIfOmitSubnet":['
  config+=ips
  config+='],"messageNanoSecondInterval":50000000,"clientTimeoutSeconds":5,"messageLocation":"client.message.json","messageByteSize":1000,"testDurationSeconds":180,"testWarmupSeconds":60,"testCooldownSeconds":120},"subnet":{"numHosts":10,"pubsubCIDR":"127.0.0.1/8","pubsubPortRange":[3000,4000],"rpcCIDR":"127.0.0.1/8","rpcPortRange":[8080,9080],"peerTopology":"whiteblocks"},"host":{"keyType":"ecdsa","rsaBits":2048,"transports":["tcp","ws"],"muxers":[["yamux","/yamux/1.0.0"],["mplex","/mplex/6.7.0"]],"security":"secio","pubsubAlgorithm":"gossip","omitRelay":false,"omitConnectionManager":false,"omitNATPortMap":false,"omitRPCServer":false,"omitDiscoveryService":false,"omitRouting":false},"general":{"loggerLocation":"","debug":true}}'
  return config

start = "---\nnodes:\n"

end = '\n# orchestra node\n  -\n    args: {}\n    image: "gcr.io/whiteblock/libp2p_gossipsub"\n    files:\n      -\n        source: IP.txt\n        target: /go-libp2p-pubsub-benchmark-tools/IP.txt\n      -\n        source: NODECOUNT.txt\n        target: /go-libp2p-pubsub-benchmark-tools/NODECOUNT.txt\n      -\n        source: orchestra.sh\n        target: /go-libp2p-pubsub-benchmark-tools/orchestra.sh\n      -\n        source: ./configs/config.json\n        target: /go-libp2p-pubsub-benchmark-tools/configs/orchestra/config.json\n    launch-script: "ls"'

cwd = os.getcwd()
file1 = cwd+"/gossip.yaml"
file2 = cwd+"/NODECOUNT.txt"
file3 = cwd+"/configs/config.json"

if os.path.exists(file1):
  ans = raw_input("File already exists, would you like to overwrite the existing file? (y/n) \n")
  if ans.lower() == "y" or ans.lower == "yes":
    try: 
      os.remove(file1)
      os.remove(file2)
      os.remove(file3)
    except:
      pass
  else:
    print("Exiting, did not overwrite the file.")
    exit(0)

f1 = open(file1, "a")
f1.write(start)
for i in range(0,int(nodes)):
  f1.write(genYAML(i))
f1.write(end)
f1.close()

f2 = open(file2, "a")
f2.write(str(int(nodes)-1))
f2.close()

try:
  os.mkdir(cwd+"/configs")
except:
  pass
f3 = open(file3, "a")
f3.write(str(genConf(getIPs(nodes))))
f3.close()
