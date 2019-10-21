package main

import (
	"github.com/urfave/cli"
//	"github.com/whiteblock/deployer/eth2mock"
	"github.com/whiteblock/deployer/generic"
	"log"
	"os"
)

func main() {
	app := cli.NewApp()
	app.Version = "1.0.0"
	app.Name = "deployer"
	app.Usage = "Deploys testnets"
	app.Commands = []cli.Command{
//		eth2mock.DeployCommand,
		generic.DeployCommand,
	}
	err := app.Run(os.Args)
	if err != nil {
		log.Fatal(err)
	}
}
