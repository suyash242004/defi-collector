"""
Event Extractor - Phase 3
Extracts and formats events from contract ABIs.
"""

import json
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class EventExtractor:
    def __init__(self):
        pass
    
    def extract_events(self, abi: List[Dict[str, Any]]) -> List[str]:
        """Extract and format events from contract ABI."""
        
        if not abi or not isinstance(abi, list):
            logger.warning("Invalid or empty ABI provided")
            return []
        
        events = []
        
        for item in abi:
            if item.get('type') == 'event':
                event_signature = self._format_event_signature(item)
                if event_signature:
                    events.append(event_signature)
        
        logger.info(f"Extracted {len(events)} events from ABI")
        return events
    
    def _format_event_signature(self, event_abi: Dict[str, Any]) -> str:
        """Format event ABI into the required signature format."""
        
        try:
            event_name = event_abi.get('name', '')
            inputs = event_abi.get('inputs', [])
            
            if not event_name:
                return ''
            
            # Format inputs as "name type" pairs
            formatted_inputs = []
            for input_item in inputs:
                param_name = input_item.get('name', '')
                param_type = input_item.get('type', '')
                indexed = input_item.get('indexed', False)
                
                # Include 'indexed' keyword if the parameter is indexed
                if indexed:
                    param_str = f"{param_name} {param_type} indexed"
                else:
                    param_str = f"{param_name} {param_type}"
                
                formatted_inputs.append(param_str)
            
            # Create the final signature
            signature = f"{event_name}({', '.join(formatted_inputs)})"
            return signature
            
        except Exception as e:
            logger.error(f"Error formatting event signature: {str(e)}")
            return ''
    
    def get_event_names(self, abi: List[Dict[str, Any]]) -> List[str]:
        """Extract just the event names from ABI."""
        
        event_names = []
        
        for item in abi:
            if item.get('type') == 'event':
                name = item.get('name')
                if name:
                    event_names.append(name)
        
        return event_names
    
    def get_event_details(self, abi: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract detailed event information from ABI."""
        
        events = []
        
        for item in abi:
            if item.get('type') == 'event':
                event_info = {
                    'name': item.get('name', ''),
                    'signature': self._format_event_signature(item),
                    'inputs': self._process_event_inputs(item.get('inputs', [])),
                    'anonymous': item.get('anonymous', False)
                }
                events.append(event_info)
        
        return events
    
    def _process_event_inputs(self, inputs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process event inputs with additional information."""
        
        processed_inputs = []
        
        for input_item in inputs:
            processed_input = {
                'name': input_item.get('name', ''),
                'type': input_item.get('type', ''),
                'indexed': input_item.get('indexed', False),
                'components': input_item.get('components', [])  # For struct types
            }
            processed_inputs.append(processed_input)
        
        return processed_inputs
    
    def filter_events_by_name(self, abi: List[Dict[str, Any]], event_names: List[str]) -> List[str]:
        """Filter events by specific names."""
        
        all_events = self.extract_events(abi)
        filtered_events = []
        
        for event in all_events:
            event_name = event.split('(')[0]  # Get name part before parentheses
            if event_name in event_names:
                filtered_events.append(event)
        
        return filtered_events
    
    def categorize_events(self, events: List[str]) -> Dict[str, List[str]]:
        """Categorize events by common DeFi patterns."""
        
        categories = {
            'transfer': [],
            'swap': [],
            'lending': [],
            'staking': [],
            'governance': [],
            'bridge': [],
            'other': []
        }
        
        for event in events:
            event_name = event.split('(')[0].lower()
            
            if any(keyword in event_name for keyword in ['transfer', 'send', 'receive']):
                categories['transfer'].append(event)
            elif any(keyword in event_name for keyword in ['swap', 'trade', 'exchange']):
                categories['swap'].append(event)
            elif any(keyword in event_name for keyword in ['deposit', 'withdraw', 'borrow', 'repay', 'lend']):
                categories['lending'].append(event)
            elif any(keyword in event_name for keyword in ['stake', 'unstake', 'reward', 'claim']):
                categories['staking'].append(event)
            elif any(keyword in event_name for keyword in ['vote', 'proposal', 'governance']):
                categories['governance'].append(event)
            elif any(keyword in event_name for keyword in ['bridge', 'lock', 'unlock', 'mint', 'burn']):
                categories['bridge'].append(event)
            else:
                categories['other'].append(event)
        
        return categories
    
    def validate_event_signature(self, signature: str) -> bool:
        """Validate if an event signature is properly formatted."""
        
        try:
            # Basic validation: must have name and parentheses
            if '(' not in signature or ')' not in signature:
                return False
            
            # Extract name and parameters
            name_part = signature.split('(')[0]
            params_part = signature.split('(')[1].split(')')[0]
            
            # Name should not be empty
            if not name_part.strip():
                return False
            
            # If there are parameters, validate basic format
            if params_part.strip():
                # Basic check for parameter format
                params = [p.strip() for p in params_part.split(',')]
                for param in params:
                    if not param or len(param.split()) < 2:
                        return False
            
            return True
            
        except Exception:
            return False