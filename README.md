#gossip_deployer
Deploys testnets
```
go get
go build
```

## GENERATE YAML
Generates yaml file to be used by gossip_deployer
#### USAGE
`python sh.py <number-of-nodes>`

The output file will be named `gossip.yaml`, `NODECOUNT.txt`, and `config.json`.
Files will be distributed and used in the script described below.

## GOSSIP DEPLOYER
The gossip deployer will be used to deploy a testnet by sending an API request to the locally running Genesis
#### USAGE
`./gossip_deployer deploy [flags]`

## SCRIPT
There is a script that will be included in the directory called `gossip.sh` which will automate the test. The script will:
1. deploy the testnet
2. peer the nodes
3. run the tests passed as args
4. output relevant files + metrics

\*note: the script must be run from the directory where the script file exists.
#### USAGE:
`./gossip.sh <test-series> <test-series> ...`

## STEPS
1. run python script to generate necessary files.
`python sh.py <number-of-nodes>`
2. run gossip script
`./gossip.sh <test-series> ...`

## PRIVKEYS
The private keys have been generated using the tool from https://github.com/agencyenterprise/pem-utils
1000 private keys have been pregenerated to be used for every test series. The key files can be found in https://github.com/whiteblock/gossip_deployer/tree/master/gossipsub/pems

The google sheet describes the IP addresses and private key. 
https://docs.google.com/spreadsheets/u/1/d/1yRZnQv016C9Alon0KFNse6zIMc5k9YD3GGMmU2am1hc/edit#gid=1524596621
