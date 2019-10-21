package generic

import (
	"gopkg.in/yaml.v2"
	"io/ioutil"
)

type TestnetConfig struct {
	Nodes    []NodeConfig       `yaml:"nodes"`
	Services map[string]Service `yaml:"services"`
}

type FileConfig struct {
	Source string `yaml:"source"`
	Target string `yaml:"target"`
}

type Service struct {
	Name    string            `yaml:"name"`
	Image   string            `yaml:"image"`
	Files   []FileConfig      `yaml:"files"`
	Ports   []string          `yaml:"ports"`
	Env     map[string]string `yaml:"env"`
	Network string            `yaml:"network"`
}

type NodeConfig struct {
	Image        string            `yaml:"image"`
	LaunchScript string            `yaml:"launch-script"`
	Files        []FileConfig      `yaml:"files"`
	Args         map[string]string `yaml:"args"`
}

func readNodesConfiguration(yamlFile string) (TestnetConfig, error) {
	yamlContents, err := ioutil.ReadFile(yamlFile)
	if err != nil {
		return TestnetConfig{}, err
	}
	var configs TestnetConfig
	err = yaml.Unmarshal(yamlContents, &configs)
	if err != nil {
		return TestnetConfig{}, err
	}
	return configs, nil
}
