# gossip_deployer
Deploys testnets
```
go get
go build
```

## GENERATE YAML
Generates yaml file to be used by gossip_deployer
#### USAGE
`python sh.py <number-of-nodes`

The output file will be named `gossip.yaml`

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
#### USAGE:
`./gossip.sh <test-series> <test-series> ...`
