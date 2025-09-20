"""
Configuration settings for the DeFi contract collector.
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
LOGS_DIR = BASE_DIR / 'logs'

# File paths
CSV_INPUT_FILE = BASE_DIR / 'protocols.csv'
OUTPUT_JSON_FILE = DATA_DIR / 'defi_protocols_contracts_events.json'
SUMMARY_FILE = DATA_DIR / 'collection_summary.json'
LOG_FILE = LOGS_DIR / 'collector.log'

# API Configuration
API_RATE_LIMITS = {
    'etherscan': 5,  # requests per second
    'polygonscan': 5,
    'bscscan': 5,
    'arbiscan': 5,
    'default': 3
}

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

# Request timeouts
REQUEST_TIMEOUT = 30  # seconds
CONCURRENT_REQUESTS = 5  # max concurrent requests

# API Keys (set these as environment variables)
API_KEYS = {
    'ETHERSCAN_API_KEY': os.getenv('ETHERSCAN_API_KEY', ''),
    'POLYGONSCAN_API_KEY': os.getenv('POLYGONSCAN_API_KEY', ''),
    'BSCSCAN_API_KEY': os.getenv('BSCSCAN_API_KEY', ''),
    'ARBISCAN_API_KEY': os.getenv('ARBISCAN_API_KEY', ''),
    'OPTIMISTIC_API_KEY': os.getenv('OPTIMISTIC_API_KEY', ''),
    'SNOWTRACE_API_KEY': os.getenv('SNOWTRACE_API_KEY', ''),
    'FTMSCAN_API_KEY': os.getenv('FTMSCAN_API_KEY', ''),
    'BASESCAN_API_KEY': os.getenv('BASESCAN_API_KEY', '')
}

# Block Explorer URLs
EXPLORER_URLS = {
    'ethereum': 'https://api.etherscan.io/api',
    'polygon': 'https://api.polygonscan.com/api',
    'bsc': 'https://api.bscscan.com/api',
    'arbitrum': 'https://api.arbiscan.io/api',
    'optimism': 'https://api-optimistic.etherscan.io/api',
    'avalanche': 'https://api.snowtrace.io/api',
    'fantom': 'https://api.ftmscan.com/api',
    'base': 'https://api.basescan.org/api',
    'zksync_era': 'https://api-era.zksync.network/api'
}

# Protocol documentation URLs (for manual contract finding)
PROTOCOL_DOCS = {
    'aave': 'https://docs.aave.com/developers/deployed-contracts/deployed-contracts',
    'uniswap': 'https://docs.uniswap.org/contracts/v3/reference/deployments',
    'compound': 'https://compound.finance/docs#networks',
    'sushiswap': 'https://dev.sushi.com/docs/Developers/Deployment%20Addresses',
    'curve': 'https://curve.readthedocs.io/registry-address-provider.html',
    'balancer': 'https://docs.balancer.fi/reference/contracts/deployment-addresses.html'
}

# Network configurations
NETWORKS = {
    'ethereum': {
        'name': 'Ethereum Mainnet',
        'chain_id': 1,
        'native_token': 'ETH',
        'explorer': 'etherscan.io'
    },
    'polygon': {
        'name': 'Polygon',
        'chain_id': 137,
        'native_token': 'MATIC',
        'explorer': 'polygonscan.com'
    },
    'arbitrum': {
        'name': 'Arbitrum One',
        'chain_id': 42161,
        'native_token': 'ETH',
        'explorer': 'arbiscan.io'
    },
    'optimism': {
        'name': 'Optimism',
        'chain_id': 10,
        'native_token': 'ETH',
        'explorer': 'optimistic.etherscan.io'
    },
    'bsc': {
        'name': 'BNB Smart Chain',
        'chain_id': 56,
        'native_token': 'BNB',
        'explorer': 'bscscan.com'
    },
    'avalanche': {
        'name': 'Avalanche C-Chain',
        'chain_id': 43114,
        'native_token': 'AVAX',
        'explorer': 'snowtrace.io'
    },
    'fantom': {
        'name': 'Fantom',
        'chain_id': 250,
        'native_token': 'FTM',
        'explorer': 'ftmscan.com'
    },
    'base': {
        'name': 'Base',
        'chain_id': 8453,
        'native_token': 'ETH',
        'explorer': 'basescan.org'
    }
}

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': str(LOG_FILE),
            'encoding': 'utf-8',
            'formatter': 'detailed'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}