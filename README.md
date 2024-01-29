![pylint](https://img.shields.io/badge/PyLint-10.00-brightgreen?logo=python&logoColor=white)

# Description
Implements some basic automation for auto submitting tips on [kicktipp](https://kicktipp.com). The auto submitting is based on [selenium](https://www.selenium.dev) browser automation. Login credentials are PGP-encrypted with [SOPS](https://technotim.live/posts/install-mozilla-sops/).

Currently only two result submitting strategies are implemented:
- `2-1` for the "2-1 bot" (use -2)
- `random` for the "random bot" (use -r)

but the automation module can be extended easily to support any type of bets.


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
./src/auto_submit_tips.py -h
usage: Kicktipp auto tipping [-h] [-2 | -r]

Perform automatic kicktipp tipping for the bots

options:
  -h, --help  show this help message and exit
  -2          2:1 tipping
  -r          random tipping
```
