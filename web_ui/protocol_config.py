"""
Protocol configuration for supported DEX protocols.
Maps protocol identifiers to their contract addresses and ABIs.
"""

# Supported protocols with their display names and contract information
SUPPORTED_PROTOCOLS = {
    "uniswap_v3": {
        "name": "Uniswap V3",
        "description": "Uniswap V3 concentrated liquidity positions",
        "position_manager_addresses": {
            "ethereum": "0xC36442b4a4522E871399CD717aBDD847Ab11FE88",
            "arbitrum": "0xC36442b4a4522E871399CD717aBDD847Ab11FE88",
            "base": "0x03a520b32C04BF3bEEf7BEb72E919cf822Ed34f1",
            "polygon": "0xC36442b4a4522E871399CD717aBDD847Ab11FE88",
            "optimism": "0xC36442b4a4522E871399CD717aBDD847Ab11FE88",
        },
        "supported_networks": ["ethereum", "arbitrum", "base", "polygon", "optimism"],
        "position_manager_abi": [
            {
                "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
                "name": "positions",
                "outputs": [
                    {"internalType": "uint96", "name": "nonce", "type": "uint96"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "address", "name": "token0", "type": "address"},
                    {"internalType": "address", "name": "token1", "type": "address"},
                    {"internalType": "uint24", "name": "fee", "type": "uint24"},
                    {"internalType": "int24", "name": "tickLower", "type": "int24"},
                    {"internalType": "int24", "name": "tickUpper", "type": "int24"},
                    {"internalType": "uint128", "name": "liquidity", "type": "uint128"},
                    {"internalType": "uint256", "name": "feeGrowthInside0LastX128", "type": "uint256"},
                    {"internalType": "uint256", "name": "feeGrowthInside1LastX128", "type": "uint256"},
                    {"internalType": "uint128", "name": "tokensOwed0", "type": "uint128"},
                    {"internalType": "uint128", "name": "tokensOwed1", "type": "uint128"},
                ],
                "stateMutability": "view",
                "type": "function",
            }
        ],
    },
    # Add more protocols here as support is added
    # "aerodrome": {
    #     "name": "Aerodrome",
    #     "description": "Aerodrome concentrated liquidity on Base",
    #     "position_manager_addresses": {
    #         "base": "0x...",  # Aerodrome position manager on Base
    #     },
    #     "supported_networks": ["base"],
    #     "position_manager_abi": [...],
    # },
}


def get_protocol_config(protocol: str) -> dict:
    """
    Get configuration for a specific protocol.
    
    Args:
        protocol: Protocol identifier (e.g., 'uniswap_v3')
        
    Returns:
        Protocol configuration dict
        
    Raises:
        ValueError: If protocol is not supported
    """
    if protocol not in SUPPORTED_PROTOCOLS:
        raise ValueError(f"Unsupported protocol: {protocol}. Supported protocols: {list(SUPPORTED_PROTOCOLS.keys())}")
    
    return SUPPORTED_PROTOCOLS[protocol]


def get_position_manager_address(protocol: str, network: str) -> str:
    """
    Get position manager contract address for a protocol on a specific network.
    
    Args:
        protocol: Protocol identifier (e.g., 'uniswap_v3')
        network: Network name (e.g., 'ethereum', 'arbitrum')
        
    Returns:
        Contract address as string
        
    Raises:
        ValueError: If protocol or network is not supported
    """
    config = get_protocol_config(protocol)
    
    if network not in config["position_manager_addresses"]:
        raise ValueError(
            f"Network '{network}' not supported for protocol '{protocol}'. "
            f"Supported networks: {config['supported_networks']}"
        )
    
    return config["position_manager_addresses"][network]


def get_position_manager_abi(protocol: str) -> list:
    """
    Get position manager ABI for a protocol.
    
    Args:
        protocol: Protocol identifier (e.g., 'uniswap_v3')
        
    Returns:
        ABI as list of dicts
        
    Raises:
        ValueError: If protocol is not supported
    """
    config = get_protocol_config(protocol)
    return config["position_manager_abi"]


def get_supported_protocols() -> list:
    """
    Get list of all supported protocol identifiers.
    
    Returns:
        List of protocol identifiers
    """
    return list(SUPPORTED_PROTOCOLS.keys())


def get_protocol_display_name(protocol: str) -> str:
    """
    Get human-readable display name for a protocol.
    
    Args:
        protocol: Protocol identifier (e.g., 'uniswap_v3')
        
    Returns:
        Display name (e.g., 'Uniswap V3')
    """
    config = get_protocol_config(protocol)
    return config["name"]


def get_protocols_for_network(network: str) -> list:
    """
    Get list of protocols that support a specific network.
    
    Args:
        network: Network name (e.g., 'ethereum', 'base')
        
    Returns:
        List of protocol identifiers that support this network
    """
    return [
        protocol_id
        for protocol_id, config in SUPPORTED_PROTOCOLS.items()
        if network in config["supported_networks"]
    ]
