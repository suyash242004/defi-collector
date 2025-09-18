#!/usr/bin/env python3
"""
DeFi Protocol Contract & Events Collector
Main script to collect contract addresses, ABIs, and events from DeFi protocols.
"""

import csv
import json
import asyncio
import aiohttp
import time
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging
import config

from contract_finder import ContractFinder
from abi_fetcher import ABIFetcher
from event_extractor import EventExtractor
from utils import setup_logging, save_json, load_csv

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

class DefiContractCollector:
    def __init__(self):
        self.contract_finder = ContractFinder()
        self.abi_fetcher = ABIFetcher()
        self.event_extractor = EventExtractor()
        self.results = []
        
    async def process_protocol(self, protocol_data: Dict[str, str]) -> List[Dict[str, Any]]:
        """Process a single protocol and return contract data with events."""
        protocol = protocol_data['protocol']
        network = protocol_data['network']
        category = protocol_data['category']
        
        logger.info(f"Processing {protocol} on {network}")
        
        try:
            # Phase 1: Find contract addresses
            contracts = await self.contract_finder.find_contracts(protocol, network)
            
            if not contracts:
                logger.warning(f"No contracts found for {protocol} on {network}")
                return []
            
            protocol_results = []
            
            for contract in contracts:
                contract_address = contract['address']
                contract_name = contract['name']
                
                logger.info(f"Processing contract {contract_name}: {contract_address}")
                
                try:
                    # Phase 2: Fetch ABI
                    abi_data = await self.abi_fetcher.fetch_abi(contract_address, network)
                    
                    if abi_data and abi_data.get('verified', False):
                        # Phase 3: Extract events
                        events = self.event_extractor.extract_events(abi_data['abi'])
                        
                        result = {
                            'protocol': protocol,
                            'category': category,
                            'network': network,
                            'contract_address': contract_address,
                            'contract_name': contract_name,
                            'verified': 'yes',
                            'events': events
                        }
                    else:
                        result = {
                            'protocol': protocol,
                            'category': category,
                            'network': network,
                            'contract_address': contract_address,
                            'contract_name': contract_name,
                            'verified': 'no',
                            'events': []
                        }
                    
                    protocol_results.append(result)
                    logger.info(f"✅ Processed {contract_name} - {len(result['events'])} events found")
                    
                except Exception as e:
                    logger.error(f"Error processing contract {contract_address}: {str(e)}")
                    # Still add unverified entry
                    protocol_results.append({
                        'protocol': protocol,
                        'category': category,
                        'network': network,
                        'contract_address': contract_address,
                        'contract_name': contract_name,
                        'verified': 'no',
                        'events': []
                    })
                
                # Rate limiting
                await asyncio.sleep(0.5)
            
            return protocol_results
            
        except Exception as e:
            logger.error(f"Error processing protocol {protocol}: {str(e)}")
            return []
    
    async def collect_all_protocols(self, csv_file_path: str) -> None:
        """Main function to collect data for all protocols from CSV."""
        logger.info("Starting DeFi protocol data collection...")
        
        # Load protocols from CSV
        protocols = load_csv(csv_file_path)
        logger.info(f"Loaded {len(protocols)} protocols from CSV")
        
        # Process each protocol
        all_results = []
        for i, protocol_data in enumerate(protocols, 1):
            network = protocol_data['network']
            # Skip unsupported networks
            if network not in config.NETWORKS:
                logger.warning(f"Skipping unsupported network: {network} for {protocol_data['protocol']}")
                continue
            logger.info(f"Progress: {i}/{len(protocols)} - {protocol_data['protocol']}")
            
            protocol_results = await self.process_protocol(protocol_data)
            all_results.extend(protocol_results)
            
            # Save intermediate results every 10 protocols
            if i % 500 == 0:
                save_json(all_results, f'data/intermediate_results_{int(time.time())}.json')
                logger.info(f"Saved intermediate results for {i} protocols")
        
        # Save final results
        output_file = 'data/defi_protocols_contracts_events.json'
        save_json(all_results, output_file)
        
        # Generate summary
        self.generate_summary(all_results)
        
        logger.info(f"✅ Collection complete! Results saved to {output_file}")
        logger.info(f"Total contracts collected: {len(all_results)}")
        
    def generate_summary(self, results: List[Dict[str, Any]]) -> None:
        """Generate summary statistics."""
        summary = {
            'total_contracts': len(results),
            'verified_contracts': len([r for r in results if r['verified'] == 'yes']),
            'unverified_contracts': len([r for r in results if r['verified'] == 'no']),
            'total_events': sum(len(r['events']) for r in results),
            'protocols_processed': len(set(r['protocol'] for r in results)),
            'networks_covered': list(set(r['network'] for r in results)),
            'categories_covered': list(set(r['category'] for r in results))
        }
        
        save_json(summary, 'data/collection_summary.json')
        
        # Print summary
        print("\n" + "="*50)
        print("COLLECTION SUMMARY")
        print("="*50)
        print(f"Total Contracts: {summary['total_contracts']}")
        print(f"Verified: {summary['verified_contracts']}")
        print(f"Unverified: {summary['unverified_contracts']}")
        print(f"Total Events: {summary['total_events']}")
        print(f"Protocols: {summary['protocols_processed']}")
        print(f"Networks: {len(summary['networks_covered'])}")
        print(f"Categories: {len(summary['categories_covered'])}")

async def main():
    """Main execution function."""
    collector = DefiContractCollector()
    
    # Create data directory if it doesn't exist
    Path('data').mkdir(exist_ok=True)
    
    # Run collection
    await collector.collect_all_protocols('protocols.csv')

if __name__ == "__main__":
    asyncio.run(main())