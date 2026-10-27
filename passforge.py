#!/usr/bin/env python3
"""
PassForge - A secure, customizable password and passphrase generator.

Copyright (c) 2026 mammadow1337
Licensed under the MIT License.
"""

import argparse
import math
import os
import secrets
import string
import sys

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
except ImportError:
    print("Missing dependency: rich. Run: pip install -r requirements.txt")
    sys.exit(1)

console = Console()

BANNER = r"""
 ██████╗  █████╗ ███████╗███████╗███████╗ ██████╗ ██████╗  ██████╗ ███████╗
 ██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔═══██╗██╔════╝
 ██████╔╝███████║███████╗███████╗█████╗  ██║   ██║██████╔╝██║   ██║███████╗
 ██╔═══╝ ██╔══██║╚════██║╚════██║██╔══╝  ██║   ██║██╔══██╗██║   ██║╚════██║
 ██║     ██║  ██║███████║███████║███████╗╚██████╔╝██║  ██║╚██████╔╝███████║
 ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝

                        by : mammadow1337
"""

LOWER = string.ascii_lowercase
UPPER = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?/~"

AMBIGUOUS = set("Il1O0o")


def print_banner() -> None:
    console.print(Panel.fit(
        f"[bold cyan]{BANNER}[/bold cyan]\n"
        "[bold white]Secure Password & Passphrase Generator[/bold white]\n"
        "[dim]Cryptographically secure - Offline - No data collection[/dim]\n\n"
        "[bold magenta]by : mammadow1337[/bold magenta]",
        border_style="cyan",
    ))


def calculate_entropy(length: int, pool_size: int) -> float:
    if pool_size <= 1:
        return 0.0
    return length * math.log2(pool_size)


def entropy_label(bits: float) -> str:
    if bits < 40:
        return "[red]Weak[/red]"
    if bits < 60:
        return "[yellow]Fair[/yellow]"
    if bits < 80:
        return "[green]Strong[/green]"
    return "[bold green]Very strong[/bold green]"


def generate_password(
    length: int = 16,
    use_upper: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
    exclude_ambiguous: bool = False,
) -> str:
    if length < 4:
        raise ValueError("Password length must be at least 4 characters.")

    pools = [LOWER]
    if use_upper:
        pools.append(UPPER)
    if use_digits:
        pools.append(DIGITS)
    if use_symbols:
        pools.append(SYMBOLS)

    if exclude_ambiguous:
        pools = [
            "".join(char for char in pool if char not in AMBIGUOUS)
            for pool in pools
        ]
        pools = [pool for pool in pools if pool]

    alphabet = "".join(pools)
    if len(alphabet) < 4:
        raise ValueError("Not enough characters available after exclusions.")

    password_chars = [secrets.choice(pool) for pool in pools]
    remaining = length - len(password_chars)
    password_chars.extend(secrets.choice(alphabet) for _ in range(remaining))

    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


def generate_pin(length: int = 6) -> str:
    if not 4 <= length <= 16:
        raise ValueError("PIN length must be between 4 and 16 digits.")
    return "".join(secrets.choice(DIGITS) for _ in range(length))


def generate_passphrase(
    word_count: int = 5,
    separator: str = "-",
    capitalize: bool = True,
    add_number: bool = True,
    add_symbol: bool = False,
) -> str:
    if not 3 <= word_count <= 12:
        raise ValueError("Passphrase must contain between 3 and 12 words.")

    words = load_wordlist()
    selected = [secrets.choice(words) for _ in range(word_count)]

    if capitalize:
        selected = [word.capitalize() for word in selected]

    passphrase = separator.join(selected)

    if add_number:
        passphrase += separator + str(secrets.randbelow(9000) + 1000)

    if add_symbol:
        passphrase += secrets.choice("!@#$%^&*")

    return passphrase


def load_wordlist() -> list[str]:
    bundled_path = os.path.join(os.path.dirname(__file__), "wordlist.txt")

    if os.path.exists(bundled_path):
        with open(bundled_path, "r", encoding="utf-8") as file:
            words = [line.strip() for line in file if line.strip()]

        words = [word for word in words if word.isalpha() and 3 <= len(word) <= 10]

        if len(words) >= 1000:
            return words

    fallback = [
        "apple", "river", "cloud", "stone", "tiger", "maple", "ocean", "comet",
        "falcon", "harbor", "lantern", "meadow", "nimbus", "orbit", "pebble",
        "quartz", "raven", "saffron", "thunder", "velvet", "willow", "zephyr",
        "canyon", "ember", "forest", "glacier", "horizon", "island", "jungle",
        "kernel", "lagoon", "marble", "nebula", "onyx", "prairie", "quiver",
        "reef", "summit", "tundra", "umbra", "violet", "walnut", "xenon",
        "yonder", "zenith", "aurora", "basalt", "cobalt", "drift", "echo",
    ]

    if len(fallback) < 1000:
        console.print(
            "[yellow]Warning: Using a small built-in fallback wordlist. "
            "Add wordlist.txt for stronger passphrases.[/yellow]"
        )

    return fallback


def show_result(password: str, entropy: float, kind: str) -> None:
    table = Table(show_header=False, border_style="cyan")
    table.add_row("[bold]Type[/bold]", kind)
    table.add_row("[bold]Result[/bold]", f"[bold green]{password}[/bold green]")
    table.add_row("[bold]Entropy[/bold]", f"{entropy:.1f} bits")
    table.add_row("[bold]Strength[/bold]", entropy_label(entropy))

    console.print(Panel(table, title="[bold cyan]Generated Secret[/bold cyan]", border_style="cyan"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="PassForge",
        description="Generate secure passwords, passphrases, and PINs offline.",
    )

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-p", "--password", action="store_true", help="Generate a random password (default)")
    mode.add_argument("-x", "--passphrase", action="store_true", help="Generate a memorable passphrase")
    mode.add_argument("-n", "--pin", action="store_true", help="Generate a numeric PIN")

    parser.add_argument("-l", "--length", type=int, default=16, help="Password or PIN length")
    parser.add_argument("-w", "--words", type=int, default=5, help="Number of words in a passphrase")
    parser.add_argument("-c", "--count", type=int, default=1, help="Number of results to generate")
    parser.add_argument("--no-upper", action="store_true", help="Exclude uppercase letters")
    parser.add_argument("--no-digits", action="store_true", help="Exclude digits")
    parser.add_argument("--no-symbols", action="store_true", help="Exclude symbols")
    parser.add_argument("--no-ambiguous", action="store_true", help="Exclude ambiguous characters")
    parser.add_argument("--separator", default="-", help="Passphrase separator")
    parser.add_argument("--no-capitalize", action="store_true", help="Do not capitalize passphrase words")
    parser.add_argument("--no-number", action="store_true", help="Do not add a number to passphrase")
    parser.add_argument("--add-symbol", action="store_true", help="Add a symbol to passphrase")
    parser.add_argument("--copy", action="store_true", help="Copy the first result to clipboard")
    parser.add_argument("--no-banner", action="store_true", help="Hide startup banner")

    return parser


def copy_to_clipboard(text: str) -> bool:
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except Exception:
        return False


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.no_banner:
        print_banner()

    try:
        for index in range(args.count):
            if args.pin:
                result = generate_pin(args.length)
                entropy = calculate_entropy(args.length, 10)
                kind = "Numeric PIN"

            elif args.passphrase:
                result = generate_passphrase(
                    word_count=args.words,
                    separator=args.separator,
                    capitalize=not args.no_capitalize,
                    add_number=not args.no_number,
                    add_symbol=args.add_symbol,
                )
                entropy = args.words * math.log2(7776)
                kind = "Passphrase"

            else:
                result = generate_password(
                    length=args.length,
                    use_upper=not args.no_upper,
                    use_digits=not args.no_digits,
                    use_symbols=not args.no_symbols,
                    exclude_ambiguous=args.no_ambiguous,
                )
                pool_size = len(LOWER)
                if not args.no_upper:
                    pool_size += len(UPPER)
                if not args.no_digits:
                    pool_size += len(DIGITS)
                if not args.no_symbols:
                    pool_size += len(SYMBOLS)

                if args.no_ambiguous:
                    pool_size -= len(AMBIGUOUS & set(LOWER + UPPER + DIGITS))

                entropy = calculate_entropy(args.length, max(pool_size, 1))
                kind = "Random password"

            show_result(result, entropy, kind)

            if args.copy and index == 0:
                if copy_to_clipboard(result):
                    console.print("[dim]Copied first result to clipboard.[/dim]")
                else:
                    console.print("[yellow]Clipboard support unavailable. Install pyperclip.[/yellow]")

        return 0

    except ValueError as error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
