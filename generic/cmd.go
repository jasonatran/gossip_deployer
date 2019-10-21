package generic

import (
	"github.com/urfave/cli"
	"io/ioutil"
	"log"
	"path/filepath"
)

var (
	DeployCommand = cli.Command{
		Name:        "deploy",
		Usage:       "Command to start a testnet",
		Description: `Command to start a testnet`,
		Action:      deployTestnet,
		Flags: []cli.Flag{
			NodesFileFlag,
			WorkDir,
			Host,
		},
	}
)

func deployTestnet(ctx *cli.Context) {
	configFile := ctx.String(NodesFileFlag.Name)
	workDir := ctx.String(WorkDir.Name)
	host := ctx.String(Host.Name)
	if workDir == "" {
		newDir, err := ioutil.TempDir("", "testnet")
		if err != nil {
			log.Fatalf("Could not create a temporary directory, %v", err)
		}
		workDir = newDir
	}

	nodesConfig, err := readNodesConfiguration(configFile)
	if err != nil {
		log.Fatalf("Error reading yaml file %v", err)
	}

	if err != nil {
		log.Fatalf("Error generating state %v", err)
	}
	absPath, err := filepath.Abs(configFile)
	if err != nil {
		log.Fatalf("Error computing the full path of config file %s %v", configFile, err)
	}
	deployToGenesis(nodesConfig, host, workDir+"/testnetId", filepath.Dir(absPath))
}
