#!/usr/bin/python

import sys
import os

nodes = sys.argv[1]

start = "---\nnodes:\n"

end = '\n# orchestra node\n  -\n    args: {}\n    image: "gcr.io/whiteblock/libp2p_gossipsub"\n    files:\n      -\n        source: IP.txt\n        target: /go-libp2p-pubsub-benchmark-tools/IP.txt\n      -\n        source: NODECOUNT.txt\n        target: /go-libp2p-pubsub-benchmark-tools/NODECOUNT.txt\n      -\n        source: orchestra.sh\n        target: /go-libp2p-pubsub-benchmark-tools/orchestra.sh\n    launch-script: "ls"'

def replace(edit):
  if edit == 0:
    st='#node '
    st+=str(edit)
    st+='\n  -\n    args: {}\n    image: "gcr.io/whiteblock/libp2p_gossipsub"\n    files:\n      -\n        source: pems/pk-'
    st+=str(edit+1)
    st+='.pem'
    st+='\n        target: /go-libp2p-pubsub-benchmark-tools/pk.pem\n      -\n        source: NODECOUNT.txt\n        target: /go-libp2p-pubsub-benchmark-tools/NODECOUNT.txt\n      -\n        source: IP.txt\n        target: /go-libp2p-pubsub-benchmark-tools/IP.txt\n      -\n        source: MADDR.txt\n        target: /go-libp2p-pubsub-benchmark-tools/MADDR.txt\n      -\n        source: start.sh\n        target: /go-libp2p-pubsub-benchmark-tools/start.sh \n    launch-script: "./start.sh"\n'
    return st
  else:
    st='#node '
    st+=str(edit)
    st+='\n  -\n    args: {}\n    image: "gcr.io/whiteblock/libp2p_gossipsub"\n    files:\n      -\n        source: pems/pk-'
    st+=str(edit+1)
    st+='.pem'
    st+='\n        target: /go-libp2p-pubsub-benchmark-tools/pk.pem\n      -\n        source: NODECOUNT.txt\n        target: /go-libp2p-pubsub-benchmark-tools/NODECOUNT.txt\n      -\n        source: IP.txt\n        target: /go-libp2p-pubsub-benchmark-tools/IP.txt\n      -\n        source: MADDR.txt\n        target: /go-libp2p-pubsub-benchmark-tools/MADDR.txt\n      -\n        source: start.sh\n        target: /go-libp2p-pubsub-benchmark-tools/start.sh \n    launch-script: "./start.sh '
    st+=str(edit-1)
    st+='"\n'
    return st

#print(os.getcwd()+"/gossip.yaml")
#print(os.path.exists(os.getcwd()+"/gossip.yaml"))

cwd = os.getcwd()
file1 = cwd+"/gossip.yaml"
file2 = cwd+"/NODECOUNT.txt"

if os.path.exists(file1):
  ans = raw_input("File already exists, would you like to overwrite the existing file? (y/n) \n")
  if ans.lower() == "y" or ans.lower == "yes":
    os.remove(file1)
    os.remove(file2)
  else:
    print("Exiting, did not overwrite the file.")
    exit(0)

f1 = open("gossip.yaml", "a")
f1.write(start)
for i in range(0,int(nodes)):
  f1.write(replace(i))
f1.write(end)
f1.close()

f2 = open("NODECOUNT.txt", "a")
f2.write(str(int(nodes)-1))
f2.close()
