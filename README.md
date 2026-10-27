# PassForge

> **by : mammadow1337**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue" alt="Python version">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Offline-100%25-success" alt="Offline">
  <img src="https://img.shields.io/badge/Author-mammadow1337-purple" alt="Author">
</p>

**PassForge** is a fast, offline password, passphrase, and PIN generator for developers and security-conscious users.

It uses Python's built-in `secrets` module to generate cryptographically secure random values. No generated password is stored, transmitted, logged, or sent to any server.

## Features

- Secure random passwords
- Memorable passphrases
- Numeric PINs
- Customizable character sets
- Ambiguous-character exclusion
- Entropy and strength estimation
- Clipboard copy support
- Colorful terminal banner and output
- Fully offline operation
- No account, telemetry, or network requests

## Installation

```bash
git clone https://github.com/mammadow1337/PassForge.git
cd PassForge
python -m venv .venv
pip install -r requirements.txt

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

## Usage

Generate a default 16-character password:

```bash
python passforge.py
```

Generate a 24-character password:

```bash
python passforge.py --password --length 24
```

Generate 5 passwords without ambiguous characters:

```bash
python passforge.py --count 5 --no-ambiguous
```

Generate a passphrase:

```bash
python passforge.py --passphrase
```

Generate a 6-word passphrase using `_` as separator:

```bash
python passforge.py --passphrase --words 6 --separator "_"
```

Generate an 8-digit PIN:

```bash
python passforge.py --pin --length 8
```

Copy the first generated password to the clipboard:

```bash
python passforge.py --copy
```

## Example output

```text
Type: Random password
Result: Vq7#mR2x!pLz9@Kd
Entropy: 105.1 bits
Strength: Very strong
```

## Security notes

- PassForge uses the `secrets` module for security-sensitive random value generation.
- Passwords are generated locally and are never saved or transmitted.
- Entropy estimates assume uniformly random character selection.
- For important accounts, use a password manager and enable multi-factor authentication.
- Longer passwords and passphrases generally provide more resistance against guessing attacks.

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.
