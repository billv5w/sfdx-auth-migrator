# SFDX Auth Migrator

A cross-platform command-line tool for migrating Salesforce CLI (SFDX) authentication across different operating systems and development environments.

## Overview

SFDX Auth Migrator simplifies the process of transferring your authenticated Salesforce org connections from one machine to another, whether you're switching computers, setting up a new development environment, or sharing connection credentials with team members.

## Features

-   **Export authenticated org connections** from your current machine
-   **Import authentication files** to a new development environment
-   **Cross-platform support** - works on Windows, macOS, and Linux
-   **Alias preservation** - maintains your org aliases during transfer
-   **Batch processing** - handles multiple org connections simultaneously
-   **Verification** - includes built-in verification of imported connections

## Prerequisites

-   Python 3.6 or higher
-   Salesforce CLI (SFDX) installed and configured
-   Authenticated Salesforce org connections on the source machine

## Installation

1. Download the `sfdx-auth-migrator.py` script
2. Make it executable (on Unix-based systems):
    ```bash
    chmod +x sfdx-auth-migrator.py
    ```

## Usage

### Exporting Authentication

On your source machine (the one with authenticated orgs):

```bash
# Using Python 3
`python3 sfdx-auth-migrator.py export`

# Or if you made it executable
./sfdx-auth-migrator.py export
```

This will:

1. Scan for all authenticated orgs
2. Export their authentication URLs
3. Save them to a local `sfdx_auth_export` directory

### Transferring the Export

1. Copy the `sfdx_auth_export` directory to your target machine
2. Place it in the same directory as the script

### Importing Authentication

On your target machine:

```bash
# Using Python 3
python3 sfdx-auth-migrator.py import

# Or if you made it executable
./sfdx-auth-migrator.py import
```

This will:

1. Import all authentication files from the export directory
2. Create matching aliases on the new machine
3. Verify the imported connections

## Command Reference

### Export Command

```bash
python3 sfdx-auth-migrator.py export
```

Exports all authenticated org connections from the current machine.

### Import Command

```bash
python3 sfdx-auth-migrator.py import
```

Imports org connections from the exported authentication files.

### Version Information

```bash
python3 sfdx-auth-migrator.py --version
```

Displays the current version of the tool.

### Help

```bash
python3 sfdx-auth-migrator.py --help
```

Shows available commands and options.

## How It Works

1. **Export Process**:

    - Queries SFDX for all authenticated org connections
    - Retrieves authentication URLs for each org
    - Saves URLs to individual files in `sfdx_auth_export` directory

2. **Import Process**:
    - Reads authentication files from the export directory
    - Uses SFDX `auth:sfdxurl:store` command to recreate connections
    - Preserves original aliases and connection properties

## Security Considerations

⚠️ **Important**: The exported authentication files contain sensitive information that allows access to your Salesforce orgs.

-   Keep the `sfdx_auth_export` directory secure
-   Delete exported files after successful transfer
-   Do not commit these files to version control

## Troubleshooting

### Common Issues

1. **"No orgs found to export"**

    - Ensure you have authenticated orgs on the source machine
    - Run `sfdx force:org:list --all` to verify

2. **"Export directory not found"**

    - Ensure you've copied the `sfdx_auth_export` directory to the target machine
    - Place it in the same directory as the script

3. **Import fails for specific orgs**
    - Check if the source org is still accessible
    - Verify network connectivity on the target machine
    - Re-authenticate manually if needed

### Debug Mode

Add the `--verbose` flag to SFDX commands for more detailed output:

```bash
sfdx force:org:list --all --verbose
```

## Limitations

-   Only works with authenticated orgs (not scratch orgs)
-   Requires Python 3.6+
-   Depends on SFDX CLI being properly installed

## Contributing

Feel free to submit issues and enhancement requests!

## License

This tool is provided as-is under the MIT License.

## Version History

-   **v1.0.0** - Initial release with basic export/import functionality

## Author

SFDX Auth Migrator - A cross-platform tool for migrating SFDX authentication

---

For support, please open an issue in the repository or check the [Salesforce CLI documentation](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference.htm).
