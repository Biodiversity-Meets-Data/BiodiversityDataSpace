#!/usr/bin/env python3
"""
Species Identifier Resolution Service - Command Line Interface

This tool dynamically resolves species identifiers across multiple databases:
- EU Birds Directive codes (via EEA EUNIS JSON API)
- GBIF Backbone Taxonomy
- ChecklistBank (Catalogue of Life)
- Global Names Verifier (100+ databases)
- EUNIS, IUCN, Wikidata, iNaturalist, and more

Usage:
    python species_resolver.py "A072"
    python species_resolver.py "Pernis apivorus"
    python species_resolver.py "Falco apivorus" --refresh-cache
"""

import requests
import json
import sys
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict
import argparse
from pathlib import Path
import time

# Cache file for EEA policy codes
CACHE_FILE = Path.home() / '.species_resolver_cache.json'

@dataclass
class SpeciesIdentity:
    """Complete species identity across multiple databases"""
    query: str
    scientific_name: str
    canonical_name: Optional[str] = None
    authorship: Optional[str] = None
    policy_code: Optional[str] = None
    eunis_url: Optional[str] = None
    common_names: Optional[List[str]] = None
    
    # GBIF identifiers
    gbif_usage_key: Optional[int] = None
    gbif_nub_key: Optional[int] = None
    gbif_confidence: Optional[int] = None
    gbif_match_type: Optional[str] = None
    gbif_status: Optional[str] = None
    
    # Classification
    kingdom: Optional[str] = None
    phylum: Optional[str] = None
    class_name: Optional[str] = None
    order: Optional[str] = None
    family: Optional[str] = None
    genus: Optional[str] = None
    
    # ChecklistBank
    checklistbank_id: Optional[str] = None
    
    # Global Names Verifier results
    gnv_sources: Optional[Dict] = None
    
    # External identifiers
    wikidata_id: Optional[str] = None
    iucn_id: Optional[str] = None
    eunis_code: Optional[str] = None


class PolicyCodeCache:
    """Cache for EEA EUNIS policy code mappings"""
    
    def __init__(self):
        self.cache = self._load_cache()
        self.cache_age_hours = 24 * 7  # Refresh weekly
    
    def _load_cache(self) -> Dict:
        """Load cache from disk"""
        if CACHE_FILE.exists():
            try:
                with open(CACHE_FILE, 'r') as f:
                    data = json.load(f)
                    # Check if cache is recent
                    cache_time = data.get('timestamp', 0)
                    if time.time() - cache_time < self.cache_age_hours * 3600:
                        print(f"Loaded {len(data.get('codes', {}))} policy codes from cache")
                        return data
            except Exception as e:
                print(f"Cache load failed: {e}")
        return {'codes': {}, 'timestamp': 0}
    
    def _save_cache(self):
        """Save cache to disk"""
        try:
            self.cache['timestamp'] = time.time()
            with open(CACHE_FILE, 'w') as f:
                json.dump(self.cache, f)
            print(f"Saved {len(self.cache['codes'])} policy codes to cache")
        except Exception as e:
            print(f"Cache save failed: {e}")
    
    def fetch_from_eea(self) -> Dict:
        """
        Fetch policy codes from EEA JSON API
        Using: https://www.eea.europa.eu/data-and-maps/daviz/sds/list-of-eunis-species-with-1/daviz.json
        """
        print("\nFetching policy codes from EEA EUNIS database...")
        
        urls = [
            # All species with N2000 codes (3311 species)
            "https://www.eea.europa.eu/data-and-maps/daviz/sds/list-of-eunis-species-with-1/daviz.json",
        ]
        
        codes = {}
        for url in urls:
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                # Parse the EEA JSON structure
                items = data.get('items', [])
                print(f"Retrieved {len(items)} species records from EEA")
                
                for item in items:
                    n2000_code = item.get('o', '').strip()
                    scientific_name = item.get('name', '').strip()
                    authorship = item.get('author', '').strip()
                    eunis_url = item.get('s', '').strip()
                    
                    if n2000_code and scientific_name:
                        codes[n2000_code] = {
                            'scientific_name': scientific_name,
                            'authorship': authorship,
                            'eunis_url': eunis_url,
                            'natura2000': n2000_code
                        }
                
            except Exception as e:
                print(f"Failed to fetch from {url}: {e}")
        
        if codes:
            self.cache['codes'] = codes
            self._save_cache()
        
        return codes
    
    def get(self, code: str) -> Optional[Dict]:
        """Get policy code info, fetching if needed"""
        code_upper = code.upper().strip()
        
        if not self.cache['codes']:
            self.fetch_from_eea()
        
        return self.cache['codes'].get(code_upper)
    
    def get_by_name(self, scientific_name: str) -> Optional[Dict]:
        """Get policy code info by scientific name"""
        if not self.cache['codes']:
            self.fetch_from_eea()
        
        # Search for matching scientific name (case-insensitive)
        name_lower = scientific_name.lower().strip()
        for code, info in self.cache['codes'].items():
            if info['scientific_name'].lower() == name_lower:
                return info
        
        return None
    
    def refresh(self):
        """Force refresh from EEA"""
        self.cache = {'codes': {}, 'timestamp': 0}
        self.fetch_from_eea()


class SpeciesResolver:
    """Main resolver class for species identifiers"""
    
    def __init__(self, policy_cache: PolicyCodeCache):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SpeciesResolverCLI/2.0 (Educational/Research)'
        })
        self.policy_cache = policy_cache
    
    def resolve(self, query: str) -> SpeciesIdentity:
        """
        Main resolution method that orchestrates all API calls
        """
        print(f"\nResolving: {query}")
        print("=" * 60)
        
        # Step 1: Check if it's a policy code (query EEA dynamically)
        scientific_name, policy_info = self._resolve_policy_code(query)
        
        # Step 2: Query GBIF
        print("\nQuerying GBIF Backbone Taxonomy...")
        gbif_data = self._query_gbif(scientific_name)
        
        # Step 3: Query ChecklistBank
        print("Querying ChecklistBank (Catalogue of Life)...")
        clb_data = self._query_checklistbank(gbif_data.get('usageKey'))
        
        # Step 4: Query Global Names Verifier
        print("Querying Global Names Verifier (100+ databases)...")
        gnv_data = self._query_global_names(scientific_name)
        
        # Build complete identity
        identity = self._build_identity(
            query, scientific_name, policy_info, 
            gbif_data, clb_data, gnv_data
        )
        
        return identity
    
    def _resolve_policy_code(self, query: str) -> tuple:
        """Check if query is a policy code and resolve via EEA API"""
        upper_query = query.upper().strip()
        
        # Check if it looks like a policy code (e.g., A072, 1234)
        if upper_query.startswith('A') or upper_query.isdigit():
            print(f"Checking if '{upper_query}' is an EEA/EUNIS policy code...")
            policy_info = self.policy_cache.get(upper_query)
            
            if policy_info:
                print(f"Recognized EEA policy code: {upper_query}")
                print(f"  -> {policy_info['scientific_name']} {policy_info.get('authorship', '')}")
                if policy_info.get('eunis_url'):
                    print(f"  -> EUNIS: {policy_info['eunis_url']}")
                return policy_info['scientific_name'], policy_info
        
        # If not a policy code format, try searching by scientific name in EEA database
        print(f"Checking if '{query}' exists in EEA/EUNIS policy database...")
        policy_info = self.policy_cache.get_by_name(query)
        
        if policy_info:
            print(f"Found in EEA database with policy code: {policy_info['natura2000']}")
            print(f"  -> {policy_info['scientific_name']} {policy_info.get('authorship', '')}")
            if policy_info.get('eunis_url'):
                print(f"  -> EUNIS: {policy_info['eunis_url']}")
            return query, policy_info
        
        return query, None
    
    def _query_gbif(self, scientific_name: str) -> Dict:
        """Query GBIF Species Match API"""
        try:
            url = "https://api.gbif.org/v1/species/match"
            params = {
                'name': scientific_name,
                'verbose': 'true'
            }
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('usageKey'):
                print(f"GBIF match: {data.get('scientificName')}")
                print(f"  Match type: {data.get('matchType')} ({data.get('confidence')}% confidence)")
                print(f"  Status: {data.get('status')}, Rank: {data.get('rank')}")
                return data
            else:
                print("No GBIF match found")
                return {}
        except Exception as e:
            print(f"GBIF query failed: {e}")
            return {}
    
    def _query_checklistbank(self, usage_key: Optional[int]) -> Dict:
        """Query ChecklistBank API"""
        if not usage_key:
            return {}
        
        try:
            url = f"https://api.checklistbank.org/dataset/3/nameusage/{usage_key}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            print(f"ChecklistBank ID: {data.get('id')}")
            return data
        except Exception as e:
            print(f"ChecklistBank query failed: {e}")
            return {}
    
    def _query_global_names(self, scientific_name: str) -> Dict:
        """Query Global Names Verifier API"""
        try:
            url = "https://verifier.globalnames.org/api/v1/verifications"
            payload = {
                "nameStrings": [scientific_name],
                "preferredSources": [1, 11, 158, 163, 180, 207]  
                # CoL, GBIF, EUNIS, IUCN, iNaturalist, Wikidata
            }
            response = self.session.post(url, json=payload, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if data.get('names') and len(data['names']) > 0:
                results = data['names'][0].get('results', [])
                print(f"Global Names Verifier: {len(results)} source matches")
                return data['names'][0]
            else:
                print("No Global Names matches")
                return {}
        except Exception as e:
            print(f"Global Names query failed: {e}")
            return {}
    
    def _build_identity(self, query: str, scientific_name: str, 
                       policy_info: Optional[Dict], gbif_data: Dict,
                       clb_data: Dict, gnv_data: Dict) -> SpeciesIdentity:
        """Build complete species identity from all API responses"""
        
        # Extract GNV sources
        gnv_sources = {}
        if gnv_data.get('results'):
            for result in gnv_data['results']:
                source_name = result.get('dataSourceTitleShort') or result.get('dataSourceTitle')
                gnv_sources[source_name] = {
                    'record_id': result.get('recordId'),
                    'url': result.get('outlink'),
                    'match_type': result.get('matchType'),
                    'score': result.get('score')
                }
        
        return SpeciesIdentity(
            query=query,
            scientific_name=gbif_data.get('scientificName', scientific_name),
            canonical_name=gbif_data.get('canonicalName'),
            authorship=gbif_data.get('authorship') or (policy_info.get('authorship') if policy_info else None),
            policy_code=policy_info.get('natura2000') if policy_info else None,
            eunis_url=policy_info.get('eunis_url') if policy_info else None,
            gbif_usage_key=gbif_data.get('usageKey'),
            gbif_nub_key=gbif_data.get('nubKey'),
            gbif_confidence=gbif_data.get('confidence'),
            gbif_match_type=gbif_data.get('matchType'),
            gbif_status=gbif_data.get('status'),
            kingdom=gbif_data.get('kingdom'),
            phylum=gbif_data.get('phylum'),
            class_name=gbif_data.get('class'),
            order=gbif_data.get('order'),
            family=gbif_data.get('family'),
            genus=gbif_data.get('genus'),
            checklistbank_id=clb_data.get('id'),
            gnv_sources=gnv_sources if gnv_sources else None
        )


def print_identity(identity: SpeciesIdentity, format_type: str = 'pretty'):
    """Print species identity in various formats"""
    
    if format_type == 'json':
        print(json.dumps(asdict(identity), indent=2, default=str))
        return
    
    # Pretty print
    print("\n" + "=" * 60)
    print(" SPECIES IDENTITY RESOLVED")
    print("=" * 60)
    
    print(f"\n Scientific Name: {identity.scientific_name}")
    if identity.authorship:
        print(f"   Authority: {identity.authorship}")
    
    if identity.policy_code:
        print(f"\n  Policy Identifiers:")
        print(f"   EU Birds/Habitats Directive: {identity.policy_code}")
        if identity.eunis_url:
            print(f"   EUNIS: {identity.eunis_url}")
    
    print(f"\n GBIF Backbone Taxonomy:")
    print(f"   Usage Key: {identity.gbif_usage_key}")
    print(f"   Match: {identity.gbif_match_type} ({identity.gbif_confidence}% confidence)")
    print(f"   Status: {identity.gbif_status}")
    
    print(f"\n Classification:")
    if identity.kingdom:
        print(f"   Kingdom: {identity.kingdom}")
    if identity.phylum:
        print(f"   Phylum: {identity.phylum}")
    if identity.class_name:
        print(f"   Class: {identity.class_name}")
    if identity.order:
        print(f"   Order: {identity.order}")
    if identity.family:
        print(f"   Family: {identity.family}")
    if identity.genus:
        print(f"   Genus: {identity.genus}")
    
    if identity.checklistbank_id:
        print(f"\n ChecklistBank ID: {identity.checklistbank_id}")
    
    if identity.gnv_sources:
        print(f"\n🔗 Cross-Database Identifiers ({len(identity.gnv_sources)} sources):")
        for source, data in list(identity.gnv_sources.items())[:10]:
            print(f"   • {source}: {data.get('record_id', 'N/A')}")
            if data.get('url'):
                print(f"     → {data['url']}")
    
    print("\n Entity Resolution Summary:")
    print(f"   Successfully resolved identifiers across {len(identity.gnv_sources or {})} databases")
    print(f"   This demonstrates entity resolution similar to customer identity")
    print(f"   resolution (e.g., Zingg) - one species, many identifiers")
    
    print("\n Direct Links:")
    if identity.gbif_usage_key:
        print(f"   GBIF: https://www.gbif.org/species/{identity.gbif_usage_key}")
    if identity.checklistbank_id:
        print(f"   ChecklistBank: https://www.checklistbank.org/dataset/3/taxon/{identity.checklistbank_id}")
    if identity.eunis_url:
        print(f"   EUNIS: {identity.eunis_url}")
    print(f"   Global Names: https://verifier.globalnames.org/?names={identity.scientific_name.replace(' ', '+')}")
    
    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description='Species Identifier Resolution Service - Dynamically resolves species across databases',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python species_resolver.py "A072"
  python species_resolver.py "Pernis apivorus"
  python species_resolver.py "Falco apivorus" --format json
  python species_resolver.py "1234" --refresh-cache
        """
    )
    
    parser.add_argument('query', help='Species name or policy code (e.g., A072 or "Pernis apivorus")')
    parser.add_argument('--format', choices=['pretty', 'json'], default='pretty',
                       help='Output format (default: pretty)')
    parser.add_argument('--refresh-cache', action='store_true',
                       help='Force refresh policy codes from EEA')
    
    args = parser.parse_args()
    
    try:
        # Initialize policy code cache
        cache = PolicyCodeCache()
        
        if args.refresh_cache:
            print("Forcing cache refresh...")
            cache.refresh()
        
        # Resolve species
        resolver = SpeciesResolver(cache)
        identity = resolver.resolve(args.query)
        print_identity(identity, args.format)
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
