import os
import sys
import networkx as nx
#import matplotlib
#matplotlib.use('TkAgg')
#import matplotlib.pyplot as plt
# from networkx.generators import

def usage():
  print("usage: python topo.py <seed> <nodes> <degree>")
  exit(1)

try:
  sys.argv[1]
except:
  print("Please provide the seed")
  usage()

try:
  sys.argv[2]
except:
  print("Please provide the number of nodes")
  usage()

try:
  sys.argv[3]
except:
  print("Please provide the degree of connectivity")
  usage()

seed=int(sys.argv[1])
nodes=int(sys.argv[2])
degree=int(sys.argv[3])

ba=nx.barabasi_albert_graph(nodes, degree, seed)
sp=dict(nx.all_pairs_shortest_path(ba))

cwd=os.getcwd()
dir=cwd+"/topology/"

if os.path.isdir(dir):
  print("deleting directory")
  filelist = [ f for f in os.listdir(dir) if f.endswith(".txt") ]
  for f in filelist:
      os.remove(os.path.join(dir, f))
else:
  os.mkdir("topology")

for i in range(0, nodes):
   l=[n for n in ba.neighbors(i)]
   cont="\n".join(map(str,l))
   print(i,cont)

   f=open(dir+"peers_"+str(i)+".txt",'w')
   f.write(cont)
   f.close()

'''
listing the neighbors of the node
-------------------------------------
for i in range(nodes):
  print([n for n in ba.neighbors(i)])
'''

# print(nx.is_connected(ba))
# degree_sequence = sorted([d for n, d in ba.degree()], reverse=True)
# print(sum(degree_sequence)/len(degree_sequence))
# print(degree_sequence)
# print(max(degree_sequence))

'''
plotting the node connections using matplotlib
-------------------------------------------------
plt.subplot(155)
nx.draw(ba, with_labels=True, font_weight='bold')
plt.show()
'''
