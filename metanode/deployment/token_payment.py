#!/usr/bin/env python3
"""
MetaNode Token Payment System
============================
Handles rental token payments for mainnet connections
"""

import os
import json
import time
from typing import Dict, Any, Optional
from web3 import Web3
from web3.middleware import geth_poa_middleware

class TokenPayment:
    """Manages token payments for mainnet connections"""
    
    def __init__(self, network_config):
        """
        Initialize token payment system
        
        Args:
            network_config: NetworkConfig instance
        """
        self.network_config = network_config
        endpoints = network_config.get_endpoints()
        
        # Initialize Web3 connection
        self.web3 = Web3(Web3.HTTPProvider(endpoints["rpc_url"]))
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        
        # Token contract details
        self.token_contract_address = endpoints["token_contract"]
        
        # ABI for ERC20 token
        self.token_abi = [
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function"
            },
            {
                "constant": False,
                "inputs": [
                    {"name": "_to", "type": "address"},
                    {"name": "_value", "type": "uint256"}
                ],
                "name": "transfer",
                "outputs": [{"name": "success", "type": "bool"}],
                "type": "function"
            }
        ]
        
        # Initialize token contract
        self.token_contract = self.web3.eth.contract(
            address=self.token_contract_address,
            abi=self.token_abi
        )
        
    def get_token_balance(self, wallet_address: str) -> float:
        """
        Get token balance for a wallet address
        
        Args:
            wallet_address: Ethereum wallet address
            
        Returns:
            Token balance as float
        """
        if not self.web3.isAddress(wallet_address):
            raise ValueError(f"Invalid wallet address: {wallet_address}")
            
        raw_balance = self.token_contract.functions.balanceOf(wallet_address).call()
        # Assuming 18 decimals for the token
        balance = raw_balance / 10**18
        return balance
        
    def charge_rental_fee(self, wallet_address: str, private_key: str, rental_hours: int) -> Dict[str, Any]:
        """
        Charge rental fee for mainnet connection
        
        Args:
            wallet_address: User's wallet address
            private_key: Private key for the wallet
            rental_hours: Number of hours to rent mainnet connection
            
        Returns:
            Transaction receipt
        """
        if not self.network_config.use_mainnet:
            return {"status": "skipped", "reason": "Only charged on mainnet"}
            
        # Calculate fee (0.1 token per hour)
        hourly_rate = 0.1
        fee = rental_hours * hourly_rate
        fee_wei = int(fee * 10**18)  # Convert to wei
        
        # MetaNode treasury address
        treasury_address = "0x7F8cD874F5fC2E7f20C3519f9B385d2C7C552f3C"
        
        # Check balance
        balance = self.get_token_balance(wallet_address)
        if balance < fee:
            raise ValueError(f"Insufficient token balance. Need {fee}, have {balance}")
            
        # Build transaction
        nonce = self.web3.eth.getTransactionCount(wallet_address)
        tx = self.token_contract.functions.transfer(
            treasury_address,
            fee_wei
        ).buildTransaction({
            'chainId': 1,  # Ethereum mainnet
            'gas': 100000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': nonce
        })
        
        # Sign and send transaction
        signed_tx = self.web3.eth.account.signTransaction(tx, private_key)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        
        # Wait for receipt
        receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        
        return {
            "status": "success",
            "transaction_hash": receipt.transactionHash.hex(),
            "amount_charged": fee,
            "rental_hours": rental_hours,
            "timestamp": int(time.time())
        }
