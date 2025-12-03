#!/usr/bin/env python3
"""
BMD Natura2000 CLI Tool
Command-line interface for querying EEA DiscoData Natura2000 database
"""

import urllib.parse
import httpx
import json
import asyncio
import sys
from typing import Optional

EEA_BASE = "https://discodata.eea.europa.eu/sql?query="

async def query_eea(sql: str) -> Optional[dict]:
    """Forward SQL to EEA endpoint and return cleaned JSON."""
    url = EEA_BASE + urllib.parse.quote(sql)
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(url)
            r.raise_for_status()
            data = r.json()
            return data.get("records", data)
    except Exception as e:
        print(f"Error querying EEA: {e}", file=sys.stderr)
        return None

async def get_site_info(site_code: str):
    """Get site information for a Natura2000 site."""
    sql = f"""
    SELECT * FROM [BISE].[latest].[Site_Information]
    WHERE site_code='{site_code}'
    """
    results = await query_eea(sql)
    return {
        "@id": f"https://biodiversity.europa.eu/sites/natura2000/{site_code}",
        "source": "https://discodata.eea.europa.eu",
        "results": results
    }

async def get_site_habitats(site_code: str):
    """Get habitat list for a Natura2000 site."""
    sql = f"""
    SELECT * FROM [BISE].[latest].[Site_Habitats_List]
    WHERE site_code='{site_code}'
    """
    results = await query_eea(sql)
    return {
        "@id": f"https://biodiversity.europa.eu/sites/natura2000/{site_code}",
        "source": "https://discodata.eea.europa.eu",
        "results": results
    }

async def get_site_species(site_code: str):
    """Get species list for a Natura2000 site."""
    sql = f"""
    SELECT * FROM [BISE].[latest].[Site_Species_List_Details]
    WHERE site_code='{site_code}'
    """
    results = await query_eea(sql)
    return {
        "@id": f"https://biodiversity.europa.eu/sites/natura2000/{site_code}",
        "source": "https://discodata.eea.europa.eu",
        "results": results
    }

async def get_habitat_info(code_2000: str):
    """Get information about a specific habitat type."""
    sql = f"""
    SELECT * FROM [BISE].[latest].[Habitat_Information]
    WHERE code_2000='{code_2000}'
    """
    results = await query_eea(sql)
    return {
        "@id": f"https://biodiversity.europa.eu/habitats/ANNEX1_{code_2000}",
        "source": "https://discodata.eea.europa.eu",
        "results": results
    }

def print_json(data):
    """Pretty print JSON data."""
    print(json.dumps(data, indent=2, ensure_ascii=False))

def print_help():
    """Print usage information."""
    help_text = """
BMD Natura2000 CLI Tool
Usage: python natura2000_cli.py <command> <code>

Commands:
  site-info <site_code>       Get site information
  site-habitats <site_code>   Get habitats at a site
  site-species <site_code>    Get species at a site
  habitat-info <code_2000>    Get habitat information
  help                        Show this help message

Examples:
  python natura2000_cli.py site-info NL9801015
  python natura2000_cli.py site-habitats NL9801015
  python natura2000_cli.py site-species NL9801015
  python natura2000_cli.py habitat-info 6230
"""
    print(help_text)

async def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Error: No command provided", file=sys.stderr)
        print_help()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "help" or command == "-h" or command == "--help":
        print_help()
        sys.exit(0)
    
    if len(sys.argv) < 3:
        print(f"Error: Command '{command}' requires a code argument", file=sys.stderr)
        print_help()
        sys.exit(1)
    
    code = sys.argv[2]
    
    result = None
    
    if command == "site-info":
        result = await get_site_info(code)
    elif command == "site-habitats":
        result = await get_site_habitats(code)
    elif command == "site-species":
        result = await get_site_species(code)
    elif command == "habitat-info":
        result = await get_habitat_info(code)
    else:
        print(f"Error: Unknown command '{command}'", file=sys.stderr)
        print_help()
        sys.exit(1)
    
    if result:
        print_json(result)
    else:
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
