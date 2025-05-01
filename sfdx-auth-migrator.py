#!/usr/bin/env python3
"""
SFDX Auth Migrator v1.0
A cross-platform tool for migrating SFDX authentication across different operating systems
"""

import os
import json
import subprocess
import sys
import argparse
from pathlib import Path

class SFDXAuthMigrator:
    def __init__(self):
        self.export_dir = Path("sfdx_auth_export")
        self.version = "1.0.0"
    
    def run_sfdx_command(self, command, capture_output=True):
        """Run an SFDX command and return the result"""
        try:
            if capture_output:
                result = subprocess.run(command, capture_output=True, text=True, check=True)
                return result.stdout
            else:
                return subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {' '.join(command)}")
            print(f"Error: {e.stderr if hasattr(e, 'stderr') else str(e)}")
            return None
    
    def get_all_orgs(self):
        """Get all authenticated orgs"""
        output = self.run_sfdx_command(['sfdx', 'force:org:list', '--all', '--json'])
        if not output:
            return []
        
        try:
            data = json.loads(output)
            orgs = []
            for org in data.get('result', {}).get('nonScratchOrgs', []):
                if org.get('alias'):
                    orgs.append(org['alias'])
            return orgs
        except json.JSONDecodeError:
            print("Error parsing org list")
            return []
    
    def export_auth(self):
        """Export authentication info from current machine"""
        print(f"SFDX Auth Migrator v{self.version}")
        print("Exporting SFDX authentication info...")
        
        # Create export directory
        self.export_dir.mkdir(exist_ok=True)
        
        # Get all orgs
        orgs = self.get_all_orgs()
        if not orgs:
            print("No orgs found to export")
            return False
        
        success_count = 0
        fail_count = 0
        
        # Export each org
        for alias in orgs:
            print(f"Exporting auth for: {alias}")
            
            # Get auth URL
            output = self.run_sfdx_command([
                'sfdx', 'force:org:display', 
                '--target-org', alias, 
                '--verbose', '--json'
            ])
            
            if output:
                try:
                    data = json.loads(output)
                    auth_url = data.get('result', {}).get('sfdxAuthUrl')
                    
                    if auth_url:
                        # Write to file
                        auth_file = self.export_dir / f"{alias}.auth.url"
                        with open(auth_file, 'w', encoding='utf-8') as f:
                            f.write(auth_url)
                        print(f"✓ Successfully exported: {alias}")
                        success_count += 1
                    else:
                        print(f"✗ No auth URL found for: {alias}")
                        fail_count += 1
                except json.JSONDecodeError:
                    print(f"✗ Error parsing auth data for: {alias}")
                    fail_count += 1
            else:
                fail_count += 1
        
        print(f"\nExport complete!")
        print(f"Successfully exported: {success_count}")
        print(f"Failed to export: {fail_count}")
        print(f"\nTo transfer to another machine:")
        print("1. Copy the 'sfdx_auth_export' directory")
        print("2. Run: python sfdx-auth-migrator.py import")
        
        return success_count > 0
    
    def import_auth(self):
        """Import authentication info to current machine"""
        print(f"SFDX Auth Migrator v{self.version}")
        print("Importing SFDX authentication info...")
        
        if not self.export_dir.exists():
            print(f"ERROR: {self.export_dir} directory not found!")
            print("Please ensure you've copied the export directory to this location.")
            return False
        
        success_count = 0
        fail_count = 0
        
        # Import each auth file
        for auth_file in self.export_dir.glob("*.auth.url"):
            alias = auth_file.stem
            print(f"Importing auth for: {alias}")
            
            try:
                with open(auth_file, 'r', encoding='utf-8') as f:
                    auth_url = f.read().strip()
                
                # Clean the auth URL
                auth_url = auth_url.replace('\r', '').replace('\n', '').strip()
                
                # Import using stdin
                process = subprocess.Popen(
                    ['sfdx', 'auth:sfdxurl:store', '--alias', alias, '--sfdx-url-stdin'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                stdout, stderr = process.communicate(input=auth_url)
                
                if process.returncode == 0:
                    print(f"✓ Successfully imported: {alias}")
                    success_count += 1
                else:
                    print(f"✗ Failed to import: {alias}")
                    print(f"  Error: {stderr}")
                    fail_count += 1
                    
            except Exception as e:
                print(f"✗ Error processing {alias}: {str(e)}")
                fail_count += 1
        
        print(f"\nImport complete!")
        print(f"Successfully imported: {success_count}")
        print(f"Failed to import: {fail_count}")
        
        # Verify imported orgs
        print("\nVerifying imported orgs:")
        self.run_sfdx_command(['sfdx', 'force:org:list', '--all'], capture_output=False)
        
        return success_count > 0

def main():
    parser = argparse.ArgumentParser(description='SFDX Auth Migrator - Cross-platform authentication migration tool')
    parser.add_argument('command', choices=['export', 'import'], help='Command to execute')
    parser.add_argument('--version', action='version', version=f'SFDX Auth Migrator v1.0.0')
    
    args = parser.parse_args()
    
    migrator = SFDXAuthMigrator()
    
    if args.command == 'export':
        migrator.export_auth()
    elif args.command == 'import':
        migrator.import_auth()

if __name__ == "__main__":
    main()