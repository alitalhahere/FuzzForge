#!/usr/bin/env python3
"""
Async fuzzing engine for FuzzForge.
"""

import asyncio
import aiohttp
import time
from colorama import Fore, Style

class Fuzzer:
    def __init__(self, target, wordlist, method='GET', headers=None, data=None, concurrency=50, timeout=5):
        self.target = target.rstrip('/')
        self.wordlist = wordlist
        self.method = method.upper()
        self.headers = headers or {}
        self.data = data
        self.concurrency = concurrency
        self.timeout = timeout
        self.results = []
        self.semaphore = asyncio.Semaphore(concurrency)

    async def fetch(self, session, path):
        url = f"{self.target}/{path.lstrip('/')}"
        async with self.semaphore:
            try:
                if self.method == 'GET':
                    async with session.get(url, headers=self.headers, timeout=self.timeout) as resp:
                        return {
                            'url': url,
                            'status': resp.status,
                            'length': len(await resp.text()),
                            'headers': dict(resp.headers),
                            'path': path
                        }
                elif self.method == 'POST':
                    async with session.post(url, headers=self.headers, data=self.data, timeout=self.timeout) as resp:
                        return {
                            'url': url,
                            'status': resp.status,
                            'length': len(await resp.text()),
                            'headers': dict(resp.headers),
                            'path': path
                        }
            except asyncio.TimeoutError:
                return {'url': url, 'status': 'TIMEOUT', 'path': path}
            except Exception as e:
                return {'url': url, 'status': 'ERROR', 'error': str(e), 'path': path}

    async def run(self):
        print(f"\n{Fore.CYAN}[*] Fuzzing {self.target} with {len(self.wordlist)} payloads...{Style.RESET_ALL}")
        start = time.time()

        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(session, word) for word in self.wordlist]
            self.results = await asyncio.gather(*tasks)

        elapsed = time.time() - start
        print(f"{Fore.GREEN}[+] Completed in {elapsed:.2f} seconds.{Style.RESET_ALL}")
        return self.results

    def get_interesting(self):
        interesting_codes = [200, 301, 302, 303, 307, 308, 401, 403, 500, 502, 503]
        return [r for r in self.results if r.get('status') in interesting_codes]