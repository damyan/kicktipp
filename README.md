![pylint](https://img.shields.io/badge/pylint-9.44-yellow?logo=python&logoColor=white)

# Description
Implements some basic automation for auto submitting tips on [kicktipp](https://kicktipp.com). The auto submitting is based on [selenium](https://www.selenium.dev) browser automation. Login credentials are PGP-encrypted with [SOPS](https://technotim.live/posts/install-mozilla-sops/).

Currently only result submitting for the `2-1 bot` is implemented, but the automation module can be extended easily for each types of bets.


# Requirements

## OS
Tested only on MacOS. Because no OS-specific functionality is used, though, it should work on any modern OS.

## Software
- sops
- python3 + selenium module
- chrome


# Installation
```bash
brew install python3 sops
pip install -r requirements.txt
```


# Execution

```bash
./auto_submit_tips.py
```
