#!/usr/bin/env python3
"""
FuzzForge – Fast, concurrent web application fuzzer.
"""

import asyncio
import argparse
import sys
from colorama import init, Fore, Style
from modules.fuzzer import Fuzzer
from modules.detectors import Detector
from modules.payloads import DIRECTORY_WORDLIST, PARAMETER_WORDLIST, SQLI_PAYLOADS, XSS_PAYLOADS
from modules.reporter import generate_json_report, generate_html_report

init(autoreset=True)

BANNER = f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════╗
║                    🔨 FUZZFORGE v1.0 🔨                          ║
║               Forge Your Way to Vulnerabilities                  ║
║         Async Web Fuzzer | Directory | SQLi | XSS                ║
╚══════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
{Fore.YELLOW}🔐 Author: Ali Talha (CEH) | GitHub: alitalhahere{Style.RESET_ALL}
{Fore.GREEN}⚡ Crafted with Precision | Bug Bounty Ready{Style.RESET_ALL}
"""

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description='FuzzForge - Web Fuzzing Tool')
    parser.add_argument('target', help='Target URL (e.g., http://example.com/FUZZ)')
    parser.add_argument('-w', '--wordlist', help='Custom wordlist file (one per line)')
    parser.add_argument('--dirs', action='store_true', help='Use built‑in directory wordlist')
    parser.add_argument('--params', action='store_true', help='Use built‑in parameter wordlist')
    parser.add_argument('--sqli', action='store_true', help='Test for SQL injection')
    parser.add_argument('--xss', action='store_true', help='Test for XSS')
    parser.add_argument('-c', '--concurrency', type=int, default=50, help='Concurrent requests (default: 50)')
    parser.add_argument('-t', '--timeout', type=int, default=5, help='Request timeout (default: 5)')
    parser.add_argument('-m', '--method', default='GET', choices=['GET', 'POST'], help='HTTP method (default: GET)')
    parser.add_argument('-d', '--data', help='POST data (for POST method)')
    parser.add_argument('--output', default='reports', help='Output directory')
    parser.add_argument('--html', action='store_true', help='Generate HTML report')
    parser.add_argument('--json', action='store_true', help='Generate JSON report')

    args = parser.parse_args()

    wordlist = []
    if args.wordlist:
        try:
            with open(args.wordlist, 'r') as f:
                wordlist = [line.strip() for line in f if line.strip()]
            print(f"{Fore.GREEN}[+] Loaded {len(wordlist)} words from {args.wordlist}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[-] Error loading wordlist: {e}{Style.RESET_ALL}")
            sys.exit(1)
    elif args.dirs:
        wordlist = DIRECTORY_WORDLIST
        print(f"{Fore.GREEN}[+] Using directory wordlist ({len(wordlist)} entries){Style.RESET_ALL}")
    elif args.params:
        wordlist = PARAMETER_WORDLIST
        print(f"{Fore.GREEN}[+] Using parameter wordlist ({len(wordlist)} entries){Style.RESET_ALL}")
    elif args.sqli:
        wordlist = SQLI_PAYLOADS
        print(f"{Fore.GREEN}[+] Using SQLi payloads ({len(wordlist)} entries){Style.RESET_ALL}")
    elif args.xss:
        wordlist = XSS_PAYLOADS
        print(f"{Fore.GREEN}[+] Using XSS payloads ({len(wordlist)} entries){Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[-] Specify a wordlist (-w, --dirs, --params, --sqli, or --xss){Style.RESET_ALL}")
        sys.exit(1)

    fuzzer = Fuzzer(
        target=args.target,
        wordlist=wordlist,
        method=args.method,
        concurrency=args.concurrency,
        timeout=args.timeout,
        data=args.data
    )

    try:
        results = asyncio.run(fuzzer.run())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Interrupted by user{Style.RESET_ALL}")
        sys.exit(0)

    interesting = fuzzer.get_interesting()
    print(f"\n{Fore.CYAN}[*] Interesting findings: {len(interesting)}/{len(results)}{Style.RESET_ALL}")

    for r in interesting[:20]:
        status = r.get('status', 'N/A')
        color = Fore.GREEN if status == 200 else Fore.YELLOW if status in [301, 302] else Fore.RED if status >= 400 else Fore.WHITE
        print(f"  {color}{status}{Style.RESET_ALL} - {r['url']} ({r.get('length', 'N/A')} bytes)")

    if len(interesting) > 20:
        print(f"  ... and {len(interesting) - 20} more")

    if args.json:
        generate_json_report(interesting, f"{args.output}/fuzz_report.json")
    if args.html:
        generate_html_report(interesting, f"{args.output}/fuzz_report.html")

    print(f"\n{Fore.GREEN}[+] Fuzzing complete.{Style.RESET_ALL}")

if __name__ == '__main__':
    main()