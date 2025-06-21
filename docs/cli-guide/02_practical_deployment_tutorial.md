# MetaNode CLI: Practical Deployment Tutorial

This tutorial provides a hands-on guide to deploying a real application using the MetaNode CLI. We'll walk through the complete process from initialization to deployment and monitoring of a data analysis application with blockchain integration.

## Prerequisites

Before starting, make sure you have:

1. Installed the MetaNode SDK and CLI
2. Access to the MetaNode testnet (running at `http://159.203.17.36:8545`)
3. Basic knowledge of Python for our example application

## Tutorial Overview

In this tutorial, we'll:
1. Set up a new MetaNode application
2. Develop a simple data analysis application
3. Create and deploy a blockchain agreement
4. Configure verification proofs
5. Deploy the application using vPod technology
6. Monitor and manage the deployed application

## Step 1: Initialize the Application

First, let's initialize a new MetaNode application:

```bash
metanode-cli init data-analyzer --network testnet
```

This creates a new directory called `data-analyzer` with the necessary MetaNode configuration files.

## Step 2: Develop the Application

Let's create a simple data analysis application that uses federated average execution to compute statistics across distributed data sources.

```bash
# Create application source directory
mkdir -p data-analyzer/src
```

Create the main application file:

```bash
# File: data-analyzer/src/app.py

from metanode.full_sdk import MetaNodeSDK
import numpy as np
import json
import os

class DataAnalyzer:
    def __init__(self):
        self.sdk = MetaNodeSDK()
        self.sdk.connect_to_testnet(rpc_url="http://159.203.17.36:8545")
        self.computation_id = None
    
    def register_computations(self):
        # Register our statistical analysis function
        self.computation_id = self.sdk.register_computation(
            function=self.statistical_analysis,
            description="Statistical analysis with federated averaging"
        )
        print(f"Registered computation with ID: {self.computation_id}")
        
        # Save computation ID to config
        self._save_computation_id()
        
        return self.computation_id
    
    def _save_computation_id(self):
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "metanode_config", 
            "computation.json"
        )
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        with open(config_path, "w") as f:
            json.dump({"computation_id": self.computation_id}, f)
    
    def statistical_analysis(self, data):
        """
        Perform statistical analysis on data using federated averaging
        
        Input: List of numerical values
        Output: Dict of statistical metrics
        """
        if not data or not isinstance(data, list):
            return {"error": "Input must be a non-empty list of numbers"}
        
        try:
            # Convert to numpy array
            values = np.array(data, dtype=float)
            
            # Calculate various statistics
            result = {
                "mean": float(np.mean(values)),
                "median": float(np.median(values)),
                "std_dev": float(np.std(values)),
                "min": float(np.min(values)),
                "max": float(np.max(values)),
                "count": len(values),
                "quartiles": [
                    float(np.percentile(values, 25)),
                    float(np.percentile(values, 50)),
                    float(np.percentile(values, 75))
                ]
            }
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def execute_with_agreement(self, agreement_id, input_data):
        """Execute analysis with blockchain agreement"""
        result = self.sdk.execute_computation_with_agreement(
            agreement_id=agreement_id,
            computation_id=self.computation_id,
            input_data=input_data,
            verification_proofs=True
        )
        return result

def main():
    analyzer = DataAnalyzer()
    
    # Register computations
    computation_id = analyzer.register_computations()
    print(f"Application ready with computation ID: {computation_id}")
    
    # Read agreement ID from environment if available
    agreement_id = os.environ.get("METANODE_AGREEMENT_ID")
    if agreement_id:
        # Test execution with sample data
        test_data = [1.2, 3.4, 5.6, 7.8, 9.0, 2.1, 4.3]
        result = analyzer.execute_with_agreement(agreement_id, test_data)
        print(f"Test execution result: {result}")

if __name__ == "__main__":
    main()
```

Create a requirements file:

```bash
# File: data-analyzer/requirements.txt
metanode-sdk>=1.1.0
numpy>=1.20.0
```

## Step 3: Set Up Testnet Connection

Next, let's set up the connection to the MetaNode testnet:

```bash
metanode-cli testnet data-analyzer --setup
```

This configures your application to connect to the testnet at `http://159.203.17.36:8545`.

## Step 4: Create and Deploy a Blockchain Agreement

Create a new agreement for the application:

```bash
metanode-cli agreement data-analyzer --create
```

Take note of the agreement ID from the output. Let's assume it's `12345678-abcd-1234-efgh-123456789abc`.

Now deploy the agreement to the blockchain:

```bash
metanode-cli agreement data-analyzer --deploy --id 12345678-abcd-1234-efgh-123456789abc
```

Verify the agreement status:

```bash
metanode-cli agreement data-analyzer --verify --id 12345678-abcd-1234-efgh-123456789abc
```

## Step 5: Set Up Verification Proofs

Configure verification proofs to ensure trustless execution:

```bash
metanode-cli testnet data-analyzer --setup-proofs
```

This creates the necessary chainlink.lock files and proof structure.

## Step 6: Deploy the Application

Now we're ready to deploy the application:

```bash
metanode-cli deploy data-analyzer
```

This process:
1. Packages your application code
2. Sets up vPod containers for execution
3. Connects to the testnet
4. Configures the application with your agreement
5. Deploys the application to the MetaNode infrastructure

## Step 7: Check Application Status

Monitor your application's status:

```bash
metanode-cli status data-analyzer
```

## Step 8 (Optional): Create a Node Cluster

To enhance decentralization, create a node cluster:

```bash
metanode-cli cluster data-analyzer --create
```

## Step 9: Execute the Application

Now let's run the application with our deployed agreement. First, save the agreement ID as an environment variable:

```bash
export METANODE_AGREEMENT_ID=12345678-abcd-1234-efgh-123456789abc
```

Then run the application:

```bash
cd data-analyzer
python src/app.py
```

## Step 10: Monitor Agreement Status

Keep track of your agreement execution:

```bash
metanode-cli agreement data-analyzer --status --id 12345678-abcd-1234-efgh-123456789abc
```

## Advanced: Customizing vPod Execution

You can customize how your application runs in vPods by creating a configuration file:

```bash
# File: data-analyzer/metanode_config/vpod_config.json

{
  "vpod_type": "data_analysis",
  "execution_algorithm": "federated_average",
  "resource_limits": {
    "cpu": "1",
    "memory": "1Gi"
  },
  "verification": {
    "proof_type": "chainlink.lock",
    "verification_level": "comprehensive"
  }
}
```

Apply this configuration:

```bash
# Update application deployment with custom vPod configuration
metanode-cli deploy data-analyzer
```

## Executing with Different Datasets

Let's create a script to execute our analysis with different datasets:

```bash
# File: data-analyzer/src/execute_analysis.py

from metanode.full_sdk import MetaNodeSDK
import json
import sys
import os

def main():
    if len(sys.argv) < 3:
        print("Usage: python execute_analysis.py <agreement_id> <data_file>")
        sys.exit(1)
    
    agreement_id = sys.argv[1]
    data_file = sys.argv[2]
    
    # Load data from file
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading data file: {e}")
        sys.exit(1)
    
    # Initialize SDK
    sdk = MetaNodeSDK()
    
    # Load computation ID
    try:
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "metanode_config", 
            "computation.json"
        )
        with open(config_path, "r") as f:
            config = json.load(f)
            computation_id = config.get("computation_id")
            if not computation_id:
                raise ValueError("Computation ID not found")
    except Exception as e:
        print(f"Error loading computation ID: {e}")
        sys.exit(1)
    
    print(f"Executing analysis with agreement ID: {agreement_id}")
    print(f"Computation ID: {computation_id}")
    print(f"Data points: {len(data)}")
    
    # Execute with agreement
    result = sdk.execute_computation_with_agreement(
        agreement_id=agreement_id,
        computation_id=computation_id,
        input_data=data,
        verification_proofs=True
    )
    
    print("\nAnalysis Results:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
```

Create a sample dataset:

```bash
# File: data-analyzer/sample_data.json
[10.2, 15.6, 8.3, 22.1, 17.5, 9.8, 12.4, 14.7, 19.3, 11.6]
```

Execute the analysis:

```bash
cd data-analyzer
python src/execute_analysis.py 12345678-abcd-1234-efgh-123456789abc sample_data.json
```

## Troubleshooting Common Issues

### Connection Issues

If you're having trouble connecting to the testnet:

```bash
# Test connection explicitly
metanode-cli testnet data-analyzer --test

# Reconnect if needed
metanode-cli testnet data-analyzer --setup
```

### Agreement Verification Issues

If agreement verification fails:

```bash
# Check agreement status
metanode-cli agreement data-analyzer --status --id 12345678-abcd-1234-efgh-123456789abc

# Redeploy if needed
metanode-cli agreement data-analyzer --deploy --id 12345678-abcd-1234-efgh-123456789abc
```

### Application Deployment Issues

If application deployment fails:

```bash
# Check application status
metanode-cli status data-analyzer

# Check logs (if available)
cat data-analyzer/metanode_config/deployment.log

# Try redeploying
metanode-cli deploy data-analyzer
```

## Conclusion

You've successfully:
1. Created a new MetaNode application
2. Set up testnet connection
3. Created and deployed a blockchain agreement
4. Configured verification proofs
5. Deployed the application
6. Executed data analysis with blockchain verification

This pattern can be extended to more complex applications, including machine learning models, data processing pipelines, or any computation that benefits from decentralized, trustless execution.

For more information, see the complete [CLI User Guide](/docs/cli-guide/01_cli_complete_guide.md) and the [Dapp Execution Documentation](/docs/dapp-execution/01_dapp_execution_overview.md).

## Next Steps

After completing this tutorial, consider:

1. Customizing the application for your specific use case
2. Exploring advanced verification proof options
3. Implementing more complex execution algorithms
4. Creating custom agreement terms for specific requirements
