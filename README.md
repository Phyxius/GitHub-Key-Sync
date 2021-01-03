# Github Key Synchronizer

This script synchronizes your GitHub authorized SSH keys with an `authorized_keys` file stored on a web server, using PGPy to verify the file to prevent takeovers.

## Installation
Configure `config.py` with appropriate information. It requires a URL to download, a path to a stored PGP public key, and a GitHub personal access token with permissions to read/write SSH keys. You will also need to `pip install requests PyGithub pgpy`.