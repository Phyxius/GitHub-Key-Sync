# Github Key Synchronizer

This script synchronizes your GitHub authorized SSH keys with an `authorized_keys` file stored on a web server, using PGPy to verify the file to prevent takeovers. It will also add each key as a valid SSH signing key. It won't remove revoked keys since that will retroactively mark any commits signed with them as unverified; you'll have to do that yourself if that is what you want.

## Installation
Configure `config.py` with appropriate information. It requires a URL to download, a path to a stored PGP public key, and a GitHub personal access token with permissions to read/write SSH keys. You will also need to `pip install requests ghapi pgpy`.

You probably will also want to add it to a scheduler like cron.