# 🔨 FuzzForge

**Forge Your Way to Vulnerabilities – Fast, concurrent web fuzzer for bug bounty and pentesting.**

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Async](https://img.shields.io/badge/async-aiohttp-orange)

## 🎯 Purpose

FuzzForge helps security professionals:
- Discover hidden directories and files
- Identify parameter injection points
- Detect SQL injection and XSS vulnerabilities
- Automate fuzzing with async concurrency

## 📦 Installation

```bash
git clone https://github.com/alitalhahere/FuzzForge.git
```
```bash
cd FuzzForge
```
```bash
pip install -r requirements.txt
```
## 🚀 Usage

```bash
# Directory fuzzing
python fuzzforge.py http://example.com/FUZZ --dirs -c 50
```
```bash
# Parameter fuzzing
python fuzzforge.py http://example.com/page.php?FUZZ=test --params
```
```bash
# SQL injection testing
python fuzzforge.py http://example.com/page.php?id=FUZZ --sqli
```
```bash
# XSS testing
python fuzzforge.py http://example.com/search?q=FUZZ --xss
```
```bash
# Custom wordlist
python fuzzforge.py http://example.com/FUZZ -w wordlists/custom.txt
```
```bash
# POST method
python fuzzforge.py http://example.com/login --dirs -m POST -d "username=FUZZ&password=test"
```
```bash
# Generate HTML report
python fuzzforge.py http://example.com/FUZZ --dirs --html
```
## 👤 Author

Ali Talha – [LinkedIn](https://www.linkedin.com/in/imalitalha)
