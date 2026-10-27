#!/usr/bin/env python3
"""PassForge ” by : mammadow1337. MIT License."""
import argparse
import math
import secrets
import string
from pathlib import Path

LOWER = string.ascii_lowercase
UPPER = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?/~"
AMBIGUOUS = set("Il1O0o")


def print_banner():
    print()
    print("[ PASSFORGE                     ]")
    print("[ MODE   : PASSWORD GENERATOR   ]")
    print("[ AUTHOR : mammadow1337         ]")
    print()


def show_result(password, entropy, kind):
    print(f"  Type     : {kind}")
    print(f"  Password : {password}\n")


def password_pools(args):
    pools = [LOWER]
    if not args.no_upper:
        pools.append(UPPER)
    if not args.no_digits:
        pools.append(DIGITS)
    if not args.no_symbols:
        pools.append(SYMBOLS)
    if args.no_ambiguous:
        pools = ["".join(c for c in pool if c not in AMBIGUOUS) for pool in pools]
    return pools


def load_wordlist():
    path = Path(__file__).with_name("wordlist.txt")
    if path.exists():
        words = list(dict.fromkeys(w.strip().lower() for w in path.read_text(encoding="utf-8").splitlines() if w.strip().isalpha() and 3 <= len(w.strip()) <= 10))
        if len(words) >= 1000:
            return words
    print("  Warning: Small fallback wordlist; add wordlist.txt for stronger passphrases.\n")
    return "apple river cloud stone tiger maple ocean comet falcon harbor lantern meadow nimbus orbit pebble quartz raven saffron thunder velvet willow zephyr canyon ember forest glacier horizon island jungle kernel lagoon marble nebula onyx prairie quiver reef summit tundra umbra violet walnut xenon yonder zenith aurora basalt cobalt drift echo".split()


def build_parser():
    parser = argparse.ArgumentParser(description="PassForge â€” by : mammadow1337")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-p", "--password", action="store_true")
    mode.add_argument("-x", "--passphrase", action="store_true")
    mode.add_argument("-n", "--pin", action="store_true")
    parser.add_argument("-l", "--length", type=int, default=16)
    parser.add_argument("-w", "--words", type=int, default=5)
    parser.add_argument("-c", "--count", type=int, default=1)
    for flag in ("no-upper", "no-digits", "no-symbols", "no-ambiguous", "no-capitalize", "no-number", "add-symbol", "copy", "no-banner"):
        parser.add_argument("--" + flag, action="store_true")
    parser.add_argument("--separator", default="-")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if args.count < 1:
        parser.error("Count must be at least 1.")
    if args.pin and not 4 <= args.length <= 16:
        parser.error("PIN length must be between 4 and 16 digits.")
    if not args.pin and not args.passphrase and args.length < 4:
        parser.error("Password length must be at least 4.")
    if args.passphrase and not 3 <= args.words <= 12:
        parser.error("Passphrase must contain between 3 and 12 words.")
    if not args.no_banner:
        print_banner()
    words = load_wordlist() if args.passphrase else None
    for index in range(args.count):
        if args.pin:
            result = "".join(secrets.choice(DIGITS) for _ in range(args.length))
            kind = "Numeric PIN"
        elif args.passphrase:
            chosen = [secrets.choice(words) for _ in range(args.words)]
            if not args.no_capitalize:
                chosen = [w.capitalize() for w in chosen]
            result = args.separator.join(chosen)
            if not args.no_number:
                result += args.separator + str(secrets.randbelow(9000) + 1000)
            if args.add_symbol:
                result += secrets.choice("!@#$%^&*")
            kind = "Passphrase"
        else:
            pools = password_pools(args)
            alphabet = "".join(pools)
            chars = [secrets.choice(pool) for pool in pools]
            chars.extend(secrets.choice(alphabet) for _ in range(args.length - len(chars)))
            secrets.SystemRandom().shuffle(chars)
            result = "".join(chars)
            kind = "Random password"
        show_result(result, None, kind)
        if args.copy and index == 0:
            try:
                import pyperclip
                pyperclip.copy(result)
                print("  Copied first result to clipboard.\n")
            except Exception:
                print("  Clipboard unavailable. Install pyperclip and check clipboard access.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
