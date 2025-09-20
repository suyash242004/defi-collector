# DeFi Protocol Contract & Events Collector

This project collects contract addresses, ABIs, and events from DeFi protocols across multiple blockchain networks.

## 📊 Data Flow

### Phase 1: Contract Discovery

- Input: Protocol name + network from CSV
- Process: Search known contracts, protocol docs, APIs
- Output: List of contract addresses with names

### Phase 2: ABI Retrieval

- Input: Contract addresses + network
- Process: Query block explorer APIs for verified contracts
- Output: Contract ABIs (JSON format)

### Phase 3: Event Extraction

- Input: Contract ABIs
- Process: Parse ABI JSON, extract only events
- Output: Formatted event signatures

## 🔧 Configuration

### API Rate Limits

The script respects API rate limits:

- Etherscan: 5 requests/second
- Other explorers: 3-5 requests/second
- Concurrent requests: Limited to 5

### Network Support

Currently supports:

- Ethereum
- Polygon
- Arbitrum
- Optimism
- BNB Smart Chain
- Avalanche
- Fantom
- Base
- zkSync Era

### Fallback Mechanisms

1. **No API Keys**: Uses sample ABI data
2. **Unverified Contracts**: Marks as unverified, no events
3. **Unknown Protocols**: Generates placeholder contracts
4. **API Failures**: Retries with exponential backoff

## 📝 Output Files

### Main Output: `defi_protocols_contracts_events.json`

Complete dataset with all collected information.

### Summary: `collection_summary.json`

```json
{
  "total_contracts": 150,
  "verified_contracts": 120,
  "unverified_contracts": 30,
  "total_events": 450,
  "protocols_processed": 50,
  "networks_covered": ["ethereum", "polygon", "arbitrum"],
  "categories_covered": ["dexs", "lending", "bridge"]
}
```

### Logs: `data/collector.log`

Detailed execution logs with timestamps and error messages.

## 🛠 Customization

### Adding New Networks

Edit `config.py` to add new network configurations:

```python
NETWORKS['new_network'] = {
    'name': 'New Network',
    'chain_id': 123,
    'native_token': 'NEW',
    'explorer': 'newscan.io'
}

EXPLORER_URLS['new_network'] = 'https://api.newscan.io/api'
```

### Adding Known Contracts

Edit `contract_finder.py` to add known contract addresses:

```python
self.known_contracts['protocol_network'] = [
    {'address': '0x...', 'name': 'ContractName'}
]
```

### Custom Event Filtering

Modify `event_extractor.py` to filter specific event types:

```python
def filter_swap_events(self, events):
    return [e for e in events if 'swap' in e.lower()]
```

## 🔍 Troubleshooting

### Common Issues

1. **No contracts found for protocol**

   - Check protocol name spelling in CSV
   - Add known contracts manually in `contract_finder.py`

2. **API rate limit exceeded**

   - Reduce `CONCURRENT_REQUESTS` in config
   - Add delays between requests

3. **Empty events list**
   - Contract might not be verified
   - ABI might not contain events
   - Check logs for detailed errors

### Debug Mode

Enable detailed logging by setting log level to DEBUG in `config.py`.

## 📋 Assignment Checklist

- [x] ✅ Load protocols from CSV file
- [x] ✅ Find contract addresses for each protocol+network pair
- [x] ✅ Fetch ABIs from block explorers
- [x] ✅ Extract events from ABIs in required format
- [x] ✅ Include contract names in output
- [x] ✅ Handle verified/unverified contracts
- [x] ✅ Export final JSON with all required fields
- [x] ✅ Generate summary statistics
- [x] ✅ Proper error handling and logging

## 🎯 Key Features

- **Async Processing**: Fast concurrent API calls
- **Rate Limiting**: Respects API limits
- **Fallback Data**: Works without API keys
- **Error Recovery**: Continues on individual failures
- **Progress Tracking**: Shows collection progress
- **Intermediate Saves**: Backup saves every 10 protocols
- **Comprehensive Logging**: Detailed execution logs

## 🚀 Quick Start

1. Clone/download all files
2. Install requirements: `pip install -r requirements.txt`
3. Place your `protocols.csv` in the root directory
4. Run: `python main.py`
5. Find results in `data/defi_protocols_contracts_events.json`

## 📞 Support

For issues or questions:

1. Check logs in `data/collector.log`
2. Verify CSV format matches expected structure
3. Ensure network connectivity for API calls
4. Review configuration in `config.py`📁 Project Structure

```
defi-collector/
├── main.py                 # Main execution script
├── contract_finder.py      # Phase 1: Find contract addresses
├── abi_fetcher.py          # Phase 2: Fetch contract ABIs
├── event_extractor.py      # Phase 3: Extract events from ABIs
├── utils.py                # Utility functions
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── protocols.csv           # Input CSV with protocol data
├── README.md              # This documentation
├── data/                  # Output directory
│   ├── defi_protocols_contracts_events.json  # Final output
│   ├── collection_summary.json               # Summary statistics
│   ├── intermediate_results_*.json           # Backup saves
│   └── collector.log                          # Execution logs
└── logs/                  # Additional logs
```

## 🚀 Setup & Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys (Optional but Recommended)

Set environment variables for block explorer API keys:

```bash
export ETHERSCAN_API_KEY="your_etherscan_api_key"
export POLYGONSCAN_API_KEY="your_polygonscan_api_key"
export BSCSCAN_API_KEY="your_bscscan_api_key"
export ARBISCAN_API_KEY="your_arbiscan_api_key"
export OPTIMISTIC_API_KEY="your_optimistic_api_key"
export SNOWTRACE_API_KEY="your_snowtrace_api_key"
export FTMSCAN_API_KEY="your_ftmscan_api_key"
export BASESCAN_API_KEY="your_basescan_api_key"
```

**Note:** The script will work without API keys using fallback data, but real API keys provide access to actual contract ABIs.

### 3. Prepare Input Data

Ensure your `protocols.csv` file exists with the required format:

```csv
protocol,category,network
aave,lending,ethereum
uniswap,dexs,ethereum
axelar,bridge,injective
jupiter_staked_sol,liquid_staking,solana
prdt,prediction_market,polygon
```

If the CSV doesn't exist, the script will create a sample one automatically.

## 🎯 Usage

### Run Complete Collection

```bash
python main.py
```

This will:

1. Load protocols from `protocols.csv`
2. Find contract addresses for each protocol
3. Fetch ABIs from block explorers
4. Extract events from ABIs
5. Save results to `data/defi_protocols_contracts_events.json`

### Expected Output Format

```json
[
  {
    "protocol": "aave",
    "category": "lending",
    "network": "ethereum",
    "contract_address": "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9",
    "contract_name": "LendingPool",
    "verified": "yes",
    "events": [
      "Deposit(reserve address indexed, user address, onBehalfOf address indexed, amount uint256, referral uint16 indexed)",
      "Withdraw(reserve address indexed, user address indexed, to address indexed, amount uint256)",
      "Borrow(reserve address indexed, user address, onBehalfOf address indexed, amount uint256, borrowRateMode uint256, borrowRate uint256, referral uint16 indexed)"
    ]
  }
]
```

##
