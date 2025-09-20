
"""
Utility functions for the DeFi contract collector.
"""

import csv
import json
import logging
import os
from pathlib import Path
from typing import List, Dict, Any

def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('data/collector.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    # Create data directory if it doesn't exist
    Path('data').mkdir(exist_ok=True)

def load_csv(file_path: str) -> List[Dict[str, str]]:
    """Load protocols from CSV file."""
    protocols = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Clean up the row data
                cleaned_row = {k.strip(): v.strip() for k, v in row.items()}
                protocols.append(cleaned_row)
        
        print(f"Loaded {len(protocols)} protocols from {file_path}")
        return protocols
        
    except FileNotFoundError:
        print(f"CSV file not found: {file_path}")
        print("Creating sample CSV file...")
        create_sample_csv(file_path)
        return load_csv(file_path)
    
    except Exception as e:
        print(f"Error loading CSV: {str(e)}")
        return []

def create_sample_csv(file_path: str):
    """Create a sample CSV file with protocol data."""
    sample_data = [
        {'protocol': 'aave', 'category': 'lending', 'network': 'ethereum'},
        {'protocol': 'uniswap', 'category': 'dexs', 'network': 'ethereum'},
        {'protocol': 'compound', 'category': 'lending', 'network': 'ethereum'},
        {'protocol': 'sushiswap', 'category': 'dexs', 'network': 'polygon'},
        {'protocol': 'curve', 'category': 'dexs', 'network': 'ethereum'},
        {'protocol': 'makerdao', 'category': 'cdp', 'network': 'ethereum'},
        {'protocol': 'pancakeswap', 'category': 'dexs', 'network': 'bsc'},
        {'protocol': 'velodrome_v2', 'category': 'dexs', 'network': 'optimism'},
        {'protocol': 'axelar', 'category': 'bridge', 'network': 'cosmos'},
        {'protocol': 'jupiter_staked_sol', 'category': 'liquid_staking', 'network': 'solana'},
        {'protocol': 'multichain', 'category': 'bridge', 'network': 'ethereum'},
        {'protocol': 'increment_protocol', 'category': 'derivatives', 'network': 'zksync_era'},
        {'protocol': 'virtuals_protocol', 'category': 'ai_agents', 'network': 'base'},
        {'protocol': 'prdt', 'category': 'prediction_market', 'network': 'polygon'},
        {'protocol': 'vaultcraft', 'category': 'yield', 'network': 'ethereum'}
    ]
    
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['protocol', 'category', 'network']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sample_data)
    
    print(f"Created sample CSV file: {file_path}")

def save_json(data: Any, file_path: str):
    """Save data to JSON file."""
    try:
        # Ensure directory exists
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        
        print(f"Saved data to {file_path}")
        
    except Exception as e:
        print(f"Error saving JSON to {file_path}: {str(e)}")

def load_json(file_path: str) -> Any:
    """Load data from JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"JSON file not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error loading JSON from {file_path}: {str(e)}")
        return None

def validate_address(address: str) -> bool:
    """Validate if a string is a valid Ethereum-like address."""
    if not address or not isinstance(address, str):
        return False
    
    # Remove '0x' prefix if present
    if address.startswith('0x'):
        address = address[2:]
    
    # Check if it's 40 characters of hexadecimal
    if len(address) != 40:
        return False
    
    try:
        int(address, 16)
        return True
    except ValueError:
        return False

def clean_protocol_name(protocol: str) -> str:
    """Clean and normalize protocol names."""
    if not protocol:
        return ""
    
    # Convert to lowercase and replace special characters
    cleaned = protocol.lower().replace('-', '_').replace(' ', '_')
    
    # Remove version suffixes for consistency
    version_suffixes = ['_v1', '_v2', '_v3', '_2', '_3']
    for suffix in version_suffixes:
        if cleaned.endswith(suffix):
            cleaned = cleaned[:-len(suffix)]
    
    return cleaned

def get_network_info(network: str) -> Dict[str, Any]:
    """Get information about blockchain networks."""
    network_info = {
        'ethereum': {
            'name': 'Ethereum',
            'chain_id': 1,
            'explorer': 'https://etherscan.io',
            'api': 'https://api.etherscan.io/api'
        },
        'polygon': {
            'name': 'Polygon',
            'chain_id': 137,
            'explorer': 'https://polygonscan.com',
            'api': 'https://api.polygonscan.com/api'
        },
        'arbitrum': {
            'name': 'Arbitrum One',
            'chain_id': 42161,
            'explorer': 'https://arbiscan.io',
            'api': 'https://api.arbiscan.io/api'
        },
        'optimism': {
            'name': 'Optimism',
            'chain_id': 10,
            'explorer': 'https://optimistic.etherscan.io',
            'api': 'https://api-optimistic.etherscan.io/api'
        },
        'bsc': {
            'name': 'BNB Smart Chain',
            'chain_id': 56,
            'explorer': 'https://bscscan.com',
            'api': 'https://api.bscscan.com/api'
        },
        'avalanche': {
            'name': 'Avalanche C-Chain',
            'chain_id': 43114,
            'explorer': 'https://snowtrace.io',
            'api': 'https://api.snowtrace.io/api'
        },
        'fantom': {
            'name': 'Fantom',
            'chain_id': 250,
            'explorer': 'https://ftmscan.com',
            'api': 'https://api.ftmscan.com/api'
        },
        'base': {
            'name': 'Base',
            'chain_id': 8453,
            'explorer': 'https://basescan.org',
            'api': 'https://api.basescan.org/api'
        },
        'zksync_era': {
            'name': 'zkSync Era',
            'chain_id': 324,
            'explorer': 'https://explorer.zksync.io',
            'api': 'https://api-era.zksync.network/api'
        }
    }
    
    return network_info.get(network.lower(), {
        'name': network.title(),
        'chain_id': None,
        'explorer': None,
        'api': None
    })

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    size = size_bytes
    i = 0
    
    while size >= 1024 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1
    
    return f"{size:.1f}{size_names[i]}"

def create_directory_structure():
    """Create necessary directory structure for the project."""
    directories = [
        'data',
        'data/abis',
        'data/contracts',
        'data/logs',
        'logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

def export_to_csv(data: List[Dict], filename: str):
    """Export results to CSV format."""
    if not data:
        print("No data to export")
        return
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in data:
                # Convert lists to strings for CSV compatibility
                csv_row = {}
                for key, value in row.items():
                    if isinstance(value, list):
                        csv_row[key] = '; '.join(map(str, value))
                    else:
                        csv_row[key] = value
                writer.writerow(csv_row)
        
        print(f"Exported data to CSV: {filename}")
        
    except Exception as e:
        print(f"Error exporting to CSV: {str(e)}")