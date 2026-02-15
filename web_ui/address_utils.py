"""
Utility functions for blockchain address normalization and handling.
"""

def normalize_address_for_storage(address: str, network: str) -> str:
    """
    Normalize blockchain address for database storage.
    
    EVM chains (ethereum, arbitrum, base, polygon, optimism):
    - Lowercase for consistent matching (ERC-20 addresses are case-insensitive)
    
    Non-EVM chains (solana):
    - Preserve original case (case-sensitive addresses)
    
    Args:
        address: Blockchain address string
        network: Network identifier (ethereum, arbitrum, base, polygon, optimism, solana, etc.)
    
    Returns:
        Normalized address string suitable for database storage
    
    Examples:
        >>> normalize_address_for_storage("0xAbC123", "ethereum")
        "0xabc123"
        >>> normalize_address_for_storage("SomeBase58Address", "solana")
        "SomeBase58Address"
    """
    if not address:
        return address
    
    # EVM networks use case-insensitive addresses (EIP-55 checksum is optional)
    EVM_NETWORKS = {'ethereum', 'arbitrum', 'base', 'polygon', 'optimism'}
    
    if network.lower() in EVM_NETWORKS:
        return address.lower()
    
    # Non-EVM networks (e.g., Solana) are case-sensitive
    # Return address unchanged to preserve original case
    return address
