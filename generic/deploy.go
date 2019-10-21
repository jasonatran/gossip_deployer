package generic

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

type FileParameter struct {
	Source string `json:"source"`
	Target string `json:"target"`
}

type ServiceParameter struct {
	Name    string            `json:"name"`
	Image   string            `json:"image"`
	Ports   []string          `json:"ports"`
	Volumes []string          `json:"volumes"`
	Env     map[string]string `json:"env"`
	Network string            `json:"network"`
}

type TestnetParameters struct {
	Args            []map[string]string `json:"args"`
	Files           [][]FileParameter   `json:"files"`
	LaunchScripts   []string            `json:"launch-script"`
	NetworkTopology string              `json:"network-topology"`
}

type TestnetResource struct {
	Cpus    string   `json:"cpus"`
	Memory  string   `json:"memory"`
	Volumes []string `json:"volumes"`
	Ports   []string `json:"ports"`
}

type Testnet struct {
	Servers    []int              `json:"servers"`
	Blockchain string             `json:"blockchain"`
	Nodes      int                `json:"nodes"`
	Images     []string           `json:"images"`
	Resources  []TestnetResource  `json:"resources"`
	Params     TestnetParameters  `json:"params"`
	Services   []ServiceParameter `json:"services"`
}

func deployToGenesis(config TestnetConfig, host string, output string, configFileDir string) {
	images := make([]string, len(config.Nodes))
	launchScripts := make([]string, len(config.Nodes))
	args := make([]map[string]string, len(config.Nodes))
	files := make([][]FileParameter, len(config.Nodes))
	for nodeIndex, node := range config.Nodes {
		images[nodeIndex] = node.Image
		launchScripts[nodeIndex] = node.LaunchScript
		files[nodeIndex] = make([]FileParameter, len(node.Files))
		for i, fileConfig := range node.Files {
			files[nodeIndex][i] = FileParameter{configFileDir + "/" + fileConfig.Source, fileConfig.Target}
		}
		args[nodeIndex] = node.Args
	}
	serviceParameters := make([]ServiceParameter, len(config.Services))
	i := 0
	for _, serviceConfig := range config.Services {
		volumes := make([]string, len(serviceConfig.Files))
		for i, fileConfig := range serviceConfig.Files {
			volumes[i] = configFileDir + "/" + fileConfig.Source + ":" + fileConfig.Target
		}
		serviceParameters[i] = ServiceParameter{serviceConfig.Name, serviceConfig.Image, serviceConfig.Ports, volumes, serviceConfig.Env, serviceConfig.Network}
		i++
	}
	testNet := Testnet{
		[]int{1},
		"generic",
		len(config.Nodes),
		images,
		[]TestnetResource{
			{"", "", []string{}, []string{}},
		},
		TestnetParameters{
			args,
			files,
			launchScripts,
			"none",
		},
		serviceParameters,
	}
	payload, err := json.Marshal(testNet)
	if err != nil {
		log.Fatal("Error preparing testnet configuration", err)
	}
	log.Printf(string(payload))
	resp, err := http.Post(fmt.Sprintf("%s/testnets", host), "application/json", bytes.NewBuffer(payload))
	if err != nil {
		log.Fatal("Error sending a testnet configuration", err)
	}
	if resp.StatusCode != 200 {
		log.Fatal("There was an error deploying the testnet", err)
	}
	testnetId, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatal("There was an error reading the response from genesis", err)
	}
	log.Printf("Testnet deployed with id %s", testnetId)
	if output != "" {
		err := ioutil.WriteFile(output, testnetId, 0644)
		if err != nil {
			log.Fatal("There was an error saving testnet id to file", err)
		}
	}
}
