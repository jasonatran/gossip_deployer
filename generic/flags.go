package generic

import (
	"github.com/urfave/cli"
)

var (
	NodesFileFlag = cli.StringFlag{
		Name:  "file",
		Usage: "File containing testnet definition",
		Value: "testnet.yaml",
	}
	WorkDir = cli.StringFlag{
		Name:  "workDir",
		Usage: "Folder where files generated during the testnet will be placed",
		Value: "",
	}
	Host = cli.StringFlag{
		Name:  "host",
		Usage: "Genesis host to deploy to",
		Value: "http://localhost:8000",
	}
)
