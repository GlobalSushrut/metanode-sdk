package metanode

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
)

// SDK version
const Version = "1.1.0"

// MetaNodeSDK represents the main SDK interface
type MetaNodeSDK struct {
	CLIPath      string
	Network      string
	RPCEndpoint  string
	WSEndpoint   string
	ConfigPath   string
	WalletPath   string
	IpfsGateway  string
	initialized  bool
}

// Config represents the SDK configuration
type Config struct {
	AppName          string            `json:"app_name"`
	CreatedAt        string            `json:"created_at"`
	Network          string            `json:"network"`
	ConsensusEnabled bool              `json:"consensus_enabled"`
	AgreementEnabled bool              `json:"agreement_enabled"`
	RPCEndpoint      string            `json:"rpc_endpoint"`
	WSEndpoint       string            `json:"ws_endpoint"`
	IpfsGateway      string            `json:"ipfs_gateway"`
	WalletPath       string            `json:"wallet_path"`
	Testnet          map[string]string `json:"testnet"`
}

// Agreement represents a blockchain agreement
type Agreement struct {
	ID             string            `json:"id"`
	Type           string            `json:"type"`
	CreatedAt      string            `json:"created_at"`
	Network        string            `json:"network"`
	Status         string            `json:"status"`
	BlockchainTx   string            `json:"blockchain_tx"`
	Verified       bool              `json:"verified"`
	AppID          string            `json:"app_id"`
	AppName        string            `json:"app_name"`
	Meta           map[string]string `json:"meta"`
}

// NewSDK creates a new MetaNode SDK instance
func NewSDK() (*MetaNodeSDK, error) {
	// Find the CLI path
	cliPath, err := findCLI()
	if err != nil {
		return nil, err
	}

	// Create SDK instance with defaults
	sdk := &MetaNodeSDK{
		CLIPath:     cliPath,
		Network:     "testnet",
		RPCEndpoint: "http://159.203.17.36:8545",
		WSEndpoint:  "ws://159.203.17.36:8546",
		ConfigPath:  filepath.Join(os.Getenv("HOME"), ".metanode"),
		WalletPath:  filepath.Join(os.Getenv("HOME"), ".metanode", "wallet"),
		IpfsGateway: "http://localhost:8081",
	}

	return sdk, nil
}

// Initialize initializes the SDK
func (sdk *MetaNodeSDK) Initialize() error {
	// Check if CLI exists
	_, err := os.Stat(sdk.CLIPath)
	if os.IsNotExist(err) {
		return fmt.Errorf("MetaNode CLI not found at %s", sdk.CLIPath)
	}

	// Create config directory if it doesn't exist
	if _, err := os.Stat(sdk.ConfigPath); os.IsNotExist(err) {
		err = os.MkdirAll(sdk.ConfigPath, 0755)
		if err != nil {
			return err
		}
	}

	// Create wallet directory if it doesn't exist
	if _, err := os.Stat(sdk.WalletPath); os.IsNotExist(err) {
		err = os.MkdirAll(sdk.WalletPath, 0755)
		if err != nil {
			return err
		}
	}

	sdk.initialized = true
	return nil
}

// InitApp initializes a new MetaNode application
func (sdk *MetaNodeSDK) InitApp(appName string) error {
	cmd := exec.Command(sdk.CLIPath, "init", appName, "--network", sdk.Network, "--rpc", sdk.RPCEndpoint)
	output, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Errorf("error initializing app: %v, output: %s", err, string(output))
	}

	fmt.Println(string(output))
	return nil
}

// DeployApp deploys a MetaNode application
func (sdk *MetaNodeSDK) DeployApp(appPath string) error {
	cmd := exec.Command(sdk.CLIPath, "deploy", appPath, "--network", sdk.Network, "--rpc", sdk.RPCEndpoint)
	output, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Errorf("error deploying app: %v, output: %s", err, string(output))
	}

	fmt.Println(string(output))
	return nil
}

// CreateAgreement creates a new agreement for an application
func (sdk *MetaNodeSDK) CreateAgreement(appPath string, agreementType string) (*Agreement, error) {
	cmd := exec.Command(sdk.CLIPath, "agreement", appPath, "--create", "--type", agreementType)
	output, err := cmd.CombinedOutput()
	if err != nil {
		return nil, fmt.Errorf("error creating agreement: %v, output: %s", err, string(output))
	}

	fmt.Println(string(output))

	// Parse output to find agreement ID
	lines := strings.Split(string(output), "\n")
	var agreementID string
	for _, line := range lines {
		if strings.Contains(line, "Agreement created with ID:") {
			parts := strings.Split(line, ":")
			if len(parts) >= 2 {
				agreementID = strings.TrimSpace(parts[1])
			}
		}
	}

	if agreementID == "" {
		return nil, fmt.Errorf("could not find agreement ID in output")
	}

	// Get agreement details
	return sdk.GetAgreement(appPath, agreementID)
}

// GetAgreement gets details of an agreement
func (sdk *MetaNodeSDK) GetAgreement(appPath, agreementID string) (*Agreement, error) {
	// Agreement file path
	agreementPath := filepath.Join(appPath, "metanode_agreements", fmt.Sprintf("agreement_%s.json", agreementID))

	// Read agreement file
	data, err := ioutil.ReadFile(agreementPath)
	if err != nil {
		return nil, fmt.Errorf("error reading agreement file: %v", err)
	}

	// Parse agreement JSON
	var agreement Agreement
	err = json.Unmarshal(data, &agreement)
	if err != nil {
		return nil, fmt.Errorf("error parsing agreement JSON: %v", err)
	}

	return &agreement, nil
}

// DeployAgreement deploys an agreement to the blockchain
func (sdk *MetaNodeSDK) DeployAgreement(appPath, agreementID string) error {
	cmd := exec.Command(sdk.CLIPath, "agreement", appPath, "--deploy", "--id", agreementID)
	output, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Errorf("error deploying agreement: %v, output: %s", err, string(output))
	}

	fmt.Println(string(output))
	return nil
}

// CreateNodeCluster creates a node cluster for improved decentralization
func (sdk *MetaNodeSDK) CreateNodeCluster(appPath string) error {
	cmd := exec.Command(sdk.CLIPath, "cluster", appPath, "--create", "--rpc", sdk.RPCEndpoint)
	output, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Errorf("error creating node cluster: %v, output: %s", err, string(output))
	}

	fmt.Println(string(output))
	return nil
}

// CheckStatus checks the status of a MetaNode application
func (sdk *MetaNodeSDK) CheckStatus(appPath string) error {
	cmd := exec.Command(sdk.CLIPath, "status", appPath)
	output, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Errorf("error checking status: %v, output: %s", err, string(output))
	}

	fmt.Println(string(output))
	return nil
}

// TestTestnetConnection tests the connection to the testnet
func (sdk *MetaNodeSDK) TestTestnetConnection() error {
	cmd := exec.Command(sdk.CLIPath, "testnet", "--test", "--rpc", sdk.RPCEndpoint)
	output, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Errorf("error testing testnet connection: %v, output: %s", err, string(output))
	}

	fmt.Println(string(output))
	return nil
}

// Helper function to find the CLI path
func findCLI() (string, error) {
	// Check if CLI is in PATH
	path, err := exec.LookPath("metanode-cli")
	if err == nil {
		return path, nil
	}

	// Check in common locations
	locations := []string{
		filepath.Join(os.Getenv("HOME"), "bin", "metanode-cli"),
		filepath.Join(os.Getenv("HOME"), "metanode-deployment", "bin", "metanode-cli"),
		"/usr/local/bin/metanode-cli",
	}

	for _, loc := range locations {
		if _, err := os.Stat(loc); err == nil {
			return loc, nil
		}
	}

	return "", fmt.Errorf("metanode-cli not found")
}
