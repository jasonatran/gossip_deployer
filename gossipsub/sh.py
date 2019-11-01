#!/usr/bin/python

import sys
import os

nodes = sys.argv[1]

start = "---\nnodes:\n"

end = '\n# orchestra node\n\t-\n\t\targs: {}\n\t\timage: "gcr.io/whiteblock/libp2p_gossipsub"\n\t\tfiles:\n\t\t\t-\n\t\t\t\tsource: IP.txt\n\t\t\t\ttarget: /go-libp2p-pubsub-benchmark-tools/IP.txt\n\t\t\t-\n\t\t\t\tsource: NODECOUNT.txt\n\t\t\t\ttarget: /go-libp2p-pubsub-benchmark-tools/NODECOUNT.txt\n\t\t\t-\n\t\t\t\tsource: orchestra.sh\n\t\t\t\ttarget: /go-libp2p-pubsub-benchmark-tools/orchestra.sh\n\t\tlaunch-script: "ls"'

def replace(edit):
  if edit == 0:
    st='#node '
    st+=str(edit)
    st+='\n\t-\n\t\targs: {}\n\t\timage: "gcr.io/whiteblock/libp2p_gossipsub"\n\t\tfiles:\n\t\t\t-\n\t\t\t\tsource: pems/pk-'
    st+=str(edit+1)
    st+='.pem'
    st+='\n\t\t\t\ttarget: /go-libp2p-pubsub-benchmark-tools/pk.pem\n\t\t\t-\n\t\t\t\tsource: NODECOUNT.txt\n\t\t\t\ttarget: /go-libp2p-pubsub-benchmark-tools/NODECOUNT.txt\n\t\t\t-\n\t\t\t\tsource: IP.txt\n\t\t\t\ttarget: /go-libp2p-pubsub-benchmark-tools/IP.txt\n\t\t\t-\n\t\t\t\tsource: MADDR.txt\n\t\t\t\ttarget: /go-libp2p-pubsub-benchmark-tools/MADDR.txt\n\t\t\t-\n\t\t\t\tsource: start.sh\n\t\t\t\ttarget: /go-libp2p-pubsub-benchmark-tools/start.sh \n\t\tlaunch-script: "./start.sh"\n'
    return st
  else:
    st='#node '
    st+=str(edit)
    st+='\n\t-\n\t\targs: {}\n\t\timage: "gcr.io/whiteblock/libp2p_gossipsub"\n\t\tfiles:\n\t\t\t-\n\t\t\t\tsource: pems/pk-'
    st+=str(edit+1)
    st+='.pem'
    st+='\n\t\t\t\ttarget: /go-libp2p-pubsub-benchmark-tools/pk.pem\n\t\t\t-\n\t\t\t\tsource: NODECOUNT.txt\n\t\t\t\ttarget: /go-libp2p-pubsub-benchmark-tools/NODECOUNT.txt\n\t\t\t-\n\t\t\t\tsource: IP.txt\n\t\t\t\ttarget: /go-libp2p-pubsub-benchmark-tools/IP.txt\n\t\t\t-\n\t\t\t\tsource: MADDR.txt\n\t\t\t\ttarget: /go-libp2p-pubsub-benchmark-tools/MADDR.txt\n\t\t\t-\n\t\t\t\tsource: start.sh\n\t\t\t\ttarget: /go-libp2p-pubsub-benchmark-tools/start.sh \n\t\tlaunch-script: "./start.sh '
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
